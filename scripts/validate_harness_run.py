#!/usr/bin/env python3
"""Validate harness run artifacts before step closure or gate decisions."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


PUBLISH_WORD_RE = re.compile(r"\b(publish|published|publishing|check-?in|submit)\b", re.I)
PASS_WORD_RE = re.compile(r"\b(pass|ready)\b", re.I)
BAD_BOUNDARY_RE = re.compile(
    r"\b(partial|condition(?:al)?|defer(?:red)?|provisional|guarded later|before publish|later gate)\b",
    re.I,
)
TOOL_OWNER_RE = re.compile(
    r"\b("
    r"tool(?:s)?|validation(?: tools)?|browser|ssh|shell|runtime|build|ci(?:/cd)?|"
    r"pipeline|sandbox|session|credential|host|path|repo mirror|evidence"
    r")\b",
    re.I,
)
CLAUDE_IMPLEMENTER_RE = re.compile(r"\b(claude|opus|sonnet|haiku)\b", re.I)
EXPLICIT_MODEL_EXCEPTION_RE = re.compile(
    r"\b(?:model|implementer|implementation)[- ]?(?:exception|override)\b|"
    r"\buser[- ]?approved[- ]?(?:model|implementer|implementation)[- ]?(?:exception|override)\b",
    re.I,
)
SMALL_MODEL_RE = re.compile(
    r"\b("
    r"small[- ]?model|fast[- ]?model|"
    r"(?:gpt|o[0-9]|claude|gemini|llama|mistral|qwen|deepseek|grok)[\w.-]*[- ](?:mini|nano|flash|haiku)|"
    r"(?:mini|nano|flash|haiku)[- ][\w.-]*(?:model|agent|delegate|worker|reviewer|gate)"
    r")\b",
    re.I,
)
CODEX_OWNER_RE = re.compile(r"\b(main )?codex( current thread| main| validation tools)?\b", re.I)
CURRENT_CONTEXT_RE = re.compile(
    r"\b(current (codex )?(thread|context)|same (codex )?(thread|context|instance)|main codex|codex current thread)\b",
    re.I,
)
LOCAL_ONLY_RE = re.compile(
    r"\b(local-only|local only|disposable mirror|not assigned|publish/check-in owner: not assigned|"
    r"implementation is still local|no publish owner|not publish-ready|non-publish)\b",
    re.I,
)
TELEMETRY_EVENTS = {
    "step_enter",
    "step_exit",
    "gate_verdict",
    "rework_requested",
    "compaction",
    "model_call",
    "human_wait_enter",
    "human_wait_exit",
}
TELEMETRY_STEPS = {"preflight", "S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"}
TELEMETRY_MAX_LINES = 50_000
FIELD_LINE_RE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9 /-]*?)\s*:\s*(.*)\s*$")
STEP_RE = re.compile(r"\bS[0-8]\b", re.I)
CHECKPOINT_STEP_ORDER = ["S1", "S3", "S5", "S7"]
CHECKPOINT_REQUIRED_FIELDS = [
    "Run ID",
    "Active Run Workspace Path",
    "Current Step",
    "Last Completed Step",
    "Checkpoint Seq",
    "Last Updated",
    "Completed Checklist",
    "Remaining Checklist",
    "Inflight Delegations",
    "Boundary Violations",
    "Next Action",
    "Blockers",
    "Evidence Pointers",
    "Context Pressure Signal",
]
CHECKPOINT_ALLOW_NONE_FIELDS = {"Inflight Delegations", "Boundary Violations", "Blockers", "Context Pressure Signal"}
PATH_TOKEN_RE = re.compile(
    r"(?i)(?:[A-Za-z]:[\\/])?(?:[\w.-]+[\\/])+[\w.@-]+|[\w.@-]+\.(?:md|txt|jsonl?|py|ya?ml|tsx?|jsx?|css|html|log|patch)"
)
LOCATOR_TOKEN_RE = re.compile(r"(?i)(:\d+|#[\w.-]+|@[0-9a-f]{7,40}|\bcommit\s+[0-9a-f]{7,40}\b|\bartifact\s*:)")
CONTEXT_PRESSURE_RE = re.compile(r"(?i)\b(auto[- ]?compact|compacted|context pressure|context overload|token pressure)\b")
DELEGATION_RECORD_REQUIRED_FIELDS = [
    "Slice ID",
    "Owner",
    "Context Boundary",
    "Scope",
    "Allowed Tools",
    "Writable Area",
    "Expected Evidence",
    "Delegated At",
]
DELEGATION_SLICE_RE = re.compile(
    r"(?i)\b("
    r"implement(?:ation|er)?|diagnostic|root[- ]?cause|explor(?:e|atory|ation)|"
    r"verif(?:y|ication)|runtime|test(?:ing| execution)?|log review|worktree|"
    r"publish|commit|check[- ]?in|submit"
    r")\b"
)
VAGUE_EVIDENCE_RE = re.compile(
    r"(?i)^\s*(?:tbd|todo|unknown|n/?a|none|see above|see output|validator passed|"
    r"tests passed|done|proof|evidence|record|checkpoint|artifact|pass(?:ed)?)\s*\.?\s*$"
)
KNOWN_ROLE_KEYS = {
    "orchestrator",
    "implementer",
    "critic",
    "quality_gate",
    "runtime_verifier",
    "advisor",
    "source_analyst",
    "principle_mapper",
    "workflow_designer",
    "template_editor",
    "publish_worker",
    "human_decision_maker",
}


@dataclass
class MarkdownDoc:
    path: Path
    rel: str
    text: str


@dataclass
class ContinuationCheckpoint:
    path: Path
    rel: str
    text: str
    fields: dict[str, str]
    seq: int | None


@dataclass
class RoleRow:
    role: str
    owner: str
    boundary: str
    shared: str = ""
    notes: str = ""


@dataclass
class DelegationRecord:
    fields: dict[str, str]
    source: str


@dataclass
class RunArtifacts:
    root: Path
    docs: list[MarkdownDoc]
    text: str
    s1_text: str
    s7_text: str
    s8_text: str
    publish_intent: str
    boundary_status: str
    roles: dict[str, RoleRow]
    matrix_text: str
    task_graph_text: str
    run_id: str
    telemetry_mode: str
    telemetry_event_path: str
    telemetry_profiler_path: str
    checkpoints: list[ContinuationCheckpoint]
    current_pointer: str
    checkpoint_errors: list[str]


def _read_markdown_docs(root: Path) -> list[MarkdownDoc]:
    if root.is_file():
        return [MarkdownDoc(path=root, rel=root.name, text=root.read_text(encoding="utf-8"))]
    if not root.exists():
        raise FileNotFoundError(root)
    docs: list[MarkdownDoc] = []
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root).as_posix()
        docs.append(MarkdownDoc(path=path, rel=rel, text=path.read_text(encoding="utf-8")))
    return docs


def _join_markdown(docs: list[MarkdownDoc]) -> str:
    parts: list[str] = []
    for doc in docs:
        parts.append(f"\n\n<!-- FILE: {doc.rel} -->\n")
        parts.append(doc.text)
    return "".join(parts)


def _section(text: str, step: str) -> str:
    pattern = re.compile(
        rf"(?ims)^#{{1,4}}\s*(?:step\s*)?{re.escape(step)}\b.*?(?=^#{{1,4}}\s*(?:step\s*)?S[0-9]\b|\Z)"
    )
    matches = list(pattern.finditer(text))
    return "\n\n".join(m.group(0) for m in matches)


def _field(text: str, name: str) -> str:
    match = re.search(rf"(?im)^\s*{re.escape(name)}\s*:\s*(.+?)\s*$", text)
    return match.group(1).strip() if match else ""


def _parse_fields(text: str) -> dict[str, str]:
    fields: dict[str, list[str]] = {}
    current: str | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        match = FIELD_LINE_RE.match(line)
        if match and "|" not in line:
            current = _clean_cell(match.group(1))
            fields.setdefault(current, [])
            value = match.group(2).strip()
            if value:
                fields[current].append(value)
            continue
        if current and line.strip() and not line.lstrip().startswith("#"):
            fields[current].append(line.strip())
    return {name: "\n".join(values).strip() for name, values in fields.items()}


def _strip_pointer(value: str) -> str:
    for raw in value.splitlines():
        line = raw.strip().lstrip("-").strip()
        if not line:
            continue
        backtick = re.search(r"`([^`]+)`", line)
        if backtick:
            return backtick.group(1).strip()
        return line.strip("<>")
    return ""


def _checkpoint_section(text: str) -> str:
    match = re.search(
        r"(?ims)^#{1,4}\s*(?:Continuation Packet|Continuation Checkpoint|Checkpoint Packet)\b.*?(?=^#{1,4}\s|\Z)",
        text,
    )
    return match.group(0) if match else text


def _load_checkpoint_file(path: Path, rel: str) -> ContinuationCheckpoint:
    text = path.read_text(encoding="utf-8")
    checkpoint_text = _checkpoint_section(text)
    fields = _parse_fields(checkpoint_text)
    seq = _parse_int(fields.get("Checkpoint Seq", ""))
    return ContinuationCheckpoint(path=path, rel=rel, text=checkpoint_text, fields=fields, seq=seq)


def _parse_int(value: str) -> int | None:
    match = re.search(r"\d+", value or "")
    return int(match.group(0)) if match else None


def _load_checkpoints(root: Path, docs: list[MarkdownDoc]) -> tuple[list[ContinuationCheckpoint], str, list[str]]:
    errors: list[str] = []
    if root.is_file():
        section = _checkpoint_section(docs[0].text)
        if section == docs[0].text and not re.search(r"(?im)^\s*Checkpoint Seq\s*:", section):
            return [], "", ["CONTINUATION_PACKET_MISSING: no Continuation Packet section found."]
        fields = _parse_fields(section)
        return [ContinuationCheckpoint(path=root, rel=root.name, text=section, fields=fields, seq=_parse_int(fields.get("Checkpoint Seq", "")))], root.name, errors

    current_path = root / "CURRENT.md"
    if not current_path.exists():
        return [], "", ["CONTINUATION_CURRENT_MISSING: Lite/Full run workspace must contain CURRENT.md."]

    current_text = current_path.read_text(encoding="utf-8")
    current_fields = _parse_fields(current_text)
    pointer = _strip_pointer(
        current_fields.get("Current Checkpoint", "")
        or current_fields.get("Latest Checkpoint", "")
        or current_text
    )
    if not pointer:
        errors.append("CONTINUATION_CURRENT_POINTER_MISSING: CURRENT.md must point to the latest checkpoint.")
        return [], "", errors
    if Path(pointer).is_absolute():
        errors.append("CONTINUATION_CURRENT_POINTER_ABSOLUTE: CURRENT.md must use a run-workspace-relative path.")
        return [], pointer, errors

    checkpoint_paths: dict[Path, str] = {}
    checkpoint_dir = root / "checkpoints"
    if checkpoint_dir.exists():
        for path in sorted(checkpoint_dir.glob("*.md")):
            checkpoint_paths[path.resolve()] = path.relative_to(root).as_posix()
    pointed = (root / pointer).resolve()
    if not pointed.exists():
        errors.append(f"CONTINUATION_CURRENT_TARGET_MISSING: CURRENT.md points to `{pointer}`, but that file does not exist.")
    elif pointed.suffix.lower() == ".md":
        checkpoint_paths[pointed] = pointer.replace("\\", "/")

    checkpoints = [_load_checkpoint_file(path, rel) for path, rel in sorted(checkpoint_paths.items(), key=lambda item: item[1])]
    return checkpoints, pointer.replace("\\", "/"), errors


def _clean_cell(cell: str) -> str:
    return re.sub(r"\s+", " ", cell.strip().strip("|").strip())


def _parse_role_rows(s1_text: str) -> dict[str, RoleRow]:
    rows: dict[str, RoleRow] = {}
    for raw in s1_text.splitlines():
        line = raw.strip()
        if "|" not in line or "---" in line:
            continue
        cells = [_clean_cell(c) for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        first = cells[0].lower()
        if first in {"role", "phase-critical action", "action"}:
            continue
        role = cells[0]
        role_key = _role_key(role)
        if role_key not in KNOWN_ROLE_KEYS:
            continue
        owner = cells[1] if len(cells) > 1 else ""
        boundary = cells[2] if len(cells) > 2 else ""
        shared = cells[3] if len(cells) > 3 else ""
        notes = cells[4] if len(cells) > 4 else ""
        rows[role_key] = RoleRow(role=role, owner=owner, boundary=boundary, shared=shared, notes=notes)
    return rows


def _role_key(role: str) -> str:
    normalized = re.sub(r"[^a-z]+", "_", role.lower()).strip("_")
    if normalized.startswith("quality_gate"):
        return "quality_gate"
    if normalized.startswith("orchestrator"):
        return "orchestrator"
    if normalized.startswith("implementer"):
        return "implementer"
    if normalized.startswith("critic"):
        return "critic"
    if normalized.startswith("runtime_verifier"):
        return "runtime_verifier"
    if normalized.startswith("advisor"):
        return "advisor"
    if normalized.startswith("source_analyst"):
        return "source_analyst"
    if normalized.startswith("principle_mapper"):
        return "principle_mapper"
    if normalized.startswith("workflow_designer"):
        return "workflow_designer"
    if normalized.startswith("template_editor"):
        return "template_editor"
    if normalized.startswith("publish_worker"):
        return "publish_worker"
    if normalized.startswith("human_decision_maker"):
        return "human_decision_maker"
    return normalized


def _matrix_text(s1_text: str) -> str:
    match = re.search(r"(?ims)(Run-Specific Responsibility Matrix.*?)(?=^#|\Z)", s1_text)
    return match.group(1) if match else ""


def _task_graph_text(text: str) -> str:
    matches = []
    for step in ("S3", "Step S3"):
        section = _section(text, step)
        if section:
            matches.append(section)
    if not matches:
        pattern = re.compile(r"(?ims)^#{1,4}\s*Task Graph\b.*?(?=^#{1,4}\s*(?:S[0-9]|Step S[0-9])\b|\Z)")
        matches = [match.group(0) for match in pattern.finditer(text)]
    return "\n\n".join(matches)


def _delegation_record_texts(docs: list[MarkdownDoc]) -> list[tuple[str, str]]:
    records: list[tuple[str, str]] = []
    pattern = re.compile(
        r"(?ims)^#{1,4}\s*(?:Delegation Record|Delegation Records)\b.*?(?=^#{1,4}\s|\Z)"
    )
    for doc in docs:
        for index, match in enumerate(pattern.finditer(doc.text), start=1):
            records.append((f"{doc.rel}#delegation-record-{index}", match.group(0)))
    return records


def load_run(root: Path) -> RunArtifacts:
    docs = _read_markdown_docs(root)
    text = _join_markdown(docs)
    s1_text = _section(text, "S1")
    s7_text = _section(text, "S7")
    s8_text = _section(text, "S8")
    task_graph_text = _task_graph_text(text)
    checkpoints, current_pointer, checkpoint_errors = _load_checkpoints(root, docs)
    return RunArtifacts(
        root=root,
        docs=docs,
        text=text,
        s1_text=s1_text,
        s7_text=s7_text,
        s8_text=s8_text,
        publish_intent=_field(s1_text, "Publish Intent"),
        boundary_status=_field(s1_text, "Boundary Status"),
        roles=_parse_role_rows(s1_text),
        matrix_text=_matrix_text(s1_text),
        task_graph_text=task_graph_text,
        run_id=_field(text, "Run ID"),
        telemetry_mode=_field(text, "Telemetry Mode"),
        telemetry_event_path=_field(text, "Event Log Path"),
        telemetry_profiler_path=_field(text, "Profiler Summary Path"),
        checkpoints=checkpoints,
        current_pointer=current_pointer,
        checkpoint_errors=checkpoint_errors,
    )


def _norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _canonical_owner(row: RoleRow) -> str:
    combined = " ".join([row.owner, row.boundary, row.notes])
    if CODEX_OWNER_RE.search(combined) or CURRENT_CONTEXT_RE.search(combined):
        return "main codex"
    return _norm(row.owner)


def _combined_role_text(row: RoleRow) -> str:
    return " ".join([row.role, row.owner, row.boundary, row.shared, row.notes])


def _model_posture_text(row: RoleRow) -> str:
    return " ".join([row.owner, row.notes])


def _is_publish_intent(value: str) -> bool:
    return _norm(value) == "publish"


def _is_nonpublish_intent(value: str) -> bool:
    return "non publish" in _norm(value) or "exploration" in _norm(value)


def _has_publish_claim(text: str) -> bool:
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if re.match(r"(?i)^\s*(decision|verdict|status)\s*:", line):
            if PUBLISH_WORD_RE.search(line) and re.search(r"(?i)\b(pass|ready|guarded)\b", line):
                return True
        if len(line) <= 80 and not re.search(r"[a-z]", line) and PUBLISH_WORD_RE.search(line):
            if re.search(r"(?i)\b(pass|ready|guarded)\b", line):
                return True
    return False


def _clean_path_value(value: str) -> str:
    return value.strip().strip("`").strip('"').strip("'")


def _resolve_run_relative_path(run: RunArtifacts, value: str, label: str) -> tuple[Path | None, str | None]:
    raw = _clean_path_value(value)
    if not raw:
        return None, None
    normalized = raw.replace("\\", "/")
    if normalized.startswith("<run-workspace>/"):
        if run.root.is_file():
            return None, f"S0_TELEMETRY_PATH_UNVERIFIABLE: cannot verify {label} from a single markdown file."
        return run.root / normalized.removeprefix("<run-workspace>/"), None
    path = Path(raw)
    if path.is_absolute():
        return path, None
    if run.root.is_file():
        return None, f"S0_TELEMETRY_PATH_UNVERIFIABLE: cannot verify {label} from a single markdown file."
    return run.root / path, None


def _is_nonnegative_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _validate_telemetry_record(
    record: object, line_no: int, run: RunArtifacts, errors: list[str], warnings: list[str]
) -> None:
    if not isinstance(record, dict):
        errors.append(f"S0_TELEMETRY_RECORD_NOT_OBJECT: line {line_no} is not a JSON object.")
        return

    for field_name in ["run_id", "ts", "event", "step"]:
        if field_name not in record or record[field_name] in {"", None}:
            errors.append(f"S0_TELEMETRY_FIELD_MISSING: line {line_no} missing `{field_name}`.")

    run_id = record.get("run_id")
    if run.run_id and isinstance(run_id, str) and run_id != run.run_id:
        warnings.append(
            f"S0_TELEMETRY_RUN_ID_MISMATCH: line {line_no} run_id `{run_id}` does not match `{run.run_id}`."
        )

    event = record.get("event")
    if isinstance(event, str) and event not in TELEMETRY_EVENTS:
        errors.append(f"S0_TELEMETRY_EVENT_INVALID: line {line_no} event `{event}` is not allowed.")
    elif event is not None and not isinstance(event, str):
        errors.append(f"S0_TELEMETRY_EVENT_INVALID: line {line_no} event must be a string.")

    step = record.get("step")
    if isinstance(step, str) and step not in TELEMETRY_STEPS:
        errors.append(f"S0_TELEMETRY_STEP_INVALID: line {line_no} step `{step}` is not allowed.")
    elif step is not None and not isinstance(step, str):
        errors.append(f"S0_TELEMETRY_STEP_INVALID: line {line_no} step must be a string.")

    active_ms = record.get("active_ms", 0)
    human_wait_ms = record.get("human_wait_ms", 0)
    for field_name, value in [("active_ms", active_ms), ("human_wait_ms", human_wait_ms)]:
        if field_name in record and not _is_nonnegative_int(value):
            errors.append(f"S0_TELEMETRY_TIMING_INVALID: line {line_no} `{field_name}` must be a non-negative integer.")
    if _is_nonnegative_int(active_ms) and _is_nonnegative_int(human_wait_ms):
        if event != "step_exit" and active_ms > 0 and human_wait_ms > 0:
            errors.append(
                f"S0_TELEMETRY_TIMING_DOUBLE_COUNT: line {line_no} has both active_ms and human_wait_ms."
            )


def _validate_telemetry(run: RunArtifacts, errors: list[str], warnings: list[str]) -> None:
    mode = _norm(run.telemetry_mode)
    if not run.telemetry_mode:
        errors.append("S0_TELEMETRY_MODE_MISSING: `Telemetry Mode` must be `Off` or `On`.")
        return
    if "|" in run.telemetry_mode:
        errors.append("S0_TELEMETRY_MODE_TEMPLATE: replace the template value with `Off` or `On`.")
        return
    if mode not in {"off", "on"}:
        errors.append("S0_TELEMETRY_MODE_INVALID: `Telemetry Mode` must be `Off` or `On`.")
        return
    if mode == "off":
        return

    if not run.telemetry_event_path:
        errors.append("S0_TELEMETRY_PATH_MISSING: `Telemetry Mode: On` requires `Event Log Path`.")
        return

    event_path, path_warning = _resolve_run_relative_path(run, run.telemetry_event_path, "Event Log Path")
    if path_warning:
        errors.append(path_warning)
    if event_path is None:
        return
    if not event_path.exists() or not event_path.is_file():
        errors.append(f"S0_TELEMETRY_FILE_MISSING: event log not found at `{event_path}`.")
        return
    if event_path.stat().st_size == 0:
        errors.append(f"S0_TELEMETRY_FILE_EMPTY: event log is empty at `{event_path}`.")
        return

    with event_path.open("r", encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, start=1):
            if line_no > TELEMETRY_MAX_LINES:
                warnings.append(
                    f"S0_TELEMETRY_SCAN_TRUNCATED: scanned first {TELEMETRY_MAX_LINES} telemetry lines only."
                )
                break
            line = raw.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"S0_TELEMETRY_JSONL_INVALID: line {line_no} is invalid JSON: {exc.msg}.")
                continue
            _validate_telemetry_record(record, line_no, run, errors, warnings)

    if run.telemetry_profiler_path:
        profiler_path, profiler_warning = _resolve_run_relative_path(
            run, run.telemetry_profiler_path, "Profiler Summary Path"
        )
        if profiler_warning:
            warnings.append(profiler_warning)
        elif profiler_path is not None:
            if not profiler_path.exists() or not profiler_path.is_file():
                warnings.append(f"S8_PROFILER_FILE_MISSING: profiler summary not found at `{profiler_path}`.")
            else:
                try:
                    json.loads(profiler_path.read_text(encoding="utf-8"))
                except json.JSONDecodeError as exc:
                    warnings.append(f"S8_PROFILER_JSON_INVALID: profiler summary is invalid JSON: {exc.msg}.")


def _field_empty(value: str, allow_none: bool = False) -> bool:
    stripped = re.sub(r"\s+", " ", value or "").strip()
    if not stripped:
        return True
    lowered = stripped.lower()
    if allow_none and lowered in {"none", "n/a", "na"}:
        return False
    return bool(re.fullmatch(r"(<[^>]+>|tbd|todo|unknown|-|n/a|na)", lowered, re.I))


def _root_matches_checkpoint_path(root: Path, value: str) -> bool:
    raw = _strip_pointer(value)
    if not raw or re.fullmatch(r"<[^>]+>", raw):
        return False
    normalized_root = root.resolve().as_posix().rstrip("/").lower()
    normalized_value = raw.replace("\\", "/").rstrip("/").lower()
    if Path(raw).is_absolute():
        return Path(raw).resolve().as_posix().rstrip("/").lower() == normalized_root
    return normalized_root == normalized_value or normalized_root.endswith("/" + normalized_value)


def _checkpoint_mentions_step(checkpoint: ContinuationCheckpoint, step: str) -> bool:
    step = step.upper()
    values = " ".join(
        [
            checkpoint.fields.get("Current Step", ""),
            checkpoint.fields.get("Last Completed Step", ""),
            checkpoint.fields.get("Completed Checklist", ""),
            checkpoint.fields.get("Remaining Checklist", ""),
            checkpoint.rel,
        ]
    )
    return bool(re.search(rf"\b{step}\b", values, re.I))


def _latest_checkpoint(run: RunArtifacts) -> ContinuationCheckpoint | None:
    if not run.checkpoints:
        return None
    if run.current_pointer:
        for checkpoint in run.checkpoints:
            if checkpoint.rel.replace("\\", "/") == run.current_pointer:
                return checkpoint
    checkpoints_with_seq = [checkpoint for checkpoint in run.checkpoints if checkpoint.seq is not None]
    if checkpoints_with_seq:
        return max(checkpoints_with_seq, key=lambda checkpoint: checkpoint.seq or -1)
    return run.checkpoints[-1]


def _parse_task_graph_rows(task_graph_text: str) -> tuple[list[dict[str, str]], bool, list[str]]:
    task_rows: list[dict[str, str]] = []
    current: dict[str, str] = {}
    table_headers: list[str] = []
    saw_task_graph_table = False
    in_fence = False
    for raw in task_graph_text.splitlines():
        line = raw.strip()
        if re.match(r"(?i)^#{1,4}\s*Delegation Records?\b", line):
            break
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not line:
            continue
        field_match = re.match(r"(?i)^(task|owner|context boundary|depends on|outputs|writable area|validation checkpoint|fallback)\s*:\s*(.*)$", line)
        if field_match:
            key = field_match.group(1).strip().lower()
            value = field_match.group(2).strip()
            current[key] = value
            if key == "fallback":
                task_rows.append(current)
                current = {}
            continue
        if "|" in line and "---" not in line:
            cells = [_clean_cell(c) for c in line.strip("|").split("|")]
            header_candidates = {"task", "owner", "context boundary", "depends on", "outputs", "writable area", "validation checkpoint", "fallback"}
            if cells and cells[0].lower() == "task":
                table_headers = [cell.lower() for cell in cells]
                saw_task_graph_table = True
                continue
            if len(cells) >= 2:
                saw_task_graph_table = True
                row = {}
                if table_headers:
                    for idx, header in enumerate(table_headers):
                        if header in header_candidates:
                            row[header] = cells[idx] if idx < len(cells) else ""
                else:
                    row = {
                        "task": cells[0],
                        "owner": cells[1] if len(cells) > 1 else "",
                        "context boundary": cells[2] if len(cells) > 2 else "",
                        "depends on": cells[3] if len(cells) > 3 else "",
                        "outputs": cells[4] if len(cells) > 4 else "",
                        "writable area": cells[5] if len(cells) > 5 else "",
                        "validation checkpoint": cells[6] if len(cells) > 6 else "",
                        "fallback": cells[7] if len(cells) > 7 else "",
                    }
                task_rows.append(row)
    if current and current not in task_rows:
        task_rows.append(current)
    return task_rows, saw_task_graph_table, table_headers


def _parse_delegation_records(run: RunArtifacts) -> list[DelegationRecord]:
    records: list[DelegationRecord] = []
    for source, text in _delegation_record_texts(run.docs):
        fields = _parse_fields(text)
        if any(field in fields for field in DELEGATION_RECORD_REQUIRED_FIELDS):
            records.append(DelegationRecord(fields=fields, source=source))
            continue
        table_headers: list[str] = []
        for raw in text.splitlines():
            line = raw.strip()
            if "|" not in line or "---" in line:
                continue
            cells = [_clean_cell(c) for c in line.strip("|").split("|")]
            lowered = [cell.lower() for cell in cells]
            if "slice id" in lowered and "owner" in lowered:
                table_headers = cells
                continue
            if table_headers and len(cells) >= 2:
                row = {
                    table_headers[idx]: cells[idx] if idx < len(cells) else ""
                    for idx in range(len(table_headers))
                }
                records.append(DelegationRecord(fields=row, source=source))
    return records


def _record_owner_matches_role(record: DelegationRecord, role: RoleRow) -> bool:
    owner = _norm(record.fields.get("Owner", ""))
    boundary = _norm(record.fields.get("Context Boundary", ""))
    role_names = {_norm(role.role), _norm(role.owner)}
    return bool(owner and boundary and owner in role_names and boundary == _norm(role.boundary))


def _is_concrete_writable_area(value: str) -> bool:
    stripped = value.strip()
    if _field_empty(stripped):
        return False
    return bool(PATH_TOKEN_RE.search(stripped) or re.search(r"(?i)\b(run workspace|<run-workspace>|workspace/|exec-plans/|tests/fixtures/|src/|references/|scripts/)\b", stripped))


def _is_concrete_expected_evidence(value: str) -> bool:
    stripped = value.strip()
    if _field_empty(stripped):
        return False
    if VAGUE_EVIDENCE_RE.fullmatch(stripped):
        return False
    return _has_actionable_evidence_pointer(stripped) or bool(re.search(r"(?i)\bcheckpoint\s+[A-Za-z0-9_.:/# -]+\b", stripped))


def _slice_key(value: str) -> str:
    return _norm(value)


def _record_matches_task(record: DelegationRecord, row: dict[str, str]) -> bool:
    slice_id = record.fields.get("Slice ID", "")
    task = row.get("task", "")
    if not slice_id or not task:
        return False
    return _slice_key(slice_id) == _slice_key(task)


def _requires_delegation_record(row: dict[str, str]) -> bool:
    owner = row.get("owner", "")
    if _role_key(owner) == "implementer":
        return True
    combined = " ".join([row.get("task", ""), owner, row.get("outputs", ""), row.get("validation checkpoint", "")])
    return bool(DELEGATION_SLICE_RE.search(combined))


def _validate_delegation_records(run: RunArtifacts, task_rows: list[dict[str, str]], errors: list[str]) -> None:
    records = _parse_delegation_records(run)
    required_rows = [row for row in task_rows if _requires_delegation_record(row)]
    if required_rows and not records:
        errors.append("S3_DELEGATION_RECORD_MISSING: task-domain slices require field-valid Delegation Records before S3 closes.")

    for record in records:
        label = record.fields.get("Slice ID", record.source)
        for field in DELEGATION_RECORD_REQUIRED_FIELDS:
            if field not in record.fields:
                errors.append(f"S3_DELEGATION_RECORD_FIELD_MISSING: `{label}` missing `{field}`.")
            elif _field_empty(record.fields[field]):
                errors.append(f"S3_DELEGATION_RECORD_FIELD_EMPTY: `{label}` field `{field}` must contain run-specific data.")

        owner = record.fields.get("Owner", "")
        if _role_key(owner) == "orchestrator" or _norm(owner) == _norm(run.roles.get("orchestrator", RoleRow("", "", "")).owner):
            errors.append(f"S3_DELEGATION_RECORD_ORCHESTRATOR_OWNER: `{label}` names Orchestrator as owner.")
        if owner and _role_key(owner) not in KNOWN_ROLE_KEYS:
            errors.append(f"S3_DELEGATION_RECORD_OWNER_UNRECOGNIZED: `{label}` owner `{owner}` must map to an assigned role.")
        elif owner and _role_key(owner) not in run.roles:
            errors.append(f"S3_DELEGATION_RECORD_OWNER_UNASSIGNED: `{label}` owner `{owner}` is not assigned in S1.")
        elif owner and not _record_owner_matches_role(record, run.roles[_role_key(owner)]):
            errors.append(f"S3_DELEGATION_RECORD_BOUNDARY_MISMATCH: `{label}` owner/context boundary does not match the S1 role table.")

        if "Writable Area" in record.fields and not _is_concrete_writable_area(record.fields["Writable Area"]):
            errors.append(f"S3_DELEGATION_RECORD_WRITABLE_AREA_VAGUE: `{label}` must name a concrete writable area.")
        if "Expected Evidence" in record.fields and not _is_concrete_expected_evidence(record.fields["Expected Evidence"]):
            errors.append(f"S3_DELEGATION_RECORD_EVIDENCE_VAGUE: `{label}` must name an artifact path plus locator or checkpoint name.")

    for row in required_rows:
        task = row.get("task", "").strip() or "<unnamed task>"
        matches = [record for record in records if _record_matches_task(record, row)]
        if not matches:
            errors.append(f"S3_DELEGATION_RECORD_MISSING_FOR_SLICE: `{task}` has no matching Delegation Record.")
            continue
        for record in matches:
            if row.get("owner") and _role_key(record.fields.get("Owner", "")) != _role_key(row.get("owner", "")):
                errors.append(f"S3_DELEGATION_RECORD_OWNER_MISMATCH: `{task}` Delegation Record owner does not match the Task Graph owner.")
            if row.get("context boundary") and _norm(record.fields.get("Context Boundary", "")) != _norm(row.get("context boundary", "")):
                errors.append(f"S3_DELEGATION_RECORD_CONTEXT_MISMATCH: `{task}` Delegation Record context boundary does not match the Task Graph.")
            if row.get("writable area") and _norm(record.fields.get("Writable Area", "")) != _norm(row.get("writable area", "")):
                errors.append(f"S3_DELEGATION_RECORD_WRITABLE_AREA_MISMATCH: `{task}` Delegation Record writable area does not match the Task Graph.")


def _validate_continuation(run: RunArtifacts, stage: str) -> tuple[list[str], list[str]]:
    errors: list[str] = list(run.checkpoint_errors)
    warnings: list[str] = []

    if not run.checkpoints:
        errors.append("CONTINUATION_PACKET_MISSING: Lite/Full runs must provide an append-only continuation checkpoint.")
        return errors, warnings

    latest = _latest_checkpoint(run)
    if latest is None:
        errors.append("CONTINUATION_PACKET_MISSING: no readable continuation checkpoint found.")
        return errors, warnings

    expected_stage = _expected_checkpoint_stage(stage)
    if expected_stage and not _checkpoint_mentions_step(latest, expected_stage):
        errors.append(
            f"CONTINUATION_STAGE_MISMATCH: latest checkpoint must reflect `{expected_stage}` for `--stage {stage}`."
        )

    fields = latest.fields
    for field in CHECKPOINT_REQUIRED_FIELDS:
        if field not in fields:
            errors.append(f"CONTINUATION_FIELD_MISSING: `{field}` is required in the latest checkpoint.")
        elif _field_empty(fields[field], allow_none=field in CHECKPOINT_ALLOW_NONE_FIELDS):
            errors.append(f"CONTINUATION_FIELD_EMPTY: `{field}` must contain run-specific recovery data.")

    if "Active Run Workspace Path" in fields and not _root_matches_checkpoint_path(run.root, fields["Active Run Workspace Path"]):
        errors.append(
            "CONTINUATION_WORKSPACE_MISMATCH: `Active Run Workspace Path` does not match the validated run path."
        )

    for field in ["Current Step", "Last Completed Step"]:
        if field in fields and fields[field] and not STEP_RE.search(fields[field]):
            errors.append(f"CONTINUATION_STEP_INVALID: `{field}` must identify an S0-S8 step.")

    if "Checkpoint Seq" in fields and latest.seq is None:
        errors.append("CONTINUATION_SEQ_INVALID: `Checkpoint Seq` must contain an integer.")
    if "Last Updated" in fields and fields["Last Updated"] and not re.search(r"\d{4}-\d{2}-\d{2}", fields["Last Updated"]):
        errors.append("CONTINUATION_LAST_UPDATED_INVALID: `Last Updated` must include an ISO-like date.")

    seqs = [checkpoint.seq for checkpoint in run.checkpoints]
    if any(seq is None for seq in seqs):
        errors.append("CONTINUATION_SEQ_MISSING: every checkpoint file must include `Checkpoint Seq`.")
    numeric_seqs = [seq for seq in seqs if seq is not None]
    if len(numeric_seqs) != len(set(numeric_seqs)):
        errors.append("CONTINUATION_SEQ_DUPLICATE: checkpoint sequence numbers must be unique.")
    if numeric_seqs and numeric_seqs != sorted(numeric_seqs):
        errors.append("CONTINUATION_SEQ_NOT_MONOTONIC: checkpoint sequence numbers must increase in file order.")
    if numeric_seqs and latest.seq != max(numeric_seqs):
        errors.append("CONTINUATION_CURRENT_NOT_LATEST: CURRENT.md must point to the highest checkpoint sequence.")

    required_steps = _required_checkpoint_steps(latest, stage)
    for step in required_steps:
        if not any(_checkpoint_mentions_step(checkpoint, step) for checkpoint in run.checkpoints):
            errors.append(f"CONTINUATION_STEP_CHECKPOINT_MISSING: no checkpoint records `{step}`.")

    evidence = fields.get("Evidence Pointers", "")
    if evidence and not _has_actionable_evidence_pointer(evidence):
        warnings.append(
            "EVIDENCE_POINTER_VAGUE: `Evidence Pointers` should include a path plus a locator such as line, anchor, artifact name, or commit SHA."
        )

    if _is_publish_intent(run.publish_intent) and re.search(r"(?i)\bnon-publish exploration\b", latest.text):
        errors.append(
            "CONTINUATION_INHERITED_NONPUBLISH: latest checkpoint still describes non-publish exploration in a publish run."
        )

    pressure_signal = fields.get("Context Pressure Signal", "")
    if (CONTEXT_PRESSURE_RE.search(run.text) or len(run.text) > 70000) and _field_empty(pressure_signal, allow_none=True):
        warnings.append(
            "CONTEXT_PRESSURE_SIGNAL_MISSING: context pressure is visible, but the latest checkpoint lacks `Context Pressure Signal`."
        )

    return errors, warnings


def _expected_checkpoint_stage(stage: str) -> str | None:
    normalized = stage.lower()
    if normalized in {"s1", "s2"}:
        return "S1"
    if normalized == "s3":
        return "S3"
    if normalized == "s7":
        return "S7"
    return None


def _required_checkpoint_steps(latest: ContinuationCheckpoint, stage: str) -> list[str]:
    if stage in {"s1", "s2"}:
        return ["S1"]
    if stage == "s7":
        return CHECKPOINT_STEP_ORDER.copy()

    state_text = " ".join(
        [
            latest.fields.get("Current Step", ""),
            latest.fields.get("Last Completed Step", ""),
            latest.fields.get("Completed Checklist", ""),
            latest.fields.get("Remaining Checklist", ""),
        ]
    )
    required: list[str] = []
    for step in CHECKPOINT_STEP_ORDER:
        if re.search(rf"\b{step}\b", state_text, re.I):
            required.append(step)
    return required or ["S1"]


def _has_actionable_evidence_pointer(value: str) -> bool:
    for raw in value.splitlines():
        line = raw.strip()
        if not line:
            continue
        if PATH_TOKEN_RE.search(line) and LOCATOR_TOKEN_RE.search(line):
            return True
    return False


def _validate_pointer_discipline(run: RunArtifacts) -> list[str]:
    warnings: list[str] = []
    for doc in run.docs:
        rel = doc.rel.replace("\\", "/")
        if rel == "CURRENT.md" or rel.startswith("checkpoints/"):
            continue
        if len(doc.text) > 80000:
            warnings.append(
                f"MAINLINE_POINTER_DISCIPLINE: `{rel}` is very large; keep mainline artifacts to decisions plus pointers and move bulky evidence into run-workspace artifacts."
            )
            break
        if any(len(line) > 4000 for line in doc.text.splitlines()):
            warnings.append(
                f"MAINLINE_POINTER_DISCIPLINE: `{rel}` contains very long lines; prefer artifact pointers over pasted tool output."
            )
            break
    return warnings


def validate_run(
    run: RunArtifacts, stage: str = "all", skip_telemetry: bool = False
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not run.s1_text:
        errors.append("S1_MISSING: no S1 Role Owner Table section found.")
        return errors, warnings

    if not skip_telemetry:
        _validate_telemetry(run, errors, warnings)

    continuation_errors, continuation_warnings = _validate_continuation(run, stage)
    errors.extend(continuation_errors)
    warnings.extend(continuation_warnings)
    warnings.extend(_validate_pointer_discipline(run))

    required_roles = ["orchestrator", "implementer", "quality_gate"]
    for role in required_roles:
        if role not in run.roles:
            errors.append(f"S1_ROLE_MISSING: required role `{role}` is missing from S1.")
        elif not run.roles[role].owner:
            errors.append(f"S1_OWNER_MISSING: role `{role}` has no accountable owner.")

    if "implementer" in run.roles:
        impl_text = _model_posture_text(run.roles["implementer"])
        if CLAUDE_IMPLEMENTER_RE.search(impl_text) and not EXPLICIT_MODEL_EXCEPTION_RE.search(impl_text):
            warnings.append(
                "S1_IMPLEMENTER_MODEL_POSTURE: Implementer appears to be Claude/Opus-family; prefer GPT/Codex for implementation or record an explicit user-approved exception in S1 notes."
            )

    if "advisor" in run.roles:
        advisor_owner = _canonical_owner(run.roles["advisor"])
        for role_key, code in [
            ("implementer", "S1_ADVISOR_IMPLEMENTER_COLLISION"),
            ("critic", "S1_ADVISOR_CRITIC_COLLISION"),
            ("quality_gate", "S1_ADVISOR_GATE_COLLISION"),
        ]:
            if role_key not in run.roles:
                continue
            if advisor_owner != _canonical_owner(run.roles[role_key]):
                continue
            errors.append(
                f"{code}: Advisor and {run.roles[role_key].role} resolve to the same accountable owner; Advisor output does not satisfy that role's ownership."
            )

    if "quality_gate" in run.roles:
        gate_text = _model_posture_text(run.roles["quality_gate"])
        if SMALL_MODEL_RE.search(gate_text):
            warnings.append(
                "S1_GATE_MODEL_TIER_WEAK: Quality Gate appears to use a small/fast model; final gate decisions should use a stronger model or explicitly justify the exception."
            )

    for source_role in ["source_analyst", "critic"]:
        if source_role in run.roles and SMALL_MODEL_RE.search(_model_posture_text(run.roles[source_role])):
            warnings.append(
                f"S1_{source_role.upper()}_MODEL_TIER_WEAK: `{run.roles[source_role].role}` appears to use a small/fast model for source-fidelity-heavy review; use a stronger model or record why the slice is bounded."
            )

    s7_claims_publish = _has_publish_claim(run.s7_text + "\n" + run.s8_text)

    if not run.publish_intent:
        errors.append("S1_PUBLISH_INTENT_MISSING: S1 must declare `Publish Intent` before S2.")
    elif not (_is_publish_intent(run.publish_intent) or _is_nonpublish_intent(run.publish_intent)):
        errors.append(
            "S1_PUBLISH_INTENT_INVALID: `Publish Intent` must be `Publish` or `Non-publish exploration`."
        )

    if s7_claims_publish and not _is_publish_intent(run.publish_intent):
        errors.append(
            "S7_PUBLISH_CONTRADICTS_INTENT: S7/S8 makes a publish-readiness claim but S1 is not `Publish`."
        )

    publish_like = _is_publish_intent(run.publish_intent) or s7_claims_publish
    if publish_like:
        if not run.boundary_status:
            errors.append("S1_BOUNDARY_STATUS_MISSING: publishable runs must declare `Boundary Status: Satisfied`.")
        elif _norm(run.boundary_status) != "satisfied":
            errors.append(
                "S1_BOUNDARY_STATUS_INVALID: publishable runs must use `Boundary Status: Satisfied` before S2."
            )
        if BAD_BOUNDARY_RE.search(run.s1_text):
            errors.append(
                "S1_BOUNDARY_DEFERRED: S1 contains partial/conditional/deferred boundary language in a publishable run."
            )

    if run.matrix_text == "":
        errors.append("S1_MATRIX_MISSING: S1 must include a Run-Specific Responsibility Matrix before S2.")
    else:
        for required in ["S7 gate verdict", "S8 publish"]:
            if required.lower() not in run.matrix_text.lower():
                errors.append(f"S1_MATRIX_ACTION_MISSING: `{required}` owner resolution is missing.")

    needs_s3_validation = stage in {"s3", "s7"} or bool(run.s7_text)
    if not run.task_graph_text:
        if needs_s3_validation:
            errors.append("S3_TASK_GRAPH_MISSING: no S3 Task Graph section found.")
    else:
        task_rows, saw_task_graph_table, table_headers = _parse_task_graph_rows(run.task_graph_text)

        if saw_task_graph_table and "validation checkpoint" not in table_headers and not any(
            "validation checkpoint" in row for row in task_rows
        ):
            errors.append("S3_TASK_GRAPH_CHECKPOINT_COLUMN_MISSING: Task Graph implementation table must include a Validation Checkpoint column.")
        for idx, row in enumerate(task_rows, start=1):
            if not row.get("owner", "").strip():
                warnings.append(f"S3_TASK_ROW_OWNER_MISSING: Task Graph row {idx} has no Owner field.")
            elif _role_key(row.get("owner", "")) not in KNOWN_ROLE_KEYS:
                warnings.append(
                    f"S3_TASK_ROW_OWNER_UNRECOGNIZED: Task Graph row `{row.get('task', idx)}` has owner `{row.get('owner')}` that may not map to a known role."
                )

        implementation_rows = [
            row for row in task_rows
            if row.get("owner", "").strip() and _role_key(row.get("owner", "")) == "implementer"
        ]
        for idx, row in enumerate(implementation_rows, start=1):
            task_value = row.get("task", "")
            if not task_value:
                errors.append(f"S3_TASK_ROW_MISSING_TASK: implementation node {idx} has no Task field.")
            task_norm = _norm(task_value)
            if not task_norm:
                errors.append(f"S3_TASK_ROW_EMPTY_TASK: implementation node {idx} has an empty Task field.")
            if not row.get("validation checkpoint", "").strip():
                errors.append(
                    f"S3_TASK_ROW_CHECKPOINT_MISSING: implementation node `{task_value or idx}` must define Validation Checkpoint."
                )
            if not row.get("writable area", "").strip():
                errors.append(
                    f"S3_TASK_ROW_WRITABLE_AREA_MISSING: implementation node `{task_value or idx}` must define Writable Area."
                )
            if task_value:
                behavior_words = re.findall(r"[a-z0-9]+", task_norm)
                if len(behavior_words) > 14 and not re.search(r"\b(file cluster|cluster|single|one|focused|slice)\b", task_norm):
                    warnings.append(
                        f"S3_TASK_ROW_TOO_BROAD: implementation node `{task_value}` looks too broad for one slice; split it before S4."
                    )
            checkpoint = row.get("validation checkpoint", "")
            if checkpoint and not re.search(r"\b(test|lint|typecheck|lsp|log|api|browser|runtime|evidence|probe|smoke|check)\b", checkpoint, re.I):
                warnings.append(
                    f"S3_TASK_ROW_WEAK_CHECKPOINT: implementation node `{task_value or idx}` uses a checkpoint that may be too vague."
                )

        _validate_delegation_records(run, task_rows, errors)

    if all(role in run.roles for role in required_roles):
        orch = run.roles["orchestrator"]
        impl = run.roles["implementer"]
        gate = run.roles["quality_gate"]
        owner_map = {
            "Orchestrator": _canonical_owner(orch),
            "Implementer": _canonical_owner(impl),
            "Quality Gate": _canonical_owner(gate),
        }
        if publish_like:
            if owner_map["Orchestrator"] == owner_map["Implementer"]:
                errors.append(
                    "S1_OWNER_COLLISION: Orchestrator and Implementer resolve to the same accountable owner."
                )
            if owner_map["Orchestrator"] == owner_map["Quality Gate"]:
                errors.append(
                    "S1_OWNER_COLLISION: Orchestrator and Quality Gate resolve to the same accountable owner."
                )
            if owner_map["Implementer"] == owner_map["Quality Gate"]:
                errors.append(
                    "S1_OWNER_COLLISION: Implementer and Quality Gate resolve to the same accountable owner."
                )
            if _norm(impl.boundary) == _norm(gate.boundary):
                errors.append(
                    "S1_CONTEXT_COLLISION: Implementer and Quality Gate share the same Context Boundary."
                )
        gate_combined = " ".join([gate.owner, gate.boundary, gate.notes])
        if TOOL_OWNER_RE.search(gate.owner) or TOOL_OWNER_RE.search(gate_combined) and not re.search(
            r"\b(claude|opus|agent|delegate|reviewer|gate owner|quality gate session)\b", gate_combined, re.I
        ):
            errors.append(
                "S1_GATE_OWNER_SURFACE: Quality Gate is assigned to a tool, validation surface, runtime, or evidence surface."
            )

    if s7_claims_publish and LOCAL_ONLY_RE.search(run.s7_text + "\n" + run.s8_text + "\n" + run.matrix_text):
        errors.append(
            "S7_PUBLISH_SCOPE_CONFLICT: S7/S8 claims publish readiness while evidence says local-only or publish owner is unassigned."
        )

    return errors, warnings


def _run_self_tests(script: Path) -> int:
    repo = script.parent.parent
    cases = {
        "tests/fixtures/invalid/advisor-critic-collision": False,
        "tests/fixtures/invalid/advisor-gate-collision": False,
        "tests/fixtures/invalid/advisor-implementer-collision": False,
        "tests/fixtures/invalid/corpview-regression": False,
        "tests/fixtures/invalid/missing-intent-publish-s7": False,
        "tests/fixtures/invalid/missing-continuation-current": False,
        "tests/fixtures/invalid/nonpublish-publish-s7": False,
        "tests/fixtures/invalid/same-owner-alias": False,
        "tests/fixtures/invalid/stale-continuation-current": False,
        "tests/fixtures/invalid/tool-gate-boundary": False,
        "tests/fixtures/invalid/bad-boundary-status": False,
        "tests/fixtures/invalid/missing-delegation-record.md": False,
        "tests/fixtures/invalid/orchestrator-delegation-record.md": False,
        "tests/fixtures/invalid/empty-task-checkpoint-cell": False,
        "tests/fixtures/invalid/missing-task-checkpoint": False,
        "tests/fixtures/invalid/telemetry-mode-missing": False,
        "tests/fixtures/invalid/telemetry-mode-invalid": False,
        "tests/fixtures/invalid/telemetry-on-file-missing": False,
        "tests/fixtures/invalid/telemetry-on-bad-jsonl": False,
        "tests/fixtures/invalid/telemetry-on-bad-event": False,
        "tests/fixtures/invalid/telemetry-on-double-count": False,
        "tests/fixtures/invalid/telemetry-on-single-file-unverifiable.md": False,
        "tests/fixtures/invalid/telemetry-mode-template": False,
        "tests/fixtures/valid/single-runbook": True,
        "tests/fixtures/valid/separate-files": True,
        "tests/fixtures/valid/model-tier-warnings": True,
        "tests/fixtures/valid/telemetry-on-minimal": True,
        "tests/fixtures/valid/telemetry-on-profiler-warning": True,
        "tests/fixtures/valid/telemetry-on-step-exit-summary": True,
    }
    expected_warnings = {
        "tests/fixtures/valid/model-tier-warnings": [
            "S1_IMPLEMENTER_MODEL_POSTURE",
            "S1_GATE_MODEL_TIER_WEAK",
            "S1_SOURCE_ANALYST_MODEL_TIER_WEAK",
            "S1_CRITIC_MODEL_TIER_WEAK",
        ],
    }
    failures: list[str] = []
    for rel, should_pass in cases.items():
        root = repo / rel
        errors, warnings = validate_run(load_run(root))
        passed = not errors
        status = "PASS" if passed else "FAIL"
        expected = "PASS" if should_pass else "FAIL"
        print(f"{rel}: {status} expected {expected}")
        for err in errors:
            print(f"  ERROR {err}")
        for warn in warnings:
            print(f"  WARN {warn}")
        if passed != should_pass:
            failures.append(rel)
            continue
        for expected_warning in expected_warnings.get(rel, []):
            if not any(expected_warning in warning for warning in warnings):
                print(f"  MISSING WARN {expected_warning}")
                failures.append(rel)
                break
    if failures:
        print("Self-test failed for: " + ", ".join(failures), file=sys.stderr)
        return 1
    print("Self-test passed.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate harness run artifacts.")
    parser.add_argument("run_path", nargs="?", help="Run workspace directory, runbook, or artifact file.")
    parser.add_argument("--stage", choices=["s1", "s2", "s3", "s7", "all"], default="all")
    parser.add_argument("--skip-telemetry", action="store_true", help="Skip telemetry declaration and JSONL checks.")
    parser.add_argument("--self-test", action="store_true", help="Run bundled regression fixtures.")
    args = parser.parse_args(argv)

    if args.self_test:
        return _run_self_tests(Path(__file__).resolve())
    if not args.run_path:
        parser.error("run_path is required unless --self-test is used")

    errors, warnings = validate_run(load_run(Path(args.run_path)), stage=args.stage, skip_telemetry=args.skip_telemetry)
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print("Harness run validation failed.")
        return 1
    print("Harness run validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
