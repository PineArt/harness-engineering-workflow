# Artifact Registry

This file is the canonical source for minimum artifact schemas.
Other files may show short fill-in blocks, but field names and ownership should stay aligned with this registry.
If this file is unavailable during execution, `Orchestrator` restores it from version control before any owner redefines artifact fields elsewhere.

## Artifact Index

| Artifact | Owner | Step | Required In |
|---|---|---|---|
| `Task Brief` | `Orchestrator` | `S0` | `Lite`, `Full` |
| `Role Owner Table` | `Orchestrator` | `S1` | `Lite`, `Full` |
| `Run-Specific Responsibility Matrix` | `Orchestrator` | `S1` | `Lite`, `Full` |
| `Continuation Packet` | `Orchestrator` | `S0`, then checkpoint boundaries | `Lite`, `Full` |
| `Execution Environment Spec` | `Orchestrator` | `S1` | `Full` |
| `Context Pack` | `Orchestrator` | `S2` | `Lite`, `Full` |
| `Task Graph` | `Orchestrator` | `S3` | `Lite`, `Full` |
| `Workflow Draft` | `Workflow Designer` | `S3` | `Full` |
| `Execution Output Record` | task owner | `S4` | `Lite`, `Full` |
| `Runtime Evidence Record` | `Runtime Verifier` | `S4` | `Lite`, `Full` when state-surface validation is required |
| `Risk Register` | `Critic` | `S5` | `Lite`, `Full` |
| `Advisory Note` | `Advisor` | decision point | `Lite`, `Full` when `Advisor` is active |
| `Unified Draft` | `Orchestrator` | `S6` | `Full` |
| `Open Questions` | `Orchestrator` | `S6` | `Full` |
| `Integration Ledger` | `Orchestrator` | `S6` | `Lite`, `Full` |
| `Decision Log` | `Orchestrator` maintains; `Human Decision Maker` appends | `S0`, `S6`, `S7`, `S8` | `Lite`, `Full` |
| `Gate Decision` | `Quality Gate` | `S7` | `Lite`, `Full` |
| `Published Version` | `Template Editor` or publish owner | `S8` | `Full` |
| `Next Iteration Notes` | `Orchestrator` | `S8` | `Full` |
| `Run Telemetry` | `Orchestrator` | `S0` starts; `S8` closes | `Lite`, `Full` optional |
| `Run Profiler` | `Orchestrator` | `S8` | `Lite`, `Full` optional |

## Run Workspace Contract

`Run Workspace` is the durable place where process artifacts for one run are written.
It must also contain the recoverable continuation state for `Lite` and `Full` runs.

Owner:
`Orchestrator` owns `Run Workspace` declaration, accessibility validation, artifact index maintenance, equivalent-location approval, and step-closure enforcement for `Lite` and `Full`.
In `Ultra Lite`, the single `Owner` owns the `Preflight Judgment`.

Default path:

```text
exec-plans/active/YYYY-MM-DD-<slug>/
```

Continuation packet location:

```text
CURRENT.md
checkpoints/NNNN-S<step>.md
```

Default completion path:

```text
exec-plans/completed/YYYY-MM-DD-<slug>/
```

Minimum fields:

```text
Run ID:
Tier:
Created Before Step:
Active Path:
Completed Path:
Artifact Index:
Step Closure Gates:
Exception Paths:
Telemetry Mode:
Event Log Path:
Profiler Summary Path:
```

Rules:
- `Ultra Lite` does not require a durable `Run Workspace` by default, but the short goal/scope block and `Preflight Judgment` must exist before editing or execution starts.
- `Ultra Lite` `Preflight Judgment` must state whether the task is still Ultra Lite, why, the concrete validation path, whether that path is executable now, the validation-failure action, and whether to escalate before execution.
- `Lite` and `Full` runs must declare a `Run Workspace` immediately after tier selection and before `S0`.
- `Lite` and `Full` runs must declare `Telemetry Mode: Off | On`; `Off` is the valid default, and `On` must include an event log path.
- `Lite` and `Full` runs must create an append-only `Continuation Packet` before `S1` validation runs. `CURRENT.md` points to the latest file under `checkpoints/`.
- `Full` runs must also formalize the `Run Workspace` during `S1` in `Execution Environment Spec`.
- every required artifact for `S0`, `S1`, `S2`, and `S3` must be written and field-valid before the workflow enters the next step.
- `S1`, `S3`, `S5`, and `S7` close only after a fresh continuation checkpoint is written with an incremented `Checkpoint Seq`.
- Before and after delegated work that crosses a new independent `Context Boundary`, `Orchestrator` refreshes the continuation checkpoint or records why no refresh was needed.
- `S4` may assert that the earlier step-closure gates were satisfied, but it must not be the first point where missing pre-execution artifacts are discovered.
- exception paths must be declared in `Task Graph` `Writable Area`; in `Full`, also declare them in `Execution Environment Spec` `Artifact Locations`.

`Field-valid` means:
- all required fields from the relevant minimum schema are present
- required fields contain task-specific values rather than placeholders
- path fields are syntactically valid for the current workspace
- owner, artifact, action, and writable-area references agree with the current `Role Owner Table`, `Run-Specific Responsibility Matrix`, and `Task Graph`
- for `Lite` and `Full` S1 closure or S2 entry, `python scripts/validate_harness_run.py <run-workspace>` passes against the current run artifacts
- for `Lite` and `Full`, the latest continuation checkpoint is present, field-valid, points at the active run workspace, and is reachable through `CURRENT.md`

If field validation fails, the current step does not close.

## Responsibility Matrix

No concrete workflow action may remain ownerless. If a rule, fallback, validation, replay, publish action, or environment repair does not name a specific owner elsewhere, `Orchestrator` owns assigning one before the action starts.

The table below is the canonical default matrix. `Lite` and `Full` runs must also write a run-specific S1 mapping before `S2`.
The run-specific mapping must not duplicate the full canonical matrix. It records:
- whether canonical defaults apply
- phase-critical S6, S7, S8, gate, rework, re-gate, replay, publish, commit, submit, and check-in owner resolution
- any non-default owner override, with a brief reason
- any action that has no canonical default, which `Orchestrator` must assign before that action starts

| Action Area | Default Owner | Required Record |
|---|---|---|
| Fast Tier Check and initial tier choice | acting `Orchestrator`; in `Ultra Lite`, the single `Owner` until escalation | `Preflight Judgment` for `Ultra Lite`; `Decision Log` for `Lite` / `Full` |
| `Ultra Lite` goal/scope, preflight, execution, validation, retry, or escalation | single `Owner` | goal/scope block and `Preflight Judgment` |
| `Run Workspace`, artifact index, equivalent-location approval, and step-closure gates | `Orchestrator` | `Run Workspace` and `Decision Log` when a closure fails |
| Continuation packet checkpoints and `CURRENT.md` pointer refresh | `Orchestrator` | `Continuation Packet` |
| Role assignment, owner separation, and independent context-boundary requests | `Orchestrator` | `Role Owner Table` and `Task Graph` |
| Applying `External-Critic-Only Quality Gate Rule` | `Orchestrator` | `Role Owner Table` notes and `Decision Log` |
| Context packaging and context-overflow split decisions | `Orchestrator` | `Context Pack`, `Task Graph`, or `Decision Log` |
| Task execution and execution artifacts | assigned task owner | `Execution Output Record` |
| Real state-surface validation | `Runtime Verifier`; if absent, `Orchestrator` must assign one or record why not required | `Runtime Evidence Record` or `Decision Log` |
| Risk scan and revision requests | `Critic` | `Risk Register` |
| Advisory debate or option generation | `Advisor` | `Advisory Note` |
| Integration and conflict resolution | `Orchestrator` | `Integration Ledger` and `Decision Log` |
| Gate verdict, return step, rework owner, and re-gate owner fields | `Quality Gate` | `Gate Decision` |
| Gate-requested corrective work | `Rework Owner` named in `Gate Decision` | refreshed artifact from the return step |
| Re-gate after corrective work | `Re-gate Owner` named in `Gate Decision` | fresh `Gate Decision` |
| Replay coordination after `Fail` or `Conditional Pass` | `Orchestrator` | `Decision Log` and refreshed downstream artifacts |
| Missing `artifact-registry.md` or `checklists.md` restoration | `Orchestrator`; `Quality Gate` blocks gate progress until restored | `Decision Log` |
| Publish readiness verification | `Orchestrator` unless a publish owner is explicitly assigned | publish checklist and `Decision Log` |
| `Published Version` production | `Template Editor` or explicit publish owner | `Published Version` |
| Commit, check-in, or submit action after gate pass | explicit publish/check-in owner; otherwise `Orchestrator` for `Lite`, `Template Editor` or publish owner for `Full` | commit, submit, or publish evidence plus `Decision Log` |
| Final version freeze or human arbitration | `Human Decision Maker` when active; otherwise `Orchestrator` records the accepted decision | `Decision Log` |
| Moving or copying durable run records from `exec-plans/active/` to `exec-plans/completed/` | `Orchestrator` unless publish owner is assigned | `Decision Log` and preserved artifact index |

### Run-Specific Responsibility Matrix

```text
Canonical Defaults: Apply | Partially overridden | Not enough

Phase-Critical Action | Owner Resolution | Required Record | Override? | Notes
S6 integration closure | Orchestrator unless explicitly overridden | Integration Ledger and Decision Log | No |
S7 gate verdict | Quality Gate | Gate Decision | No |
S7 gate outcome append and replay coordination | Orchestrator | Decision Log and refreshed downstream artifacts | No |
Gate-requested rework | Rework Owner named in Gate Decision from an owner already allowed by this mapping | refreshed artifact from Return Step | Deferred field | Gate must name the owner when needed
Re-gate after corrective work | Re-gate Owner named in Gate Decision from an owner already allowed by this mapping | fresh Gate Decision | Deferred field | Gate must name the owner when needed
S8 publish readiness verification | Orchestrator unless explicit publish owner is assigned | publish checklist and Decision Log | No |
S8 publish, commit, check-in, or submit | explicit publish/check-in owner; otherwise Orchestrator for Lite, Template Editor or publish owner for Full published assets | Published Version, Decision Log, commit or publish evidence when applicable | No |

Explicit Overrides:
Action:
Owner:
Required Record:
Reason:
```

Field notes:
- `Canonical Defaults` is `Apply` only when every unlisted action uses the canonical default matrix above.
- `Phase-Critical Action` rows may use the default owner, but they must still be present so S6, S7, S8, gate, publish, commit, submit, and check-in responsibility is mechanically inspectable.
- `Owner Resolution` must resolve to a role or owner from the `Role Owner Table`, except for deferred `Gate Decision` fields that must later name `Rework Owner` or `Re-gate Owner`.
- `Override?` is `No`, `Yes`, or `Deferred field`.
- each `Explicit Overrides` entry needs a short reason; do not add reasons for default assignments.
- if the run cannot resolve a phase-critical action during S1, S1 does not close.

## Minimum Schemas

### `Continuation Packet`

`Continuation Packet` is the recovery baseline for auto compact, thread copy, or resumed execution. It is append-only:

```text
CURRENT.md
checkpoints/0001-S1.md
checkpoints/0002-S3.md
checkpoints/0003-S5.md
checkpoints/0004-S7.md
```

`CURRENT.md` must contain a run-workspace-relative pointer:

```text
Current Checkpoint: checkpoints/0001-S1.md
```

Each checkpoint file uses this schema:

```text
Run ID:
Active Run Workspace Path:
Current Step:
Last Completed Step:
Checkpoint Seq:
Last Updated:
Completed Checklist:
Remaining Checklist:
Inflight Delegations:
Next Action:
Blockers:
Evidence Pointers:
Context Pressure Signal:
```

Field notes:
- `Active Run Workspace Path` must identify the same run workspace being validated.
- `Checkpoint Seq` is a monotonically increasing integer across checkpoint files.
- `Last Updated` must include an ISO-like date.
- `Completed Checklist` and `Remaining Checklist` must make recovery possible without relying on a compacted chat summary.
- `Inflight Delegations` should use rows like `Owner | Context Boundary | Task | Expected Output | Due`; use `None` only when no delegated task is active.
- `Evidence Pointers` should include path plus locator, such as line number, heading anchor, artifact name, or commit SHA.
- `Context Pressure Signal` is warning-only telemetry for context pressure, auto compact, or overload risk.
- When a run flips from `Non-publish exploration` to `Publish`, the latest checkpoint must be refreshed under the current publish intent and must not carry prior exploration state as closure evidence.

### `Task Brief`

```text
Goal:
Non-goals:
Constraints:
Success Criteria:
Human Decision Points:
```

### Role Owner Table

```text
Publish Intent: Publish | Non-publish exploration | N/A
Boundary Status: Satisfied | Failed | Non-publish

Role | Owner | Context Boundary | Shared? | Notes
```

Field notes:
- `Publish Intent` is a run-level field, not a per-role column; `Lite` and `Full` must declare it before `S1` closes
- `Boundary Status` is a run-level field. For publishable `Lite` and `Full`, it may not be `Conditional`, deferred, provisional, or "must be fixed before publish"; use `Satisfied` only when all required owner/context separation is already established before `S1` closes, otherwise use `Failed` and stop or record `Non-publish`
- `Owner` names the accountable person, agent, or execution owner for that role; context labels alone do not satisfy ownership
- `Context Boundary` names the execution context used by the owner; this is the hard separation record for delegation
- Tool surfaces, protocols, credentials, hosts, paths, sessions, sandboxes, runtimes, and execution environments may describe `Context Boundary` or evidence, but they are not owners. `Owner` must identify the accountable executor that can accept the task, produce the required artifact, and be reassigned or replaced.
- `Shared?` is `Yes` or `No`
- within a run, one `Context Boundary` may map to only one `Owner`
- if multiple rows share one `Context Boundary`, they must also share the same `Owner`, and `Shared?` must be `Yes`
- record an `Agent ID` or mechanism-specific handle in `Notes` only when useful; it is optional and does not prove context independence

### `Execution Environment Spec`

```text
Directory Layout:
Artifact Locations:
Read Boundary:
Write Boundary:
Tool Surface:
Versioning Rule:
```

### `Context Pack`

```text
Core Context:
Optional Context:
Forbidden Scope:
Stable Prefix:
Required Tools:
```

### `Task Graph`

```text
Task:
Owner:
Context Boundary:
Depends On:
Outputs:
Writable Area:
Validation Checkpoint:
Fallback:
```

Field notes:
- when delegation is used, the `Owner` / `Context Boundary` pair must match an existing row in the `Role Owner Table`
- different role labels, tool calls, or spawns that remain within the same context do not satisfy this field
- every implementation node must be sliced to one behavior change or one tightly related file cluster; if one node needs multiple behavioral changes across unrelated areas, split it before `S4`
- every implementation node must include `Validation Checkpoint`, naming the cheapest external signal that can prove that slice, such as a focused test, typecheck, lint check, API/log probe, browser check, or runtime evidence record
- `Validation Checkpoint` is execution evidence for `S4` and later `S7`; it is not a second gate verdict and must not replace `Gate Decision`

### `Workflow Draft`

```text
Step:
Objective:
Inputs:
Method:
Outputs:
Acceptance:
Risks:
Escalation:
```

### `Execution Output Record`

```text
Objective
Inputs
Method
Outputs
Acceptance
Risks
Escalation
Fact / Inference / Open Question
```

Rules:
- `Outputs` must match the named artifact from `Task Graph`
- the record must be written only inside the task owner's `Writable Area`
- implementer self-validation is not sufficient by itself when correctness depends on pre-existing state

### `Runtime Evidence Record`

```text
State Surface:
Starting State:
Method:
Evidence:
Result:
Residual Risk:
Fact / Inference / Open Question
```

Field notes:
- `State Surface` names the real pre-existing state surface used for validation
- `Starting State` records the relevant observed state before the change or before the verification action
- `Evidence` should cite concrete runtime outputs such as test logs, screenshots, traces, responses, or database reads

### `Run Telemetry`

`Run Telemetry` is an optional append-only JSONL event stream for run-level profiler signals.
It records harness execution shape, not domain-specific skill failure taxonomies.
Skill-specific failure codes and recovery evidence belong to the owning skill, not this artifact.

Default path:

```text
<run-workspace>/telemetry.jsonl
```

Event fields:

```json
{
  "run_id": "",
  "ts": "",
  "event": "",
  "step": "",
  "owner": "",
  "active_ms": 0,
  "human_wait_ms": 0,
  "detail": {}
}
```

Allowed `event` values:
- `step_enter`
- `step_exit`
- `gate_verdict`
- `rework_requested`
- `compaction`
- `model_call`
- `human_wait_enter`
- `human_wait_exit`

Field notes:
- `run_id` must match the declared `Run Workspace` `Run ID`.
- `ts` is an ISO 8601 UTC timestamp.
- `step` is `preflight` or `S0` through `S8`.
- `owner` should match the current `Role Owner Table` when the event has an accountable owner; leave it empty only for run-level events with no single owner.
- `active_ms` and `human_wait_ms` use integer milliseconds.
- `active_ms` means agent reasoning time plus tool execution and tool wait time. I/O wait, model wait, browser wait, SSH wait, build wait, and test wait count as active time unless the run explicitly enters human wait.
- `human_wait_ms` means time blocked on human decision, manual input, external approval, or manual authentication. It is excluded from active time.
- `active_ms` and `human_wait_ms` should appear on `step_exit` and may appear on other duration-bearing events. Do not double count the same interval in both fields.
- `detail` is a small JSON object for event-local context. Keep it short, structured, and scrubbed of secrets.
- In the first version, `Orchestrator` may record only the events it can observe reliably. `step_enter`, `step_exit`, `gate_verdict`, `rework_requested`, and `human_wait_*` events are the preferred manual baseline. `model_call` and `compaction` may be omitted when the run cannot obtain them reliably.
- A `step_exit` duration is the duration for that specific step attempt. If a step re-enters after rework, `Run Profiler` accumulates repeated attempts under the same step and records the re-entry through `rework_count`.

`validate_harness_run.py` enforces that `Telemetry Mode` is explicitly declared.
`Telemetry Mode: Off` is valid by default.
When `Telemetry Mode` is `On`, the validator checks that the event path exists, the JSONL is parseable, required event fields are present, event and step values use the allowed enums, and a single record does not double count active and human-wait time.
If a single markdown file is validated instead of a run workspace directory, `Telemetry Mode: On` cannot use relative or `<run-workspace>/...` paths because the event log cannot be verified.
The validator scans the first 50,000 telemetry lines and warns if the scan is truncated.
`--skip-telemetry` is an escape hatch for non-publish historical audits or migration work; do not use it for publish/pass gate evidence.

### `Run Profiler`

`Run Profiler` is an optional S8 summary derived from `Run Telemetry`.
It summarizes run-level cost, latency, context pressure, rework, and gate outcomes.

Default path:

```text
<run-workspace>/profiler.json
```

Minimum fields:

```json
{
  "run_id": "",
  "tier": "",
  "per_step": {
    "S0": {
      "active_ms": 0,
      "human_wait_ms": 0,
      "model_calls": 0,
      "compactions": 0,
      "rework_count": 0
    }
  },
  "totals": {
    "active_ms": 0,
    "human_wait_ms": 0,
    "model_calls": 0,
    "compactions": 0,
    "rework_count": 0
  },
  "gate_outcomes": [],
  "notes": ""
}
```

Field notes:
- `per_step` keys should use `preflight` or `S0` through `S8`.
- repeated attempts for the same step are accumulated under that step.
- `totals` should sum the comparable values from `per_step`.
- `gate_outcomes` records each S7 verdict in order, including re-gates.
- `notes` captures concise S8 learning highlights and may cite improvement candidates, but it must not automatically edit a skill.
- summary tooling should be added only after real telemetry events exist and the event schema has stabilized across runs.

Enforcement boundary:
- Do not require telemetry collection by default; `Telemetry Mode: Off` remains a valid explicit choice.
- Do not require complete `model_call` or `compaction` coverage in the first version.
- Do not make `Run Profiler` field completeness a blocking quality gate until real telemetry events exist and the summary schema has stabilized across runs.

### `Risk Register`

```text
Risk Register:
- Risk:
  Severity:
  Evidence:
  Owner:
  Required Action:
  Status:
```

Entry fields:

```text
Risk:
Severity:
Evidence:
Owner:
Required Action:
Status:
```

`Status` may only be:
- `Open`
- `Mitigating`
- `Closed`

### `Advisory Note`

```text
Question:
Mode:
Position:
Recommendation:
Risks:
Open Questions:
```

Field notes:
- `Mode` may be `Strategy`, `Pro`, `Con`, `Option Generator`, or `Red Team`
- `Advisory Note` is input to decision-making, not a `Risk Register` or `Gate Decision`
- it may be produced before S1, S3, S5, or any other decision point where direction, debate, or option generation is useful
- multiple `Advisory Note` entries may exist for the same decision point

### `Unified Draft`

```text
Summary:
Integrated Artifacts:
Resolved Conflicts:
Outstanding Risks:
```

### `Open Questions`

```text
Question:
Why It Is Open:
Owner:
Next Step:
```

### `Integration Ledger`

```text
Agent:
Claim:
Artifact Name:
Owner:
Evidence Source:
Decision:
Next Step Or Fallback:
```

### `Decision Log`

```text
Decision:
Decision Owner:
Reason:
Affected Artifact:
Recorded At:
Next Step:
```

Record at least:
- human decisions
- conflict resolution
- gate-requested rework
- conditional-pass follow-up obligations
- final gate outcomes before rework or publish
- the gate outcome appended by `Orchestrator` after `S7`

### `Gate Decision`

```text
Gate:
Verdict:
Blocking:
Evidence:
Return Step:
Owner:
Rework Owner:
Re-gate Owner:
Re-gate Condition:
Re-gate Evidence:
Due Before:
```

Field rules:
- `Owner` is the gate reviewer owner
- `Rework Owner` is the owner who must execute the corrective action for `Fail` or `Conditional Pass`
- verdict-specific population rules and replay semantics are canonical in `checklists.md`
- before returning `Pass`, `Conditional Pass`, or any publish-readiness verdict, `Quality Gate` must cite a passing `validate_harness_run.py <run-workspace>` result or fail the gate

### `Next Iteration Notes`

```text
Observed Failure Pattern:
What Changed:
What To Reuse:
What To Tighten Next Time:
Telemetry Highlights:
```
