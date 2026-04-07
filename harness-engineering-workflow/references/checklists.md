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
- [ ] each role has an explicit owner
- [ ] any `Lite` workflow intended for publish uses at least 2 distinct owners
- [ ] any `Full` workflow intended for publish uses at least 3 distinct owners
- [ ] any workflow intended for publish in a tier with separated owners is backed by the required distinct explicit UI-visible agent identifiers
- [ ] no delegated agent identifier is assigned to more than one owner in the same run
- [ ] parallel tasks do not share the same writable area

## Quality Gates

### Gate Decision Rules

- `Pass`: all blocking gates pass, and any remaining gaps are minor documentation cleanup.
- `Conditional Pass`: no blocking gate fails, but at least one non-blocking gap must be closed in a named follow-up step.
- `Fail`: any blocking gate fails, any required artifact is missing, or the workflow relies on model self-certification for a material claim.
- For `Lite` final publish, use `Fail` if the workflow has only 1 distinct owner, if `Implementer` also owns `Quality Gate`, if explicit UI-visible delegation is unavailable or not allowed, or if the required owner separation exists only on paper without distinct agent identifiers. These are fatal `Boundary Integrity` failures; tell the user final-result quality is uncontrollable.
- For `Full` final publish, use `Fail` if the workflow has fewer than 3 distinct owners, if `Implementer` shares an owner with `Critic` or `Quality Gate`, if `Quality Gate` also owns `Orchestrator`, if explicit UI-visible delegation is unavailable or not allowed, or if the required owner separation exists only on paper without distinct agent identifiers. These are fatal `Boundary Integrity` failures; tell the user final-result quality is uncontrollable.
- Use `Fail` if a change depends on pre-existing state but the workflow does not validate against a real pre-existing state surface.

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
- `Fail` must always include a `Return Step`
- `Fail` must include `Rework Owner`
- `Conditional Pass` must include `Return Step`, `Rework Owner`, `Re-gate Owner`, `Re-gate Condition`, `Re-gate Evidence`, and `Due Before`
- `Pass` should use `N/A` for `Return Step`, `Rework Owner`, and all re-gate fields
- `Fail` should use `N/A` for all re-gate fields except `Return Step` and `Rework Owner`

### Replay Rules

- after `Fail`, rerun from `Return Step` through every downstream required step until `S7`
- after `Conditional Pass`, complete the remediation owned by `Rework Owner`, then rerun from `Return Step` through every downstream required step until `S7`
- any artifact produced by the `Return Step` or a later step must be refreshed before re-gate
- a `Conditional Pass` remains open until a fresh `Pass` is recorded by a later `Gate Decision`
- `S8` may begin only when the latest `Gate Decision` verdict is `Pass`
- no workflow may continue autonomous gate-triggered rework for the same unresolved issue beyond 2 cycles; after the second cycle, require human arbitration or tier escalation before further execution

### Source Fidelity

- [ ] facts can be traced to source material
- [ ] inference is labeled as inference
- [ ] uncertain items remain open rather than guessed

### Boundary Integrity

- [ ] roles are not overlapping excessively
- [ ] single-owner `Lite` is treated as a fatal `Boundary Integrity` failure and does not proceed as a publish workflow
- [ ] `Implementer` and `Quality Gate` have different owners for any publishable `Lite` workflow
- [ ] publishable `Lite` workflows are backed by at least 2 distinct agent identifiers from explicit UI-visible subagents
- [ ] any shared `Agent ID` rows also share the same `Owner`
- [ ] if `Critic` and `Quality Gate` share an owner, the role table notes explain why stronger separation is unnecessary
- [ ] publishable `Full` workflows use at least 3 distinct owners
- [ ] `Implementer`, `Critic`, and `Quality Gate` have different owners for any publishable `Full` workflow
- [ ] `Quality Gate` does not share an owner with `Orchestrator` for any publishable `Full` workflow
- [ ] publishable `Full` workflows are backed by at least 3 distinct agent identifiers from explicit UI-visible subagents
- [ ] every delegated task's `Owner` / `Agent ID` pair matches the `Role Owner Table`
- [ ] no agent is silently making final human decisions
- [ ] write ownership is clear

### Execution Completeness

- [ ] each step has inputs
- [ ] each step has outputs
- [ ] each step has acceptance criteria
- [ ] each step has fallback or escalation
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

### Entropy Control

- [ ] stable prefixes are not rewritten without need
- [ ] long history is summarized
- [ ] subagents are introduced before context overload
- [ ] drift cleanup is part of the workflow

### Context Overflow Triggers

Any of the following should trigger summary or subagent split.
These are secondary triggers; required publish-separation subagents should be introduced earlier when explicit UI-visible delegation is available:

- [ ] more than 3 unresolved open questions in one thread
- [ ] more than 2 failed revisions on the same step
- [ ] more than 4 upstream artifacts required to continue one task
- [ ] the active agent is re-reading long history instead of operating on a stable summary

## Anti-Patterns

- giant `AGENTS.md`
- knowledge trapped in chat tools
- one agent handling every phase of a long task
- humans doing all validation after AI coding
- weak or vague error messages
- no quality gate before merge or publish
- repeated prompt rewrites instead of stable system rules
