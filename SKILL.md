---
name: harness-engineering-workflow
description: "Use when a task needs a repeatable Harness run sheet with explicit owners, repo-backed artifacts, validation gates, or independent-context delegation. Best for Lite/Full workflow runs, publish-separation decisions, and agent-first coordination where local independent subagents may be used at highest appropriate reasoning depth."
---

# Harness Engineering Workflow

Use this skill for environment-first, repo-backed workflow runs that need:
- explicit owners
- validation gates
- continuation checkpoints
- independent-context delegation
- reusable run artifacts

Do not use it for plain one-off coding, casual brainstorming, or tasks that do not need workflow artifacts or gate logic.

## Fast Start

1. Choose a tier with `Fast Tier Check`.
2. For `Ultra Lite`, use one owner, one validation path, and a short `Preflight Judgment`.
3. For `Lite` or `Full`, declare the `Run Workspace` before `S0`, then follow the tier template.
4. Use local independent subagents when they provide a real separate context boundary and artifact output. Prefer the highest appropriate reasoning depth when no external reviewer is required.

## Fast Tier Check

- Start with `Ultra Lite` when one owner and one validation path are enough, and failure does not require a formal gate loop.
- Start with `Full` immediately when two or more Full signals are already true: multi-workflow convergence, environment or repo structure in the deliverable, 5+ active roles, or human decisions across multiple rounds.
- Otherwise start with `Lite`.

## Core Rules

- Treat `role`, `owner`, and `subagent` as different things.
- Count delegation only when execution crosses an independent context boundary.
- Do not treat tool surfaces, runtimes, sessions, or hosts as owners.
- Do not reuse the same accountable owner for `Advisor` and `Implementer`, `Critic`, or `Quality Gate`.
- For publishable `Lite` or `Full`, keep `Orchestrator`, `Implementer`, and `Quality Gate` on separate accountable owners and independent boundaries, or stop with `Boundary Integrity`.
- If `Critic` is external but `Quality Gate` is not, apply the `External-Critic-Only Quality Gate Rule`.
- Run `python scripts/validate_harness_run.py <run-workspace>` at `S1` closure / `S2` entry before downstream work.
- Keep `CURRENT.md` pointing to the latest `checkpoints/NNNN-S<step>.md` file.
- Use append-only checkpoints and resolve any `Boundary Violations` before resuming task-domain work.

## What To Read

- `references/feature-template-ultra-lite.md` for tiny work
- `references/workflow-template-lite.md` for Lite runs
- `references/workflow-template.md` for Full runs
- `references/checklists.md` for gate logic
- `references/artifact-registry.md` for schemas and ownership
- `references/agent-prompts.md` for role prompts

## Tier Selection

- Use `Ultra Lite` when one owner and one validation path are enough.
- Use `Lite` when you need a runnable midweight workflow with a gate.
- Use `Full` when environment design, multi-workflow convergence, or heavier role separation is part of the job.

Keep this file lean; put details in `references/`.
