# Harness Engineering Workflow Skill

This repository contains a Codex skill for running a structured Harness Engineering workflow. The workflow is designed for tasks that need explicit owners, workflow artifacts, validation gates, and a repo-centered operating model instead of a one-off chat response.

The installable skill lives in [harness-engineering-workflow](./harness-engineering-workflow). The repository root is for packaging and documentation; it is not itself a skill folder.

## Skill Summary

- Skill name: `harness-engineering-workflow`
- Display name: `Harness Workflow`
- Invocation style: explicit only
- Trigger form: `$harness-engineering-workflow`
- Delegation mode: explicit UI-visible subagents only; hidden/background `spawn_agent` runs do not count

Use this skill when the task needs a reusable workflow with tiering from `Ultra Lite` to `Full`, plus role ownership, context packaging, gate review, and result acceptance.

## Role Mapping

There is no formal `Planner` role in this workflow.

Planning responsibilities are split across:

- `Orchestrator`: defines goals, splits work, assigns owners, and converges outputs
- `Workflow Designer`: designs workflow steps, dependencies, and fallbacks when the `Full` tier needs a dedicated workflow-design role

In practice, `Planner` maps most closely to `Orchestrator + Workflow Designer`, not to a separate standalone role.

## Repository Layout

```text
harness-engineering/
|-- README.md
|-- harness-engineering-workflow/
|   |-- SKILL.md
|   |-- agents/
|   |   `-- openai.yaml
|   `-- references/
|       |-- workflow-template.md
|       |-- workflow-template-lite.md
|       |-- feature-template-ultra-lite.md
|       |-- checklists.md
|       |-- artifact-registry.md
|       `-- agent-prompts.md
`-- materials/
```

## Install

Install by copying the skill subfolder into your Codex skills directory.

PowerShell:

```powershell
Copy-Item -Recurse -Force `
  ".\harness-engineering-workflow" `
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
  ".\harness-engineering-workflow"
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
- Do not use `Ultra Lite` for correctness-critical changes such as integrity, durability, recovery, ordering, security, or externally visible contract semantics.
- `Lite` final publish requires at least 2 distinct owners.
- For this skill, delegated owners count only when backed by explicit UI-visible subagents. Hidden/background `spawn_agent` runs are treated as delegation-unavailable.
- In publishable `Lite`, `Implementer` may not also own `Quality Gate`.
- `Full` final publish requires at least 3 distinct owners.
- In publishable `Full`, `Implementer`, `Critic`, and `Quality Gate` must have different owners.
- In publishable `Full`, `Quality Gate` may not also own `Orchestrator`.
- Exploration-only runs are allowed in any tier, but they do not satisfy final `Boundary Integrity` for publish by themselves.

## Source Of Truth

- Human-facing entrypoint: [README.md](./README.md)
- Skill entrypoint: [SKILL.md](./harness-engineering-workflow/SKILL.md)
- UI metadata: [agents/openai.yaml](./harness-engineering-workflow/agents/openai.yaml)
- Workflow references: [references/](./harness-engineering-workflow/references)
