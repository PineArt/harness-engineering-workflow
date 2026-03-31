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

`Orchestrator` owns this step and opens `Decision Log` here.

```text
Goal:

Non-goals:

Constraints:

Success Criteria:

Human Decision Points:
```

## Step S1. Role Set And Owners

`Execution Environment Spec` is `Full`-only. Lite does not require that artifact unless the work is escalating.

`Lite` must assign at least these 4 responsibilities by default:

- `Orchestrator`
- `Implementer`
- `Critic`
- `Quality Gate`

Add these only when the task requires them:
- `Runtime Verifier`
- `Source Analyst`
- `Workflow Designer`
- `Human Decision Maker`
- `Principle Mapper`
- `Template Editor`

The role table must name an explicit owner. If explicit UI-visible delegation is available, it must also record the concrete agent identifier for each delegated owner:

```text
Role | Owner | Agent ID | Shared? | Notes
Orchestrator |  |  |  |
Implementer |  |  |  |
Critic |  |  |  |
Quality Gate |  |  |  |
```

Notes:
- `Role`, `Owner`, and `Agent ID` are not interchangeable.
- The same person or the same agent may hold multiple responsibilities during exploration, but that is not the default publish posture for `Lite`.
- A `Lite` workflow intended to pass final gate and publish must use at least 2 distinct owners.
- If explicit UI-visible delegation is available for a publishable `Lite` run, those 2 distinct owners must be backed by at least 2 distinct `Agent ID` values before `S4`.
- If explicit UI-visible delegation is available, one `Agent ID` may not back more than one `Owner` in the same run.
- Hidden or background-only tool-driven delegation such as `spawn_agent` does not satisfy the `Agent ID` requirement for this skill.
- If delegation is unavailable, the role table must mark the run exploration-only in `Notes`; distinct owner labels alone do not satisfy final `Boundary Integrity`.
- `Runtime Verifier` may be added in `Lite` without forcing immediate escalation when the workflow still centers on one primary implementation path.
- In a publishable `Lite` workflow, `Implementer` and `Quality Gate` may not share the same owner.
- `Critic` and `Quality Gate` may be combined only when the notes record why stronger separation is unnecessary for this task.
- `Critic` and `Quality Gate` may not be omitted in this tier.
- If the work needs 5 or more distinct workflow roles to have active ownership, excluding a single `Runtime Verifier` added only for state-surface validation, escalate directly to `Full`.

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
Agent ID:
Depends On:
Outputs:
Writable Area:
Fallback:
```

At minimum, define:
- parallel blocks
- serial blocks
- one unique owner per task
- one bound `Agent ID` from an explicit UI-visible subagent per delegated task
- delegated tasks only reuse an `Agent ID` when they also reuse the same `Owner`
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
- Any change that depends on pre-existing state must be validated against a real pre-existing state surface.
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

If `Runtime Verifier` is active, its `Runtime Evidence Record` should exist before `Critic` closes any state-dependent risk as `Closed`.

See [artifact-registry.md](artifact-registry.md) for the full field definitions.

## Step S6. Integration Ledger And Decision Log

During integration, `Orchestrator` must maintain both `Integration Ledger` and `Decision Log`.
Do not replace the ledger and decision log with one flattened summary that drops ownership or evidence fields.
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
- gate-requested rework or `Conditional Pass` follow-up

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
Gate verdict, field-population, and replay rules are canonical in [checklists.md](checklists.md).

Rules:
- return only `Pass`, `Conditional Pass`, or `Fail`
- follow the canonical gate verdict, field-population, and replay rules from [checklists.md](checklists.md)

If `checklists.md` is temporarily unavailable:
- restore that file from version control first
- do not invent gate conclusions from memory before it is restored
- use the minimum rules in this section only when the workflow must continue, and realign with the canonical checklist before publish

If [artifact-registry.md](artifact-registry.md) is temporarily unavailable:
- restore that file from version control first
- do not rewrite `Gate Decision` field names from memory before it is restored
- do not continue through the gate if it is still unavailable and there is no prior valid `Gate Decision` artifact to reuse

## Step S8. Publish

In `Lite`, `Orchestrator` is the default publish owner and verifies the required artifacts before publish unless another publish owner is assigned explicitly.
Single-owner `Lite` is exploration-only. It may produce drafts and intermediate artifacts, but it may not satisfy final `Boundary Integrity` for publish.
If explicit UI-visible delegation was available for the run, paper-only owner separation is also exploration-only; final publish requires the role table and task graph to point to real delegated `Agent ID` values from explicit UI-visible subagents.
Do not enter `S8` unless the latest `Gate Decision` verdict is `Pass`.

Before publish, at minimum have:

- [ ] `Task Brief`
- [ ] role owner table
- [ ] at least 2 distinct role owners
- [ ] if explicit UI-visible delegation was available, at least 2 distinct delegated `Agent ID` values backing those owners
- [ ] `Context Pack`
- [ ] `Task Graph`
- [ ] `Execution Output Record`
- [ ] `Runtime Evidence Record` when correctness depends on pre-existing state or independent dynamic validation
- [ ] `Risk Register`
- [ ] `Integration Ledger`
- [ ] `Gate Decision`
- [ ] the latest `Gate Decision` verdict is `Pass`
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

Do not wait for context overload to create the minimum publish-separation subagents. In `Lite`, that separation is an entry requirement for publishable delegated runs, not only an overload response.

## Escalate To Full If

Escalate to [workflow-template.md](workflow-template.md) if any of the following is true:
- the work needs 5 or more distinct workflow roles to have active ownership, excluding a single `Runtime Verifier` added only for state-surface validation
- more than 1 parallel workflow must converge at the same time
- `Template Editor` or `Principle Mapper` is required for the final delivery
- formal environment design or repo structure changes are required
- a risk item remains open for more than 2 rounds
- gate output starts depending on extensive human interpretation instead of a fixed schema

This section describes escalation conditions after work has started. For the initial selection shortcut, use `Fast Tier Check` in `SKILL.md`.
