# Artifact Registry

This file is the canonical source for minimum artifact schemas.
Other files may show short fill-in blocks, but field names and ownership should stay aligned with this registry.
If this file is unavailable during execution, restore it from version control before redefining artifact fields elsewhere.

## Artifact Index

| Artifact | Owner | Step | Required In |
|---|---|---|---|
| `Task Brief` | `Orchestrator` | `S0` | `Lite`, `Full` |
| `Role Owner Table` | `Orchestrator` | `S1` | `Lite`, `Full` |
| `Execution Environment Spec` | `Orchestrator` | `S1` | `Full` |
| `Context Pack` | `Orchestrator` | `S2` | `Lite`, `Full` |
| `Task Graph` | `Orchestrator` | `S3` | `Lite`, `Full` |
| `Workflow Draft` | `Workflow Designer` | `S3` | `Full` |
| `Execution Output Record` | task owner | `S4` | `Lite`, `Full` |
| `Runtime Evidence Record` | `Runtime Verifier` | `S4` | `Lite`, `Full` when state-surface validation is required |
| `Risk Register` | `Critic` | `S5` | `Lite`, `Full` |
| `Unified Draft` | `Orchestrator` | `S6` | `Full` |
| `Open Questions` | `Orchestrator` | `S6` | `Full` |
| `Integration Ledger` | `Orchestrator` | `S6` | `Lite`, `Full` |
| `Decision Log` | `Orchestrator` maintains; `Human Decision Maker` appends | `S0`, `S6`, `S7`, `S8` | `Lite`, `Full` |
| `Gate Decision` | `Quality Gate` | `S7` | `Lite`, `Full` |
| `Published Version` | `Template Editor` or publish owner | `S8` | `Full` |
| `Next Iteration Notes` | `Orchestrator` | `S8` | `Full` |

## Minimum Schemas

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
Role | Owner | Agent ID | Shared? | Notes
```

Field notes:
- `Agent ID` is the concrete delegated agent identifier from an explicit UI-visible subagent when delegation is used; otherwise use `N/A`
- `Shared?` is `Yes` or `No`
- within a run, one `Agent ID` may map to only one `Owner`
- if multiple rows share one `Agent ID`, they must also share the same `Owner`, and `Shared?` must be `Yes`

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
Agent ID:
Depends On:
Outputs:
Writable Area:
Fallback:
```

Field notes:
- when delegation is used, the `Owner` / `Agent ID` pair must match an existing row in the `Role Owner Table`
- hidden or background-only tool-driven delegation such as `spawn_agent` does not satisfy this `Agent ID` field

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

### `Next Iteration Notes`

```text
Observed Failure Pattern:
What Changed:
What To Reuse:
What To Tighten Next Time:
```
