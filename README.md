# Harness Engineering Workflow Skill

This repository contains a Codex skill for running a structured Harness Engineering workflow. The workflow is designed for tasks that need explicit owners, workflow artifacts, validation gates, and a repo-centered operating model instead of a one-off chat response.

The repository root is the installable skill folder.

## Skill Summary

- Skill name: `harness-engineering-workflow`
- Display name: `Harness Workflow`
- Invocation style: explicit only
- Trigger form: `$harness-engineering-workflow`
- Delegation mode: explicit user-visible subagents with distinct Agent IDs, including terminal/CLI agent flows; hidden/background `spawn_agent` runs do not count

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
- Do not use `Ultra Lite` for correctness-critical changes such as integrity, durability, recovery, ordering, security, or externally visible contract semantics.
- `Lite` final publish requires at least 2 distinct owners backed by at least 2 explicit user-visible subagents with distinct `Agent ID` values.
- For this skill, delegated owners count only when backed by explicit user-visible subagents with distinct `Agent ID` values, including terminal/CLI agent flows. Hidden/background `spawn_agent` runs are treated as delegation-unavailable and are a fatal `Boundary Integrity` failure for publish-separation tiers.
- In publishable `Lite`, `Implementer` may not also own `Quality Gate`.
- `Full` final publish requires at least 3 distinct owners.
- In publishable `Full`, `Implementer`, `Critic`, and `Quality Gate` must have different owners.
- In publishable `Full`, `Quality Gate` may not also own `Orchestrator`.
- Do not relabel missing explicit user-visible delegation or single-owner `Lite` as exploration-only. Treat them as fatal `Boundary Integrity` failures and tell the user final-result quality is uncontrollable.

## Source Of Truth

- Human-facing entrypoint: [README.md](./README.md)
- Skill entrypoint: [SKILL.md](./SKILL.md)
- UI metadata: [agents/openai.yaml](./agents/openai.yaml)
- Workflow references: [references/](./references)
