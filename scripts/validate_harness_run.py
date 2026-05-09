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


@dataclass
class RoleRow:
    role: str
    owner: str
    boundary: str
    shared: str = ""
    notes: str = ""


@dataclass
class RunArtifacts:
    root: Path
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


def _read_markdown(root: Path) -> str:
    if root.is_file():
        return f"\n\n<!-- FILE: {root.name} -->\n" + root.read_text(encoding="utf-8")
    if not root.exists():
        raise FileNotFoundError(root)
    parts: list[str] = []
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root).as_posix()
        parts.append(f"\n\n<!-- FILE: {rel} -->\n")
        parts.append(path.read_text(encoding="utf-8"))
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
        if role_key not in {"orchestrator", "implementer", "critic", "quality_gate"}:
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


def load_run(root: Path) -> RunArtifacts:
    text = _read_markdown(root)
    s1_text = _section(text, "S1")
    s7_text = _section(text, "S7")
    s8_text = _section(text, "S8")
    task_graph_text = _task_graph_text(text)
    return RunArtifacts(
        root=root,
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
    )


def _norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _canonical_owner(row: RoleRow) -> str:
    combined = " ".join([row.owner, row.boundary, row.notes])
    if CODEX_OWNER_RE.search(combined) or CURRENT_CONTEXT_RE.search(combined):
        return "main codex"
    return _norm(row.owner)


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

    required_roles = ["orchestrator", "implementer", "quality_gate"]
    for role in required_roles:
        if role not in run.roles:
            errors.append(f"S1_ROLE_MISSING: required role `{role}` is missing from S1.")
        elif not run.roles[role].owner:
            errors.append(f"S1_OWNER_MISSING: role `{role}` has no accountable owner.")

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
        task_rows = []
        current: dict[str, str] = {}
        table_headers: list[str] = []
        saw_task_graph_table = False
        in_fence = False
        for raw in run.task_graph_text.splitlines():
            line = raw.strip()
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

        if saw_task_graph_table and "validation checkpoint" not in table_headers and not any(
            "validation checkpoint" in row for row in task_rows
        ):
            errors.append("S3_TASK_GRAPH_CHECKPOINT_COLUMN_MISSING: Task Graph implementation table must include a Validation Checkpoint column.")
        for idx, row in enumerate(task_rows, start=1):
            if not row.get("owner", "").strip():
                warnings.append(f"S3_TASK_ROW_OWNER_MISSING: Task Graph row {idx} has no Owner field.")
            elif _role_key(row.get("owner", "")) not in {"orchestrator", "implementer", "critic", "quality_gate", "runtime_verifier", "advisor", "source_analyst", "workflow_designer", "template_editor", "human_decision_maker"}:
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
        "tests/fixtures/invalid/corpview-regression": False,
        "tests/fixtures/invalid/missing-intent-publish-s7": False,
        "tests/fixtures/invalid/nonpublish-publish-s7": False,
        "tests/fixtures/invalid/same-owner-alias": False,
        "tests/fixtures/invalid/tool-gate-boundary": False,
        "tests/fixtures/invalid/bad-boundary-status": False,
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
        "tests/fixtures/valid/telemetry-on-minimal": True,
        "tests/fixtures/valid/telemetry-on-profiler-warning": True,
        "tests/fixtures/valid/telemetry-on-step-exit-summary": True,
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
