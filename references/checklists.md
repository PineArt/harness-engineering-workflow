# Checklists

This file is the canonical source for gate and checklist logic.
Other files should reference these gates by name instead of redefining them.

## Start Checklist

- [ ] `Goal` is singular and concrete
- [ ] `Non-goals` are explicit
- [ ] `Success Criteria` can be judged as pass/fail
- [ ] key knowledge is in repo or task artifacts
- [ ] `AGENTS.md` is short and navigational
- [ ] tools exist for diagnostics, testing, or runtime feedback
- [ ] `Ultra Lite` has a filled goal/scope block before execution, or the run has escalated
- [ ] `Ultra Lite` single `Owner` completed `Preflight Judgment` before execution, including validation path, executable-now status, validation-failure action, and escalation decision
- [ ] `Lite` and `Full` `Orchestrator` declared and validated a `Run Workspace` before `S0`
- [ ] `Lite` and `Full` `Orchestrator` enforced `S0`, `S1`, `S2`, and `S3` step-closure artifacts before the next step started
- [ ] any equivalent artifact location has an owner, is writable, accessible, and explicitly declared
- [ ] every concrete workflow action has an owner, using the `Responsibility Matrix` in `artifact-registry.md` when ownership is not otherwise explicit
- [ ] `Lite` and `Full` wrote a `Run-Specific Responsibility Matrix` during `S1` before `S2`
- [ ] S6, S7, S8, gate, rework, re-gate, replay, publish, commit, check-in, and submit actions resolve to owners through the S1 matrix or canonical defaults
- [ ] each role has an explicit owner
- [ ] any `Lite` workflow intended for publish uses separate accountable owners for `Orchestrator`, `Implementer`, and `Quality Gate`
- [ ] any `Lite` or `Full` workflow intended for publish records S1 boundary status as satisfied before `S2`; it is not conditional, deferred, provisional, or "must be fixed before publish"
- [ ] any `Full` workflow intended for publish uses at least 3 distinct owners
- [ ] any workflow intended for publish in a tier with separated owners is backed by the required independent context boundaries
- [ ] any publishable `Lite` or `Full` workflow that assigns `Critic` but not `Quality Gate` to an external context satisfies the `External-Critic-Only Quality Gate Rule`
- [ ] no required context boundary is assigned to more than one owner in the same run
- [ ] tool surfaces, protocols, credentials, hosts, paths, sessions, sandboxes, runtimes, and execution environments are not counted as independent accountable owners by themselves
- [ ] parallel tasks do not share the same writable area

## Quality Gates

### Gate Decision Rules

- `Pass`: all blocking gates pass, and any remaining gaps are minor documentation cleanup.
- `Conditional Pass`: no blocking gate fails, but at least one non-blocking gap must be closed in a named follow-up step.
- `Fail`: any blocking gate fails, any required artifact is missing, or the workflow relies on model self-certification for a material claim.
- Use `Fail` for any `Lite` or `Full` run if the required `Run Workspace` was not declared before `S0`, or if `S0` through `S3` step-closure artifacts were created only after the next step or task-specific execution had already started.
- Use `Fail` for any `Lite` or `Full` run if the `Run-Specific Responsibility Matrix` was not written during `S1` before `S2`, or if phase-critical S6, S7, S8, gate, rework, re-gate, replay, publish, commit, check-in, or submit ownership cannot be resolved from that matrix or the canonical defaults.
- Use `Fail` for any publishable `Lite` or `Full` run whose S1 boundary status is conditional, deferred, provisional, or depends on a later gate before it can become true.
- For `Lite` final publish, use `Fail` if publish intent was not declared before `S2`, if the workflow does not assign separate accountable owners to `Orchestrator`, `Implementer`, and `Quality Gate`, if the required independent context boundaries cannot be established before `S2`, or if the required owner separation exists only on paper without real context separation. These are fatal `Boundary Integrity` failures; tell the user final-result quality is uncontrollable.
- For `Full` final publish, use `Fail` if publish intent was not declared before `S2`, if the workflow has fewer than 3 distinct owners, if `Orchestrator` owns `Implementer` or `Quality Gate`, if `Implementer` shares an owner with `Critic` or `Quality Gate`, if the required independent context boundaries cannot be established before `S2`, or if the required owner separation exists only on paper without real context separation. These are fatal `Boundary Integrity` failures; tell the user final-result quality is uncontrollable.
- For any publishable `Lite` or `Full` workflow, use `Fail` if `Quality Gate` is not explicitly assigned or if it shares the implementation context boundary.
- Use `Fail` if a change depends on pre-existing state but the workflow does not validate against a real pre-existing state surface.

### External-Critic-Only Quality Gate Rule

When an external context such as Opus is assigned to `Critic` but not `Quality Gate` while the main context owns implementation:
- `Lite`: `Orchestrator` assigns `Quality Gate` to a separate independent context boundary.
- `Full`: `Orchestrator` assigns `Quality Gate` to a third independent context boundary.
- `Orchestrator` defaults to a local independent subagent when no separate gate owner is already available.

Missing this rule before implementation proceeds is a fatal `Boundary Integrity` failure owned by `Orchestrator`.

### Advisor Constraints

- `Advisor` is optional and advisory-only.
- `Advisor` can propose direction, trade-offs, debate positions, and options, but it does not satisfy `Critic` or `Quality Gate`.
- External `Advisor` output does not change publish-separation requirements.
- `Advisor` can own `Critic` or `Quality Gate` only when explicitly assigned to that role and producing that role's required artifact.

### Blocking Gates

- `Source Fidelity`
- `Boundary Integrity`
- `Execution Completeness`
- `External Feedback`

### Required Evidence Fields

- artifact name
- owner
- evidence source
- decision
- next step or fallback

### Gate Decision Schema

Gate Decision field names are canonical in `artifact-registry.md`.
This file is canonical for gate verdict rules and replay semantics.

### Return Step Rules

- `Return Step` may only target `S0` through `S6`
- `S7` is gate-only and is never a valid rework target
- `S8` is publish-only and is never a valid rework target
- ownership for rework, re-gate, and replay must resolve through the S1 `Run-Specific Responsibility Matrix`, the `Gate Decision` owner fields, or canonical defaults
- `Fail` must always include a `Return Step`
- `Fail` must include `Rework Owner`
- `Conditional Pass` must include `Return Step`, `Rework Owner`, `Re-gate Owner`, `Re-gate Condition`, `Re-gate Evidence`, and `Due Before`
- `Pass` should use `N/A` for `Return Step`, `Rework Owner`, and all re-gate fields
- `Fail` should use `N/A` for all re-gate fields except `Return Step` and `Rework Owner`

### Replay Rules

- after `Fail`, `Orchestrator` coordinates rerun from `Return Step` through every downstream required step until `S7`
- after `Conditional Pass`, `Rework Owner` completes the remediation, then `Orchestrator` coordinates rerun from `Return Step` through every downstream required step until `S7`
- `Orchestrator` ensures any artifact produced by the `Return Step` or a later step is refreshed before re-gate
- replay uses the existing S1 `Run-Specific Responsibility Matrix` unless `Orchestrator` explicitly updates it before re-entry to the return step
- a `Conditional Pass` remains open until a fresh `Pass` is recorded by a later `Gate Decision`
- `S8` may begin only when the latest `Gate Decision` verdict is `Pass`
- `Orchestrator` must not continue autonomous gate-triggered rework for the same unresolved issue beyond 2 cycles; after the second cycle, `Orchestrator` requires human arbitration or tier escalation before further execution

### Source Fidelity

- [ ] facts can be traced to source material
- [ ] inference is labeled as inference
- [ ] uncertain items remain open rather than guessed

### Boundary Integrity

- [ ] roles are not overlapping excessively
- [ ] `Lite` and `Full` declared a `Run Workspace` before `S0`
- [ ] `S0`, `S1`, `S2`, and `S3` step-closure gates succeeded before the next step began
- [ ] `Orchestrator` enforced step-closure gates and returned to the failed step on missing or field-invalid artifacts
- [ ] `Run-Specific Responsibility Matrix` was written during `S1`, before `S2`, and resolves phase-critical action owners
- [ ] every fallback, replay, restore, publish, escalation, and context-split action has an accountable owner
- [ ] single-owner `Lite` is treated as a fatal `Boundary Integrity` failure and does not proceed as a publish workflow
- [ ] publish intent or non-publish exploration was recorded before `S2` for any `Lite` or `Full` workflow
- [ ] publishable `Lite` and `Full` boundary status is `Satisfied` before `S2`, not `Conditional` or deferred to final gate
- [ ] `Quality Gate` is explicitly assigned for any publishable `Lite` or `Full` workflow
- [ ] `Quality Gate` uses an independent context boundary separate from the implementation context for any publishable `Lite` or `Full` workflow
- [ ] `Orchestrator` does not own `Implementer` or `Quality Gate` for any publishable `Lite` or `Full` workflow
- [ ] `Main Codex` using another execution surface is not counted as a distinct `Implementer` owner from `Main Codex` orchestration
- [ ] `Implementer` and `Quality Gate` have different owners for any publishable `Lite` workflow
- [ ] publishable `Lite` workflows are backed by at least 3 distinct independent context boundaries for `Orchestrator`, `Implementer`, and `Quality Gate`
- [ ] external `Critic` coverage without external `Quality Gate` coverage in publishable `Lite` satisfies the `External-Critic-Only Quality Gate Rule`; the general same-owner exception does not apply to this failure mode
- [ ] `Advisor` output is not counted as `Critic`, `Quality Gate`, or publish-separation evidence unless that owner is explicitly assigned to the role and produces the required artifact
- [ ] any shared `Context Boundary` rows also share the same `Owner`
- [ ] if `Critic` and `Quality Gate` share an owner, the role table notes explain why stronger separation is unnecessary
- [ ] publishable `Full` workflows use at least 3 distinct owners
- [ ] `Implementer`, `Critic`, and `Quality Gate` have different owners for any publishable `Full` workflow
- [ ] external `Critic` and external `Quality Gate` are recorded as separate accountable owners in publishable `Full`; if they are the same external owner, this fails `Boundary Integrity`
- [ ] `Quality Gate` does not share an owner with `Orchestrator` for any publishable `Full` workflow
- [ ] publishable `Full` workflows are backed by at least 3 distinct independent context boundaries
- [ ] external `Critic` coverage without external `Quality Gate` coverage in publishable `Full` satisfies the `External-Critic-Only Quality Gate Rule`
- [ ] every delegated task's `Owner` / `Context Boundary` pair matches the `Role Owner Table`
- [ ] no agent is silently making final human decisions
- [ ] write ownership is clear

### Execution Completeness

- [ ] the run has an artifact location contract appropriate to its tier
- [ ] `Ultra Lite` has the short goal/scope block and complete `Preflight Judgment` before execution, or has escalated to `Lite`
- [ ] `Lite` has `Run Workspace` before `S0`, `Task Brief` and initial `Decision Log` before `S1`, role owner table and run-specific responsibility matrix before `S2`, `Context Pack` before `S3`, and `Task Graph` before `S4`
- [ ] `Full` has `Run Workspace` before `S0`, `Task Brief` before `S1`, `Execution Environment Spec`, role owner table, and run-specific responsibility matrix before `S2`, `Context Pack` before `S3`, and `Task Graph` plus active `Workflow Draft` before `S4`
- [ ] each step has inputs
- [ ] each step has outputs
- [ ] each step has acceptance criteria
- [ ] each step has fallback or escalation
- [ ] each fallback or escalation names an owner or resolves to the `Responsibility Matrix`
- [ ] `Risk Register` exists before gate review
- [ ] an integration ledger exists with `agent / claim / artifact name / owner / evidence source / decision / next step or fallback`

### External Feedback

- [ ] important claims are checked with tools or runtime signals
- [ ] tests, logs, diagnostics, or UI checks are used where relevant
- [ ] any change that depends on pre-existing state is validated against a real pre-existing state surface
- [ ] implementer self-certification is not the only evidence when state-surface validation is required
- [ ] the workflow does not rely on model self-certification alone

### Reusability

- [ ] fixed skeleton and task-specific parameters are separated
- [ ] prompts are reusable
- [ ] artifact names and locations are consistent
- [ ] completed durable runs can be moved or copied from `exec-plans/active/` to `exec-plans/completed/` without losing the artifact index

### Entropy Control

- [ ] stable prefixes are not rewritten without need
- [ ] long history is summarized
- [ ] subagents are introduced before context overload
- [ ] drift cleanup is part of the workflow

### Context Overflow Triggers

Any of the following should trigger summary or subagent split.
These are secondary triggers; required publish-separation context splits should be introduced earlier when the run needs them:

- [ ] more than 3 unresolved open questions in one thread
- [ ] more than 2 failed revisions on the same step
- [ ] more than 4 upstream artifacts required to continue one task
- [ ] the active agent is re-reading long history instead of operating on a stable summary

`Orchestrator` owns detecting these triggers and assigning the summary or split owner.

## Anti-Patterns

- giant `AGENTS.md`
- knowledge trapped in chat tools
- one agent handling every phase of a long task
- humans doing all validation after AI coding
- weak or vague error messages
- no quality gate before merge or publish
- repeated prompt rewrites instead of stable system rules
