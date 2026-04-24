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

Only add more roles such as `Runtime Verifier`, `Source Analyst`, `Workflow Designer`, or `Human Decision Maker` when the task actually needs them.

Do not default to the full role set on small tasks.

## Execution Policy

Treat `role`, `owner`, and `subagent` as different things:
- `Role`: the responsibility
- `Owner`: the accountable executor for that responsibility
- `Subagent`: the concrete delegated execution slot, but for this skill delegation counts only when execution crosses an independent context boundary

Default execution posture:
- `Ultra Lite`: stay single-owner unless boundaries are unclear
- `Lite`: if the run is intended for final publish, establish at least 2 distinct independent context boundaries before deep execution starts
- `Full`: if the run is intended for final publish, establish at least 3 distinct independent context boundaries before deep execution starts
- if a tier requires separated owners and the run cannot establish the required independent context boundaries, stop as a fatal `Boundary Integrity` failure and tell the user final-result quality is uncontrollable
- different role labels, tool calls, or spawns that remain within the same context do not satisfy this requirement

Do not treat distinct role names by themselves as proof of distinct execution ownership.
Record context boundaries in the role table and task graph whenever delegated work is used.
Agent identifiers may be recorded when available, but they are supporting evidence only and do not prove context independence.

## Operating Rules

- Human steers; agents execute.
- Fix environment gaps before blaming the model.
- Knowledge not encoded into the repo or task artifacts should be treated as unavailable.
- Keep `AGENTS.md` short and navigational.
- Prefer append-only context growth over repeatedly rewriting stable prefixes.
- Any change that depends on pre-existing state must be validated against a real pre-existing state surface.
- If a single agent is nearing context overload, split work into subagents or smaller owned tasks.
- When delegation is required, ensure the work crosses independent context boundaries; do not simulate separation with different role labels inside one context.
- Shift humans from line-by-line review to result acceptance whenever the validation surface is strong enough.

## What To Read

- For a tiny feature or bugfix, read [references/feature-template-ultra-lite.md](references/feature-template-ultra-lite.md).
- For a runnable midweight run sheet, read [references/workflow-template-lite.md](references/workflow-template-lite.md).
- For the full operating model, role contracts, and escalation rules, read [references/workflow-template.md](references/workflow-template.md).
- For role prompts, read [references/agent-prompts.md](references/agent-prompts.md).
- For the only canonical gate rubric, read [references/checklists.md](references/checklists.md).
- For canonical artifact fields and owners, read [references/artifact-registry.md](references/artifact-registry.md).

## Quick Start

1. Use `Fast Tier Check` to choose `Ultra Lite`, `Lite`, or `Full`.
2. For `Lite` or `Full`, decide early whether the run can establish the required independent context boundaries; if not, stop and redesign instead of downgrading the same run to paper-only separation.
3. Open only the file for that tier first.
4. If you are in `Lite`, fill [references/workflow-template-lite.md](references/workflow-template-lite.md) first.
5. Open [references/artifact-registry.md](references/artifact-registry.md) before writing `Risk Register`, `Integration Ledger`, or `Decision Log`, and at any time a field name or artifact owner is unclear.
6. Only open [references/agent-prompts.md](references/agent-prompts.md) when you need role-specific prompts.
7. Open [references/checklists.md](references/checklists.md) at gate time.

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
- one owner
- one validation path
- one validation-failure action

Lite:
- one short `Task Brief`
- one role owner table
- one `Context Pack`
- one `Task Graph`
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
- full workflow draft
- `Published Version`
- `Next Iteration Notes`

Keep outputs structured and operational, not essay-like.
