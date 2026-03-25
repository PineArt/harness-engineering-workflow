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
- [ ] each role has a unique owner
- [ ] parallel tasks do not share the same writable area

## Quality Gates

### Gate Decision Rules

- `Pass`: all blocking gates pass, and any remaining gaps are minor documentation cleanup.
- `Conditional Pass`: no blocking gate fails, but at least one non-blocking gap must be closed in a named follow-up step.
- `Fail`: any blocking gate fails, any required artifact is missing, or the workflow relies on model self-certification for a material claim.

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

- `Return Step` may only target `S0` through `S7`
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
- if the only missing action is refreshed gate evidence, `Conditional Pass` may use `Return Step: S7`

### Source Fidelity

- [ ] facts can be traced to source material
- [ ] inference is labeled as inference
- [ ] uncertain items remain open rather than guessed

### Boundary Integrity

- [ ] roles are not overlapping excessively
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

Any of the following should trigger summary or subagent split:

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
