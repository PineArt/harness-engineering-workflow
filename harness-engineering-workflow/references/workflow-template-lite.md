# Workflow Template Lite

This is a fill-in run sheet.
`Lite` is for medium-complexity work: one primary workflow, limited parallelism, and a fixed gate.
See [workflow-template.md](workflow-template.md) for the full principles, extended roles, and background.
See [agent-prompts.md](agent-prompts.md) for role prompts.
The canonical gate lives in [checklists.md](checklists.md).
The minimum artifact schemas live in [artifact-registry.md](artifact-registry.md).

Default first-run order:
- fill this file first
- open [artifact-registry.md](artifact-registry.md) before writing `Risk Register`, `Integration Ledger`, or `Decision Log`
- open [checklists.md](checklists.md) when you reach `Step S7`
- open [agent-prompts.md](agent-prompts.md) only when you need a prompt for a specific role

## Step S0. Task Brief

```text
Goal:

Non-goals:

Constraints:

Success Criteria:

Human Decision Points:
```

## Step S1. Role Set And Owners

`Lite` must assign at least these 4 responsibilities by default:

- `Orchestrator`
- `Implementer`
- `Critic`
- `Quality Gate`

Add these only when the task requires them:
- `Source Analyst`
- `Workflow Designer`
- `Human Decision Maker`
- `Principle Mapper`
- `Template Editor`

The role table must name an explicit owner:

```text
Role | Owner | Notes
Orchestrator |  |
Implementer |  |
Critic |  |
Quality Gate |  |
```

Notes:
- The same person or the same agent may hold multiple responsibilities.
- `Critic` and `Quality Gate` may not be omitted in this tier.
- If the work needs more than 4 independent owners, escalate directly to `Full`.

## Step S2. Context Pack

```text
Core Context:

Optional Context:

Forbidden Scope:

Stable Prefix:

Required Tools:
```

## Step S3. Task Graph

```text
Task:
Owner:
Depends On:
Outputs:
Writable Area:
Fallback:
```

At minimum, define:
- parallel blocks
- serial blocks
- one unique owner per task
- named `Outputs` and one unique `Writable Area`
- human decision points

## Step S4. Execute

Every execution role must produce:

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

Execution rules:
- Prefer tests, LSP, logs, browsers, deployment state, or other external feedback to establish facts.
- Write intermediate results only to each role's own area.
- `Outputs` must match the named artifact in `Task Graph`, and may be written only to that task's `Writable Area`.
- On failure, fall back only to the responsible step.

## Step S5. Risk Scan

Before the gate, `Critic` must produce:

```text
Risk Register:
- Risk:
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

See [artifact-registry.md](artifact-registry.md) for the full field definitions.

## Step S6. Integration Ledger And Decision Log

During integration, `Orchestrator` must maintain both `Integration Ledger` and `Decision Log`.
Do not collapse everything into one flattened unified draft.
After `S7`, `Orchestrator` must append the gate outcome to the same `Decision Log` before rework or publish.

`Integration Ledger`:

```text
Agent:
Claim:
Artifact Name:
Owner:
Evidence Source:
Decision:
Next Step Or Fallback:
```

`Decision Log`:

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
- gate-requested rework or conditional release

See [artifact-registry.md](artifact-registry.md) for the full field definitions.

## Step S7. Gate

`Quality Gate` must prefer the canonical rules in [checklists.md](checklists.md) and return one of:
- `Pass`
- `Conditional Pass`
- `Fail`

Blocking gates:
- `Source Fidelity`
- `Boundary Integrity`
- `Execution Completeness`
- `External Feedback`

Gate output must use the `Gate Decision` schema from [artifact-registry.md](artifact-registry.md).

Rules:
- `Return Step` may only be `S0` through `S7`.
- `S8` is the publish step and is never a valid rework target.
- `Fail` must include `Return Step` and `Rework Owner`.
- `Conditional Pass` must include `Return Step`, `Rework Owner`, `Re-gate Owner`, `Re-gate Condition`, `Re-gate Evidence`, and `Due Before`.
- `Pass` should set `Return Step`, `Rework Owner`, and all re-gate fields to `N/A`.
- Rework must rerun from `Return Step` through `S7`, and must refresh every artifact produced by that step and every downstream step.

If `checklists.md` is temporarily unavailable:
- restore that file from version control first
- do not invent gate conclusions from memory before it is restored
- use the minimum rules in this section only when the workflow must continue, and realign with the canonical checklist before publish

If [artifact-registry.md](artifact-registry.md) is temporarily unavailable:
- restore that file from version control first
- do not rewrite `Gate Decision` field names from memory before it is restored
- do not continue through the gate if it is still unavailable and there is no prior valid `Gate Decision` artifact to reuse

## Step S8. Publish

Before publish, at minimum have:

- [ ] `Task Brief`
- [ ] role owner table
- [ ] `Context Pack`
- [ ] `Task Graph`
- [ ] `Risk Register`
- [ ] `Integration Ledger`
- [ ] `Gate Decision`
- [ ] `Decision Log`

`Decision Log` is maintained by `Orchestrator` by default.
If `Human Decision Maker` exists, that role's final decision must be appended to the same `Decision Log`.
`Quality Gate` does not directly own `Decision Log`, but its `Gate Decision` must be appended to the same log by `Orchestrator` after `S7`.

## Context Control Rules

Summarize or split into a subagent if any of the following becomes true:
- more than 3 unresolved open questions
- more than 2 failed revisions on the same step
- continuing requires re-reading more than 4 upstream artifacts
- the current agent has started relying on long-history recall instead of a stable summary

## Escalate To Full If

Escalate to [workflow-template.md](workflow-template.md) if any of the following is true:
- the work needs more than 4 independent responsibilities
- more than 2 parallel workflows must converge at the same time
- `Template Editor` or `Principle Mapper` is required for the final delivery
- formal environment design or repo structure changes are required
- a risk item remains open for more than 2 rounds
- gate output starts depending on extensive human interpretation instead of a fixed schema
