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
- `Agent ID` is the concrete delegated agent identifier when delegation is used; otherwise use `N/A`
- `Shared?` is `Yes` or `No`

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
- `Return Step` may only target `S0` to `S7`
- `S8` is publish-only and is never a valid rework target
- `Owner` is the gate reviewer owner
- `Rework Owner` is the owner who must execute the corrective action for `Fail` or `Conditional Pass`
- `Pass` must use `N/A` for `Return Step`, `Rework Owner`, and all re-gate fields
- `Fail` must include `Return Step` and `Rework Owner`, and should use `N/A` for all re-gate fields
- `Conditional Pass` must include `Return Step`, `Rework Owner`, and all re-gate fields
- for `Conditional Pass`, `Return Step` should point to the remediation step that must complete before re-gate; use `S7` only if the only missing action is refreshed gate evidence

### `Next Iteration Notes`

```text
Observed Failure Pattern:
What Changed:
What To Reuse:
What To Tighten Next Time:
```
