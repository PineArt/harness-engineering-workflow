# Harness Runbook: Front-Loaded Artifact Controls

Telemetry Mode: Off

## Task Brief

Goal:
Make artifact and runbook generation front-loaded across Ultra Lite, Lite, and Full so runs start on a declared track instead of relying on post-hoc gate discovery.

Non-goals:
Do not add heavy multi-file ceremony to every Ultra Lite task.
Do not change the independent-context boundary policy except where artifact timing interacts with it.

Constraints:
Keep the existing tier model.
Use `exec-plans/active/<run-id>/` as the default durable workspace for publishable Lite and Full.
Use Opus critique before and after the documentation change.

Success Criteria:
The skill docs define when run artifacts are created before execution starts.
Lite and Full declare a run workspace before S0 and close S0 through S3 only after required artifacts are written.
Ultra Lite has a required Preflight Judgment before task-specific execution and clear escalation into Lite.
The skill validates with `quick_validate.py`.

Human Decision Points:
The user wants all tiers covered and prefers front-loaded correctness over after-the-fact checks.

## Role Owner Table

Role | Owner | Context Boundary | Shared? | Notes
Orchestrator | Codex main | Current Codex context | Yes | Owns doc integration and runbook
Implementer | Codex main | Current Codex context | Yes | Applies focused documentation patch
Advisor | Opus via claude_delegate | Claude session f62bb298-c642-4d8d-aee9-4fb5a4b8c0bb | No | Pre-change critique already completed
Critic | Opus via claude_delegate | Claude session f62bb298-c642-4d8d-aee9-4fb5a4b8c0bb or follow-up | No | Post-change critique planned
Quality Gate | Codex main | Current Codex context | Yes | This is a policy maintenance run, not final publish separation certification

## Run Workspace Contract

Run ID:
2026-04-30-frontload-artifacts

Tier:
Lite maintenance pass

Active Path:
exec-plans/active/2026-04-30-frontload-artifacts/

Completed Path:
exec-plans/completed/2026-04-30-frontload-artifacts/

Artifact Index:
runbook.md contains Task Brief, Role Owner Table, Run Workspace Contract, Context Pack, Task Graph, Decision Log, Risk Register, Integration Ledger, and Gate Decision.

Step Closure Gates:
Run Intake: Run Workspace declared before S0.
S0: Task Brief and initial Decision Log written before S1.
S1: Role Owner Table written before S2.
S2: Context Pack written before S3.
S3: Task Graph written before S4.

## Context Pack

Core Context:
Previous skill docs defined artifact schemas and step timing, but default path creation and step-closure artifact creation were not mandatory.

Optional Context:
Full template already names `exec-plans/active/` and `exec-plans/completed/` as the process record area.
Opus suggested making workspace mandatory for Full and publishable Lite, while preserving Ultra Lite minimalism.

Forbidden Scope:
Do not redesign role separation.
Do not add runtime code or a new validator in this pass unless documentation alone cannot express the rule.

Stable Prefix:
Front-load run artifacts before execution instead of detecting missing records only at S8.

Required Tools:
PowerShell, apply_patch, `quick_validate.py`, claude_delegate.

## Task Graph

Task:
Patch the harness skill docs with front-loaded workspace and artifact timing controls.

Owner:
Codex main

Context Boundary:
Current Codex context

Depends On:
Pre-change Opus critique.

Outputs:
Documentation patch and validation results.

Writable Area:
SKILL.md, README.md, references/*.md, exec-plans/active/2026-04-30-frontload-artifacts/

Fallback:
If validator or post-change critique finds ambiguity, revise the docs before final.

## Decision Log

Decision:
Use a durable run workspace for this documentation maintenance pass.
Decision Owner:
Codex main
Reason:
The change itself is about front-loaded artifacts, so the run should model the intended behavior.
Affected Artifact:
runbook.md
Recorded At:
2026-04-30
Next Step:
Patch docs and validate.

Decision:
Move artifact enforcement earlier than S4.
Decision Owner:
User and Codex main
Reason:
The user pointed out that blocking at S4 is still too late for "一次性把事情作对做好"; S4 should only assert earlier step gates, not be the first gate.
Affected Artifact:
SKILL.md, workflow-template-lite.md, workflow-template.md, artifact-registry.md, checklists.md, agent-prompts.md
Recorded At:
2026-04-30
Next Step:
Replace S4-first wording with Run Intake and per-step closure gates.

Decision:
Make Ultra Lite preflight judgment mandatory.
Decision Owner:
User and Codex main
Reason:
The user clarified that Ultra Lite also must have basic事前判断, not just a goal block.
Affected Artifact:
feature-template-ultra-lite.md, SKILL.md, artifact-registry.md, checklists.md, agent-prompts.md, README.md
Recorded At:
2026-04-30
Next Step:
Validate and re-gate the updated wording.

Decision:
Add a concrete action ownership audit.
Decision Owner:
User and Codex main
Reason:
The user clarified that every concrete thing must be assigned to a person/role, not only artifacts.
Affected Artifact:
artifact-registry.md, SKILL.md, checklists.md, agent-prompts.md, workflow-template-lite.md, workflow-template.md, feature-template-ultra-lite.md
Recorded At:
2026-04-30
Next Step:
Add Responsibility Matrix, patch hot-path ownerless verbs, validate, and request independent audit.
