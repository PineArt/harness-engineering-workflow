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
Continuation Current: CURRENT.md
Checkpoint Directory: checkpoints/
```

`Telemetry`:

```text
Telemetry Mode: Off | On
Event Log Path: <run-workspace>/telemetry.jsonl
Profiler Summary Path: <run-workspace>/profiler.json
Timing Semantics: Use the `Run Telemetry` timing rules in artifact-registry.md
```

Rules:
- the default active path is `exec-plans/active/YYYY-MM-DD-<slug>/`
- the default completed path is `exec-plans/completed/YYYY-MM-DD-<slug>/`
- `Orchestrator` owns workspace creation, accessibility validation, artifact index maintenance, and exception-path approval
- `Telemetry Mode: Off` is valid by default; when `On`, use the optional `Run Telemetry` and `Run Profiler` schemas in [artifact-registry.md](artifact-registry.md)
- `validate_harness_run.py` requires a `Telemetry Mode` declaration; `Telemetry Mode: On` also validates the event log path and basic JSONL structure
- `Orchestrator` creates `CURRENT.md` and the first append-only checkpoint under `checkpoints/` before S1 validation runs; the canonical schema is `Continuation Packet` in [artifact-registry.md](artifact-registry.md)
- if the workspace cannot be created or declared, `Orchestrator` stops before `S0` and fixes the environment
- `S0` closes only when `Task Brief`, `Run Workspace`, and the initial `Decision Log` entry are written and field-valid
- if the run imports or continues from prior non-publish exploration, `S0` closure must record the imported material as evidence or context only, and the `Task Brief` must state the current run's publish goal and scope independently
- `Orchestrator` enforces step-closure gates and must return to the failed step if an artifact is missing, incomplete, field-invalid, or written to an unvalidated equivalent location
- after auto compact, thread copy, or resume, `Orchestrator` reads `CURRENT.md`, opens the latest checkpoint, re-runs the validator, and then continues from the remaining checklist
- do not infer completion from a compacted summary; re-check upload, restart, live verify, scoped commit, and publish record when those items are in scope
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
- `Publish Worker`
- `Source Analyst`
- `Workflow Designer`
- `Human Decision Maker`
- `Principle Mapper`
- `Template Editor`

The role table must name an explicit owner and record the context boundary used by each owner. Agent IDs may be noted when useful, but they are not the hard separation rule:

```text
Publish Intent: Publish | Non-publish exploration | N/A
Boundary Status: Satisfied | Failed | Non-publish

Role | Owner | Context Boundary | Shared? | Notes
Orchestrator |  |  |  |
Implementer |  |  |  |
Critic |  |  |  |
Quality Gate |  |  |  |
```

Notes:
- `Role`, `Owner`, and `Context Boundary` are not interchangeable.
- For publishable `Lite`, `Boundary Status` may not be `Conditional`, deferred, provisional, or "must be fixed before publish"; S1 either satisfies the boundary before S2 or stops.
- A publishable `Lite` run that imports prior non-publish exploration must enter `S1` with no inherited `Boundary Status`, `Gate Decision`, or publish-readiness claim; archive or cite those prior records only as evidence, then record the current run's status independently.
- Tool surfaces, protocols, credentials, hosts, paths, sessions, sandboxes, runtimes, and execution environments are not separate owners by themselves; `Main Codex` using any execution surface is still `Main Codex` unless a different accountable executor is assigned.
- A `Lite` workflow must declare publish intent or record itself as non-publish exploration during `S1`, before `S2`.
- A `Lite` workflow intended to pass final gate and publish must assign `Orchestrator`, `Implementer`, and `Quality Gate` to explicit accountable owners backed by at least 3 distinct independent context boundaries during `S1`, before `S2`.
- One `Context Boundary` may not back more than one `Owner` in the same run.
- Different role labels, tool calls, or spawns that remain within the same context do not satisfy this requirement.
- If the required independent context boundaries cannot be established, stop the run as a fatal `Boundary Integrity` failure. Do not relabel the same Lite run as exploration-only; tell the user final-result quality is uncontrollable until boundary separation is restored.
- Single-owner execution in `Lite` is a fatal `Boundary Integrity` failure.
- `Runtime Verifier` may be added in `Lite` without forcing immediate escalation when the workflow still centers on one primary implementation path.
- `Advisor` may be added in `Lite` for direction, debate, or option generation without satisfying `Implementer`, `Critic`, or `Quality Gate`; do not reuse the same accountable owner for `Advisor` and those phase-critical roles.
- In a publishable `Lite` workflow, `Orchestrator` may not own `Implementer` or `Quality Gate`.
- In a publishable `Lite` workflow, `Implementer` and `Quality Gate` may not share the same owner.
- In a publishable `Lite` workflow, `Quality Gate` must be explicitly assigned and must use an independent context boundary separate from the implementation context.
- If an external context is assigned to `Critic` but not `Quality Gate` and the main context owns implementation, apply the `External-Critic-Only Quality Gate Rule` from [checklists.md](checklists.md) during `S1`.
- `Critic` and `Quality Gate` may be combined only when they share the same owner and the notes record why stronger separation is unnecessary for this task; this exception does not apply under the `External-Critic-Only Quality Gate Rule`.
- `Critic` and `Quality Gate` may not be omitted in this tier.
- If the work needs 5 or more distinct workflow roles to have active ownership, excluding a single `Runtime Verifier` added only for state-surface validation, escalate directly to `Full`.

`Run-Specific Responsibility Matrix`:

```text
Canonical Defaults: Apply | Partially overridden | Not enough

Phase-Critical Action | Owner Resolution | Required Record | Override? | Notes
S6 integration closure | Orchestrator unless explicitly overridden | Integration Ledger and Decision Log | No |
S7 gate verdict | Quality Gate | Gate Decision | No |
S7 gate outcome append and replay coordination | Orchestrator | Decision Log and refreshed downstream artifacts | No |
Gate-requested rework | Rework Owner named in Gate Decision from an owner allowed by this mapping | refreshed artifact from Return Step | Deferred field |
Re-gate after corrective work | Re-gate Owner named in Gate Decision from an owner allowed by this mapping | fresh Gate Decision | Deferred field |
S8 publish readiness verification | Orchestrator unless explicit publish owner is assigned | publish checklist and Decision Log | No |
S8 publish, commit, submit, or check-in | explicit publish/check-in owner, otherwise Orchestrator | Published Version, Decision Log, commit or publish evidence when applicable | No |

Explicit Overrides:
Action:
Owner:
Required Record:
Reason:
```

Notes:
- Do not copy the full canonical matrix into every run. List default confirmation, phase-critical actions, and explicit overrides only.
- Phase-critical actions must resolve to the role table or to a deferred `Gate Decision` owner field before S1 closes.
- If `Main Codex` owns implementation, changing the execution surface does not satisfy independent implementer ownership.
- If `Critic` and `Quality Gate` are both assigned to an external model family, identify whether they are the same accountable owner or independent review/gate owners. For high-risk publish work, prefer separate critic and gate owners; if they are combined in Lite, record why stronger separation is unnecessary.

`Orchestrator` owns `S1` closure.
`S1` closes only when the role owner table and run-specific responsibility matrix are written to the declared `Run Workspace` or to an explicitly declared equivalent location, declares publish intent, resolves phase-critical S6/S7/S8 ownership, and satisfies the boundary rules above.
`S1` closes only after `Orchestrator` writes a fresh continuation checkpoint with an incremented `Checkpoint Seq` and updates `CURRENT.md`.
`S1` also closes only after `Orchestrator` runs `python scripts/validate_harness_run.py <run-workspace>` from the skill root, or the equivalent installed script path, and records a passing result. A failed result returns the workflow to `S1` and blocks `S2`.
For a publishable run that imports prior non-publish exploration, `S1` also closes only after `Orchestrator` verifies that the role table and responsibility matrix do not inherit prior `Boundary Status`, `Gate Decision`, or publish-readiness records.
For a publishable run that imports prior non-publish exploration, `S1` also refreshes the latest continuation checkpoint under current `Publish` intent.
Do not enter `S2` until publish intent, accountable owners, required independent context boundaries, and phase-critical action owners are established.
If a publishable `Lite` run cannot assign `Orchestrator`, `Implementer`, and `Quality Gate` to separate accountable owners on independent context boundaries, stop before `S2`, re-scope to qualifying `Ultra Lite`, or explicitly record the run as non-publish exploration before continuing.

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
For a publishable run that imports prior non-publish exploration, `S2` closes only when the `Context Pack` labels imported exploration material as evidence or context and refreshes current-run constraints, owner boundaries, and validation surfaces under `Publish` intent.

## Step S3. Task Graph

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

At minimum, define:
- parallel blocks
- serial blocks
- one unique owner per task
- one bound `Context Boundary` per delegated task
- delegated tasks only reuse a `Context Boundary` when they also reuse the same `Owner`
- named `Outputs` and one unique `Writable Area`
- implementation tasks sliced to one behavior change or one tightly related file cluster
- one `Validation Checkpoint` per implementation task, naming the external signal that proves that slice
- human decision points

For `Lite`, the `Writable Area` for every task must be inside the declared `Run Workspace` unless an exception path is explicitly declared in both the `Run Workspace` and this `Task Graph`.

`Orchestrator` owns `S3` closure.
`S3` closes only when `Task Graph` is written and field-valid, including named `Outputs`, a unique `Writable Area` for every task, and `Validation Checkpoint` for every implementation task.
If one implementation task would require multiple behavior changes across unrelated areas, `Orchestrator` splits it before `S3` closes instead of relying on `Implementer` to subdivide it during `S4`.
`S3` closes only after `Orchestrator` writes a fresh continuation checkpoint with an incremented `Checkpoint Seq` and updates `CURRENT.md`.
For a publishable run that imports prior non-publish exploration, `S3` closes only when the `Task Graph` is refreshed for the current `Publish` intent and does not reuse an exploration task graph as proof of owner separation, gate coverage, or publish readiness.

## Execution Entry Assertion

`S4` is not the first artifact gate. It may begin only after the step-closure gates for `S0`, `S1`, `S2`, and `S3` have already succeeded.

If any pre-execution artifact is missing, malformed, or only drafted in memory, return to the owning step before task-specific execution. Do not defer missing pre-execution artifacts to `S7` or `S8`.
If the S1 validator was not run successfully, return to `S1`; `S4` and `S7` may not be the first place this is discovered.

If a publishable run imports prior non-publish exploration, do not enter `S4` until `S0`, `S1`, `S2`, and `S3` have been re-closed under current `Publish` intent. Prior exploration `Boundary Status`, `Gate Decision`, publish-readiness claims, `Context Pack`, or `Task Graph` records do not satisfy this entry assertion.

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
- Do not enter `S4` if the `Task Graph` is missing, stale, or contradicts the `S1` publish-intent or owner-separation record; return to `S1` or `S3` before execution.
- Prefer tests, LSP, logs, browsers, deployment state, or other external feedback to establish facts.
- Any change that depends on pre-existing state must be validated against a real pre-existing state surface by `Runtime Verifier`; if no verifier is active, `Orchestrator` must assign one or record why it is not required.
- Write intermediate results only to each role's own area.
- `Outputs` must match the named artifact in `Task Graph`, and may be written only to that task's `Writable Area`.
- For implementation tasks, execute the `Task Graph` slice as assigned. Do not fuse adjacent slices unless `Orchestrator` first refreshes `S3`.
- Record the result of the task's `Validation Checkpoint` in the execution output or runtime evidence.
- Mainline context should hold decisions and pointers only; long tool output, grep/read dumps, traces, screenshots, and model transcripts belong in run-workspace artifacts referenced by path and locator.
- Before and after delegated work that crosses a new independent `Context Boundary`, refresh the continuation checkpoint or record why no refresh was needed.
- Treat context pressure, auto compact, or repeated long-history rereads as a signal to checkpoint early and split work.
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
`S5` closes only after `Orchestrator` writes a fresh continuation checkpoint with an incremented `Checkpoint Seq` and updates `CURRENT.md`.

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
- before returning `Pass`, `Conditional Pass`, guarded-publish, or any publish-readiness verdict, run `python scripts/validate_harness_run.py <run-workspace>` and cite the passing result in the `Gate Decision`; if it fails or was not run, return `Fail` to `S1`
- before returning any gate verdict, verify that the latest continuation checkpoint is fresh for `S7`; if it is missing or stale, return `Fail` to the owning checkpoint step

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
When `S1` assigns a `Publish Worker` or another explicit publish/check-in owner, `Orchestrator` integrates that owner's `Publish Output Record` and does not execute the assigned upload, restart, scoped commit, check-in, submit, or remote status-confirmation steps itself.
Single-owner `Lite` is a fatal `Boundary Integrity` failure. Do not publish; tell the user final-result quality is uncontrollable.
If the required independent context boundaries cannot be established for the run, or owner separation exists only on paper without real context separation, treat that as a fatal `Boundary Integrity` failure and stop.
Do not enter `S8` unless the latest `Gate Decision` verdict is `Pass`.

Before publish, at minimum have:

- [ ] declared `Run Workspace` before `S0`
- [ ] `Task Brief`
- [ ] role owner table
- [ ] run-specific responsibility matrix resolving S6, S7, S8, gate, rework, re-gate, replay, publish, commit, check-in, and submit owners
- [ ] publish intent or non-publish exploration recorded before `S2`
- [ ] publishable runs have separate accountable owners for `Orchestrator`, `Implementer`, and `Quality Gate`
- [ ] publishable runs have at least 3 distinct context boundaries backing those owners
- [ ] tool surfaces, protocols, credentials, hosts, paths, sessions, sandboxes, runtimes, and execution environments were not counted as independent accountable owners by themselves
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
- [ ] `validate_harness_run.py <run-workspace>` passed at `S1` closure / `S2` entry and again before the `S7` verdict
- [ ] `CURRENT.md` points to the latest append-only continuation checkpoint, and checkpoints exist for `S1`, `S3`, `S5`, and `S7` when those steps have been reached

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
When a trigger fires, write a continuation checkpoint before splitting or summarizing so the mainline can recover through pointers rather than a chat summary.

## Escalate To Full If

Escalate to [workflow-template.md](workflow-template.md) if any of the following is true:
- the work needs 5 or more distinct workflow roles to have active ownership, excluding a single `Runtime Verifier` added only for state-surface validation
- more than 1 parallel workflow must converge at the same time
- `Template Editor` or `Principle Mapper` is required for the final delivery
- formal environment design or repo structure changes are required
- a risk item remains open for more than 2 rounds
- gate output starts depending on extensive human interpretation instead of a fixed schema

This section describes escalation conditions after work has started. For the initial selection shortcut, use `Fast Tier Check` in `SKILL.md`.
