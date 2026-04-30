# Workflow Template Lite

This is a fill-in run sheet.
`Lite` is for medium-complexity work: one primary workflow, limited parallelism, and a fixed gate.
See [workflow-template.md](workflow-template.md) for the full principles, extended roles, and background.
See [agent-prompts.md](agent-prompts.md) for role prompts.
The canonical gate lives in [checklists.md](checklists.md).
The minimum artifact schemas live in [artifact-registry.md](artifact-registry.md).
Concrete action ownership defaults live in the `Responsibility Matrix` in [artifact-registry.md](artifact-registry.md).

Default first-run order:
- fill this file first
- open [artifact-registry.md](artifact-registry.md) before writing `Risk Register`, `Integration Ledger`, or `Decision Log`
- use the `Responsibility Matrix` in [artifact-registry.md](artifact-registry.md) before starting any action whose owner is unclear
- open [checklists.md](checklists.md) when you reach `Step S7`
- open [agent-prompts.md](agent-prompts.md) only when you need a prompt for a specific role

## Step S0. Task Brief

`Orchestrator` owns this step, opens `Decision Log`, and owns `Run Workspace` setup here.
Before `S0`, declare a `Run Workspace`. Default path: `exec-plans/active/YYYY-MM-DD-<slug>/`.

```text
Goal:

Non-goals:

Constraints:

Success Criteria:

Human Decision Points:
```

`Run Workspace`:

```text
Run ID:
Tier: Lite
Created Before Step: S0
Active Path:
Completed Path:
Artifact Index:
Step Closure Gates:
Exception Paths:
```

Rules:
- the default active path is `exec-plans/active/YYYY-MM-DD-<slug>/`
- the default completed path is `exec-plans/completed/YYYY-MM-DD-<slug>/`
- `Orchestrator` owns workspace creation, accessibility validation, artifact index maintenance, and exception-path approval
- if the workspace cannot be created or declared, `Orchestrator` stops before `S0` and fixes the environment
- `S0` closes only when `Task Brief`, `Run Workspace`, and the initial `Decision Log` entry are written and field-valid
- `Orchestrator` enforces step-closure gates and must return to the failed step if an artifact is missing, incomplete, field-invalid, or written to an unvalidated equivalent location
- do not defer workspace declaration to `S4`, `S7`, or `S8`

## Step S1. Role Set And Owners

`Execution Environment Spec` is `Full`-only. Lite does not require that artifact unless the work is escalating.

`Lite` must assign at least these 4 responsibilities by default:

- `Orchestrator`
- `Implementer`
- `Critic`
- `Quality Gate`

Add these only when the task requires them:
- `Advisor`
- `Runtime Verifier`
- `Source Analyst`
- `Workflow Designer`
- `Human Decision Maker`
- `Principle Mapper`
- `Template Editor`

The role table must name an explicit owner and record the context boundary used by each owner. Agent IDs may be noted when useful, but they are not the hard separation rule:

```text
Role | Owner | Context Boundary | Shared? | Notes
Orchestrator |  |  |  |
Implementer |  |  |  |
Critic |  |  |  |
Quality Gate |  |  |  |
```

Notes:
- `Role`, `Owner`, and `Context Boundary` are not interchangeable.
- A `Lite` workflow intended to pass final gate and publish must use at least 2 distinct owners backed by at least 2 distinct independent context boundaries during `S1`, before `S4`.
- One `Context Boundary` may not back more than one `Owner` in the same run.
- Different role labels, tool calls, or spawns that remain within the same context do not satisfy this requirement.
- If the required independent context boundaries cannot be established, stop the run as a fatal `Boundary Integrity` failure. Do not relabel the same Lite run as exploration-only; tell the user final-result quality is uncontrollable until boundary separation is restored.
- Single-owner execution in `Lite` is a fatal `Boundary Integrity` failure.
- `Runtime Verifier` may be added in `Lite` without forcing immediate escalation when the workflow still centers on one primary implementation path.
- `Advisor` may be added in `Lite` for direction, debate, or option generation without satisfying `Critic` or `Quality Gate`.
- In a publishable `Lite` workflow, `Implementer` and `Quality Gate` may not share the same owner.
- In a publishable `Lite` workflow, `Quality Gate` must be explicitly assigned and must use an independent context boundary separate from the implementation context.
- If an external context is assigned to `Critic` but not `Quality Gate` and the main context owns implementation, apply the `External-Critic-Only Quality Gate Rule` from [checklists.md](checklists.md) during `S1`.
- `Critic` and `Quality Gate` may be combined only when they share the same owner and the notes record why stronger separation is unnecessary for this task; this exception does not apply under the `External-Critic-Only Quality Gate Rule`.
- `Critic` and `Quality Gate` may not be omitted in this tier.
- If the work needs 5 or more distinct workflow roles to have active ownership, excluding a single `Runtime Verifier` added only for state-surface validation, escalate directly to `Full`.

`Orchestrator` owns `S1` closure.
`S1` closes only when the role owner table is written to the declared `Run Workspace` or to an explicitly declared equivalent location and satisfies the boundary rules above.

## Step S2. Context Pack

```text
Core Context:

Optional Context:

Forbidden Scope:

Stable Prefix:

Required Tools:
```

`Orchestrator` owns `S2` closure.
`S2` closes only when `Context Pack` is written and field-valid.

## Step S3. Task Graph

```text
Task:
Owner:
Context Boundary:
Depends On:
Outputs:
Writable Area:
Fallback:
```

At minimum, define:
- parallel blocks
- serial blocks
- one unique owner per task
- one bound `Context Boundary` per delegated task
- delegated tasks only reuse a `Context Boundary` when they also reuse the same `Owner`
- named `Outputs` and one unique `Writable Area`
- human decision points

For `Lite`, the `Writable Area` for every task must be inside the declared `Run Workspace` unless an exception path is explicitly declared in both the `Run Workspace` and this `Task Graph`.

`Orchestrator` owns `S3` closure.
`S3` closes only when `Task Graph` is written and field-valid, including named `Outputs` and a unique `Writable Area` for every task.

## Execution Entry Assertion

`S4` is not the first artifact gate. It may begin only after the step-closure gates for `S0`, `S1`, `S2`, and `S3` have already succeeded.

If any pre-execution artifact is missing, malformed, or only drafted in memory, return to the owning step before task-specific execution. Do not defer missing pre-execution artifacts to `S7` or `S8`.

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
- Any change that depends on pre-existing state must be validated against a real pre-existing state surface by `Runtime Verifier`; if no verifier is active, `Orchestrator` must assign one or record why it is not required.
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
- `Orchestrator` restores that file from version control first
- do not invent gate conclusions from memory before it is restored
- `Quality Gate` may use the minimum rules in this section only when the workflow must continue, and `Orchestrator` must realign with the canonical checklist before publish

If [artifact-registry.md](artifact-registry.md) is temporarily unavailable:
- `Orchestrator` restores that file from version control first
- do not rewrite `Gate Decision` field names from memory before it is restored
- do not continue through the gate if it is still unavailable and there is no prior valid `Gate Decision` artifact to reuse

## Step S8. Publish

In `Lite`, `Orchestrator` is the default publish owner and verifies the required artifacts before publish unless another publish owner is assigned explicitly.
Single-owner `Lite` is a fatal `Boundary Integrity` failure. Do not publish; tell the user final-result quality is uncontrollable.
If the required independent context boundaries cannot be established for the run, or owner separation exists only on paper without real context separation, treat that as a fatal `Boundary Integrity` failure and stop.
Do not enter `S8` unless the latest `Gate Decision` verdict is `Pass`.

Before publish, at minimum have:

- [ ] declared `Run Workspace` before `S0`
- [ ] `Task Brief`
- [ ] role owner table
- [ ] at least 2 distinct role owners
- [ ] at least 2 distinct context boundaries backing those owners
- [ ] `Context Pack`
- [ ] `Task Graph`
- [ ] `Execution Output Record`
- [ ] `Runtime Evidence Record` when correctness depends on pre-existing state or independent dynamic validation
- [ ] `Risk Register`
- [ ] `Integration Ledger`
- [ ] `Gate Decision`
- [ ] the latest `Gate Decision` verdict is `Pass`
- [ ] `Decision Log`
- [ ] `S0`, `S1`, `S2`, and `S3` step-closure gates succeeded before the next step began

`Decision Log` is maintained by `Orchestrator` by default.
If `Human Decision Maker` exists, that role's final decision must be appended to the same `Decision Log`.
`Quality Gate` does not directly own `Decision Log`, but its `Gate Decision` must be appended to the same log by `Orchestrator` after `S7`.

## Context Control Rules

`Orchestrator` must summarize or split into a subagent if any of the following becomes true:
- more than 3 unresolved open questions
- more than 2 failed revisions on the same step
- continuing requires re-reading more than 4 upstream artifacts
- the current agent has started relying on long-history recall instead of a stable summary

`Orchestrator` owns detecting these triggers and assigning the summary or split owner.
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
