# Harness Engineering Workflow Skill

This repository contains a Codex skill for running a structured Harness Engineering workflow. The workflow is designed for tasks that need explicit owners, workflow artifacts, validation gates, and a repo-centered operating model instead of a one-off chat response.

The repository root is the installable skill folder.

## Skill Summary

- Skill name: `harness-engineering-workflow`
- Display name: `Harness Workflow`
- Invocation style: explicit only
- Trigger form: `$harness-engineering-workflow`
- Delegation mode: independent context boundaries; role labels, tool calls, or spawns that stay in the same context do not count

Use this skill when the task needs a reusable workflow with tiering from `Ultra Lite` to `Full`, plus role ownership, context packaging, gate review, and result acceptance.

## Role Mapping

There is no formal `Planner` role in this workflow.

Planning responsibilities are split across:

- `Orchestrator`: defines goals, splits work, assigns owners, and converges outputs
- `Workflow Designer`: designs workflow steps, dependencies, and fallbacks when the `Full` tier needs a dedicated workflow-design role

In practice, `Planner` maps most closely to `Orchestrator + Workflow Designer`, not to a separate standalone role.

## Repository Layout

```text
harness-engineering-workflow/
|-- README.md
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
`-- references/
    |-- workflow-template.md
    |-- workflow-template-lite.md
    |-- feature-template-ultra-lite.md
    |-- checklists.md
    |-- artifact-registry.md
    `-- agent-prompts.md
```

## Install

Install by copying this repository root into your Codex skills directory.

PowerShell:

```powershell
Copy-Item -Recurse -Force `
  "." `
  "$HOME\.codex\skills\harness-engineering-workflow"
```

If `CODEX_HOME` is set, the target should be:

```text
$CODEX_HOME/skills/harness-engineering-workflow
```

After installation, restart Codex so the new skill is discovered.

## Validate

Validate the source skill directory with the standard quick validator:

```powershell
python "$HOME\.codex\skills\.system\skill-creator\scripts\quick_validate.py" `
  "."
```

Validate the installed copy the same way:

```powershell
python "$HOME\.codex\skills\.system\skill-creator\scripts\quick_validate.py" `
  "$HOME\.codex\skills\harness-engineering-workflow"
```

Expected result:

```text
Skill is valid!
```

## Use

Invoke the skill explicitly in Codex:

```text
Use $harness-engineering-workflow to plan this change with explicit owners and a Lite gate review.
```

The skill starts with a `Fast Tier Check` and then routes work into `Ultra Lite`, `Lite`, or `Full`.

## Tier Guardrails

- `Ultra Lite` is for low-risk, tightly bounded work where 1 owner and 1 strong validation path are enough for final publish.
- `Ultra Lite` starts with a filled goal/scope block and `Preflight Judgment` before task-specific execution.
- Do not use `Ultra Lite` for correctness-critical changes such as integrity, durability, recovery, ordering, security, or externally visible contract semantics.
- `Lite` and `Full` runs must declare a `Run Workspace` before `S0`; default active path is `exec-plans/active/YYYY-MM-DD-<slug>/`.
- Before `S1` closes and `S2` begins, `Lite` and `Full` must declare publish intent or record the run as non-publish exploration.
- If a publishable `Lite` or `Full` run imports or continues from non-publish exploration, `S0` records that material as evidence or context only, and `S0` through `S3` must re-close under current `Publish` intent.
- Publishable `Lite` and `Full` runs may not inherit `Boundary Status`, `Gate Decision`, publish-readiness claims, `Context Pack`, or `Task Graph` closure from non-publish exploration.
- For publishable `Lite` and `Full`, S1 boundary status cannot be conditional or deferred to final gate; it must be satisfied before `S2` or the run stops.
- `Lite` and `Full` `S1` must include both `Role Owner Table` and `Run-Specific Responsibility Matrix`; the matrix resolves S6, S7, S8, gate, rework, re-gate, replay, publish, commit, check-in, and submit ownership without copying the full canonical matrix.
- `Lite` final publish requires `Orchestrator`, `Implementer`, and `Quality Gate` to have explicit accountable owners backed by at least 3 independent context boundaries.
- `Full` runs must formalize that `Run Workspace` during `S1` in `Execution Environment Spec`.
- For `Lite` and `Full`, `S0` through `S3` close only after their required artifacts are written before the next step starts.
- For this skill, delegation counts only when execution crosses an independent context boundary. Role labels, tool calls, or spawns that remain within the same context do not satisfy publish separation.
- In publishable `Lite` and `Full`, `Orchestrator` may not also own `Implementer` or `Quality Gate`.
- `Full` final publish requires at least 3 distinct owners backed by at least 3 independent context boundaries.
- In publishable `Full`, `Implementer`, `Critic`, and `Quality Gate` must have different owners.
- In publishable `Full`, `Quality Gate` may not also own `Orchestrator`.
- In publishable `Lite` or `Full`, `Quality Gate` must be explicitly assigned and independent from the implementation context.
- Tool surfaces, protocols, credentials, hosts, paths, sessions, sandboxes, runtimes, and execution environments are context or evidence, not independent accountable owners by themselves.
- `Advisor` may provide direction, debate, or options, but does not satisfy `Critic`, `Quality Gate`, or publish separation by itself.
- If an external context covers `Critic` but not `Quality Gate` while the main context owns implementation, apply the `External-Critic-Only Quality Gate Rule` in [references/checklists.md](./references/checklists.md).
- Do not relabel missing required independent context boundaries or single-owner `Lite` as exploration-only. Treat them as fatal `Boundary Integrity` failures and tell the user final-result quality is uncontrollable.

## Source Of Truth

- Human-facing entrypoint: [README.md](./README.md)
- Skill entrypoint: [SKILL.md](./SKILL.md)
- UI metadata: [agents/openai.yaml](./agents/openai.yaml)
- Workflow references: [references/](./references)
