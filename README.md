# Harness Engineering Workflow Skill

This repository contains a Codex skill for running a structured Harness Engineering workflow. The workflow is designed for tasks that need explicit owners, workflow artifacts, validation gates, and a repo-centered operating model instead of a one-off chat response.

The installable skill lives in [harness-engineering-workflow](C:/Users/wangsong/Desktop/harness-engineering/harness-engineering-workflow). The repository root is for packaging and documentation; it is not itself a skill folder.

## Skill Summary

- Skill name: `harness-engineering-workflow`
- Display name: `Harness Workflow`
- Invocation style: explicit only
- Trigger form: `$harness-engineering-workflow`

Use this skill when the task needs a reusable workflow with tiering from `Ultra Lite` to `Full`, plus role ownership, context packaging, gate review, and result acceptance.

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
  "C:\Users\wangsong\Desktop\harness-engineering\harness-engineering-workflow" `
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
python C:\Users\wangsong\.codex\skills\.system\skill-creator\scripts\quick_validate.py `
  C:\Users\wangsong\Desktop\harness-engineering\harness-engineering-workflow
```

Validate the installed copy the same way:

```powershell
python C:\Users\wangsong\.codex\skills\.system\skill-creator\scripts\quick_validate.py `
  C:\Users\wangsong\.codex\skills\harness-engineering-workflow
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

## Source Of Truth

- Human-facing entrypoint: [README.md](C:/Users/wangsong/Desktop/harness-engineering/README.md)
- Skill entrypoint: [SKILL.md](C:/Users/wangsong/Desktop/harness-engineering/harness-engineering-workflow/SKILL.md)
- UI metadata: [agents/openai.yaml](C:/Users/wangsong/Desktop/harness-engineering/harness-engineering-workflow/agents/openai.yaml)
- Workflow references: [references/](C:/Users/wangsong/Desktop/harness-engineering/harness-engineering-workflow/references)
