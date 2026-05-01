---
name: harness-engineering-workflow
description: "Use when the task needs a reusable execution workflow with explicit owners, repo-backed artifacts, role-scoped context packs, structured risk review, gate decisions, or environment-first coordination across one or more agents. Start with Fast Tier Check to choose Ultra Lite, Lite, or Full. Do not use for plain one-off coding that does not need workflow artifacts, validation surfaces, or repeatable operating rules."
---

# Harness Engineering Workflow

Use this skill when the user needs a repeatable workflow or run sheet that is explicitly:
- environment-first rather than prompt-first
- grounded in repo-as-record-system and progressive context
- enforced by mechanical checks, quality gates, and result acceptance
- intended to scale beyond a one-off chat reply

Do not use this skill for:
- one-off casual brainstorming with no workflow output
- pure code implementation requests that do not need workflow artifacts or gate logic
- generic "use several agents" requests that do not need this operating model
- tasks where there is no stable workspace, no artifacts, and no validation surface

## Start Small

For `Ultra Lite`, a single `Implementer` owner is usually enough.

For `Lite`, start with these 4 roles:
- `Orchestrator`
- `Implementer`
- `Critic`
- `Quality Gate`

Only add more roles such as `Advisor`, `Runtime Verifier`, `Source Analyst`, `Workflow Designer`, or `Human Decision Maker` when the task actually needs them.

Do not default to the full role set on small tasks.

## Execution Policy

Treat `role`, `owner`, and `subagent` as different things:
- `Role`: the responsibility
- `Owner`: the accountable executor for that responsibility
- `Subagent`: the concrete delegated execution slot, but for this skill delegation counts only when execution crosses an independent context boundary
- Tool surfaces, protocols, credentials, hosts, paths, sessions, sandboxes, runtimes, and execution environments are not independent accountable owners by themselves. They may identify `Context Boundary` or evidence, but `Owner` must identify the accountable executor that can accept the task, produce the required artifact, and be reassigned or replaced.

Default execution posture:
- `Ultra Lite`: the single `Owner` stays single-owner unless boundaries are unclear
- `Lite`: `Orchestrator` establishes at least 3 distinct independent context boundaries for `Orchestrator`, `Implementer`, and `Quality Gate` when role owners are assigned if the run is intended for final publish
- `Full`: `Orchestrator` establishes at least 3 distinct independent context boundaries when role owners are assigned and before `S2` if the run is intended for final publish
- `Lite` or `Full`: `Orchestrator` applies the `External-Critic-Only Quality Gate Rule` from [references/checklists.md](references/checklists.md) if an external context covers `Critic` but not `Quality Gate` while the main context owns implementation
- if a tier requires separated owners and the run cannot establish the required independent context boundaries, `Orchestrator` stops as a fatal `Boundary Integrity` failure and tells the user final-result quality is uncontrollable
- different role labels, tool calls, or spawns that remain within the same context do not satisfy this requirement

Do not treat distinct role names by themselves as proof of distinct execution ownership.
Do not treat `Advisor` output as `Critic` or `Quality Gate` output unless that owner is explicitly assigned to the role and produces the required artifact.
Before `S1` closes and before `S2` begins, `Orchestrator` must declare whether a `Lite` or `Full` run is intended for publish or is non-publish exploration.
If a `Lite` or `Full` run imports or continues from non-publish exploration, `S0` closure must record the imported exploration material as evidence or context only, and `S0` through `S3` must re-close under the current `Publish` intent. A publishable run may not inherit `Boundary Status`, `Gate Decision`, or publish-readiness claims from non-publish exploration; it must establish its own publish goal, owner boundaries, gate path, and publish readiness in the current run.
For publishable `Lite` and `Full`, `S1` boundary status may not be `Conditional`, deferred, provisional, or "must be fixed before publish"; it is either satisfied before `S2` or the run stops before downstream work.
For publishable `Lite` and `Full`, `Orchestrator` must not own `Implementer` or `Quality Gate`.
For publishable `Lite` and `Full`, `Quality Gate` must be explicitly assigned and must use an independent context boundary separate from the implementation context.
If publish intent, accountable owners, or required independent context boundaries cannot be established before `S2`, stop before task-specific downstream work starts, re-scope to qualifying `Ultra Lite`, or explicitly record the run as non-publish exploration.
`Orchestrator` records context boundaries in the role table and task graph whenever delegated work is used.
`Orchestrator` must not defer missing publish-separation boundaries to final review; create or request the missing independent context before `S2`.
Agent identifiers may be recorded when available, but they are supporting evidence only and do not prove context independence.
Before any concrete workflow action starts, it must have an accountable owner. Use the `Responsibility Matrix` in [references/artifact-registry.md](references/artifact-registry.md) whenever ownership is unclear.
For `Lite` and `Full`, `S1` must include both a `Role Owner Table` and a `Run-Specific Responsibility Matrix`; the role table records role/context boundaries, while the run-specific matrix resolves concrete action ownership.
The run-specific matrix must not duplicate the full canonical matrix. It must make S6, S7, S8, gate, rework, re-gate, replay, publish, commit, submit, and check-in ownership mechanically inspectable, and it must list any non-default owner override with a brief reason.
If a phase-critical action cannot resolve to the S1 mapping or to a canonical default before `S2`, `Orchestrator` stops before task-specific downstream work starts.

Run workspace posture:
- `Ultra Lite`: the single `Owner` completes a `Preflight Judgment` before changing files or executing task-specific actions. It must state whether the task is still Ultra Lite, why, the concrete validation path, whether that path is executable now, the validation-failure action, and whether to escalate before execution. The judgment may live inline in the current response or in a repo-backed note. Escalate before execution if the work needs durable process records, multiple owners, a formal gate, or more than one validation path.
- `Lite`: `Orchestrator` establishes, declares, and validates a `Run Workspace` immediately after tier selection and before `S0`. Default path: `exec-plans/active/YYYY-MM-DD-<slug>/`.
- `Full`: `Orchestrator` establishes, declares, and validates a `Run Workspace` immediately after tier selection and before `S0`; then formalizes it during `S1` as part of `Execution Environment Spec`. Default path: `exec-plans/active/YYYY-MM-DD-<slug>/`; `Orchestrator` moves or copies completed run records to `exec-plans/completed/YYYY-MM-DD-<slug>/` unless a publish owner is explicitly assigned.
- `Lite` and `Full`: `Orchestrator` closes each step from `S0` through `S3` only after the required artifact for that step has been written to the run workspace, or to an explicitly declared equivalent location, before the next step starts.
- `Lite` and `Full`: when a publishable run uses prior non-publish exploration, `S0` through `S3` must close under the current `Publish` intent; stale exploration `Context Pack`, `Task Graph`, boundary status, gate verdict, or publish-readiness records do not satisfy current-run closure.
- `Lite` and `Full`: `S1` closes only after both `Role Owner Table` and `Run-Specific Responsibility Matrix` are written and field-valid.
- `S4` is only the final execution-entry assertion that earlier step-closure gates succeeded; it is not the first place missing artifacts should be discovered.
- `Orchestrator` owns the artifact index and any exception to the default path. Any exception must be declared in `Task Graph` `Writable Area`; in `Full`, also declare it in `Execution Environment Spec` `Artifact Locations`.
- `Orchestrator` validates any declared equivalent location as writable and accessible before the step closes. If validation fails, the step does not close.
- Step-closure gates are enforced by `Orchestrator` before the next step starts. If a required artifact is missing, incomplete, or field-invalid, `Orchestrator` stops the workflow and returns to the failed step.

## Operating Rules

- Human steers; agents execute.
- `Orchestrator` owns environment-gap repair in `Lite` and `Full`; the single `Owner` owns it in `Ultra Lite` or escalates before execution.
- Knowledge not encoded into the repo or task artifacts should be treated as unavailable.
- Keep `AGENTS.md` short and navigational.
- Prefer append-only context growth over repeatedly rewriting stable prefixes.
- Any change that depends on pre-existing state must be validated against a real pre-existing state surface by `Runtime Verifier`; if no verifier is active, `Orchestrator` must assign one or record why it is not required.
- `Orchestrator` assigns `Runtime Verifier` or records why no verifier is required for any change that depends on pre-existing state.
- If a single agent is nearing context overload, `Orchestrator` splits work into subagents or smaller owned tasks.
- When delegation is required, `Orchestrator` ensures the work crosses independent context boundaries; do not simulate separation with different role labels inside one context.
- Shift humans from line-by-line review to result acceptance whenever the validation surface is strong enough.

## What To Read

- For a tiny feature or bugfix, read [references/feature-template-ultra-lite.md](references/feature-template-ultra-lite.md).
- For a runnable midweight run sheet, read [references/workflow-template-lite.md](references/workflow-template-lite.md).
- For the full operating model, role contracts, and escalation rules, read [references/workflow-template.md](references/workflow-template.md).
- For role prompts, read [references/agent-prompts.md](references/agent-prompts.md).
- For the only canonical gate rubric, read [references/checklists.md](references/checklists.md).
- For canonical artifact fields and owners, read [references/artifact-registry.md](references/artifact-registry.md).
- For concrete action ownership, read the `Responsibility Matrix` in [references/artifact-registry.md](references/artifact-registry.md).

## Quick Start

1. Use `Fast Tier Check` to choose `Ultra Lite`, `Lite`, or `Full`.
2. For `Ultra Lite`, write the goal/scope block and complete `Preflight Judgment` before editing or executing.
3. For `Lite` or `Full`, `Orchestrator` decides early whether the run can establish the required independent context boundaries; if not, `Orchestrator` stops and redesigns instead of downgrading the same run to paper-only separation.
4. For `Lite` or `Full`, `Orchestrator` declares the `Run Workspace` before `S0`; use `exec-plans/active/YYYY-MM-DD-<slug>/` unless the run explicitly declares another writable area.
5. Open only the file for that tier first.
6. If you are in `Lite`, fill [references/workflow-template-lite.md](references/workflow-template-lite.md) first.
7. Open [references/artifact-registry.md](references/artifact-registry.md) before writing `Risk Register`, `Integration Ledger`, or `Decision Log`, and at any time a field name, artifact owner, or action owner is unclear.
8. Only open [references/agent-prompts.md](references/agent-prompts.md) when you need role-specific prompts.
9. Open [references/checklists.md](references/checklists.md) at gate time.

## Escalation Heuristics

Escalate or redesign if:
- agents are missing tooling or validation surfaces
- key knowledge lives only in chat or human memory
- outputs cannot be merged cleanly
- review burden falls back to humans line by line
- context grows faster than it is being summarized
- quality gates fail on source fidelity, execution completeness, external feedback, or entropy control

## Choose The Tier

Use `Ultra Lite` when:
- one owner can complete the work
- one direct validation path is enough
- no risk register or gate decision is needed

Use `Lite` when:
- you need a runnable midweight workflow
- you can name owners for `Orchestrator`, `Implementer`, `Critic`, and `Quality Gate`
- you can establish independent context boundaries if the run is meant to survive final gate and publish
- one workflow needs structured risk scan and gate review
- dynamic validation may be needed, but the work still centers on one primary implementation path

Use `Full` when:
- 5 or more distinct workflow roles need active ownership, excluding a single `Runtime Verifier` added only for state-surface validation
- more than one workflow must converge in parallel
- environment design or repo structure is part of the task
- you can establish independent context boundaries if the run is meant to survive final gate and publish
- `Lite` starts needing repeated human interpretation to pass gate review

## Fast Tier Check

Start with `Ultra Lite` if all three are true:
- one owner is enough
- one validation path is enough
- failure does not require a formal gate loop

Start with `Full` immediately if any two are true:
- more than one workflow must converge
- environment or repo structure is part of the deliverable
- you already expect 5 or more distinct workflow roles other than a single `Runtime Verifier` added only for state-surface validation to need active ownership
- human decisions must be logged across multiple rounds

Otherwise start with `Lite`.

## Required Artifacts By Tier

Ultra Lite:
- one short goal/scope block
- one `Preflight Judgment`
- one owner
- one validation path
- one validation-failure action

Lite:
- one declared `Run Workspace` before `S0`
- one short `Task Brief`
- one role owner table
- one run-specific responsibility matrix
- one `Context Pack`
- one `Task Graph`
- step-closure records for `S0`, `S1`, `S2`, and `S3` before the next step starts
- one `Execution Output Record`
- one `Runtime Evidence Record` when correctness depends on pre-existing state or independent dynamic validation
- one `Risk Register`
- one `Integration Ledger` with owner and evidence-source fields
- one `Gate Decision`
- one `Decision Log`
- real context-boundary records for delegated owners when independent-context delegation is used

Full:
- everything in Lite
- `Execution Environment Spec`
- one declared `Run Workspace` before `S0`, formalized during `S1`
- full workflow draft
- `Published Version`
- `Next Iteration Notes`

Keep outputs structured and operational, not essay-like.
