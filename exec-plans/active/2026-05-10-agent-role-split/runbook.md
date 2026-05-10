Run ID: 2026-05-10-agent-role-split
Tier: Lite
Created Before Step: S0
Active Path: exec-plans/active/2026-05-10-agent-role-split/
Completed Path: exec-plans/completed/2026-05-10-agent-role-split/
Artifact Index: README.md, SKILL.md, references/agent-prompts.md, references/artifact-registry.md, references/checklists.md, scripts/validate_harness_run.py, tests/fixtures
Step Closure Gates: S0-S3 artifacts before downstream edits; validate_harness_run.py before gate
Exception Paths: none
Telemetry Mode: Off
Event Log Path:
Profiler Summary Path:

# S0 Task Brief

Goal: Update harness-engineering-workflow rules from thread 019e1211 so Orchestrator remains thin, phase-critical actions have explicit owners, and spawned agent model-tier choices are documented safely.
Non-goals: Do not rewrite the full workflow model. Do not make Claude an Implementer for this change. Do not edit the original checkout outside this git worktree.
Constraints: Work in C:\Users\wangsong\Desktop\worktrees\harness-agent-role-split. Use Opus as Advisor or external review gate only when explicitly assigned, never as Implementer. Keep model-tier additions warning-oriented except for mechanically clear boundary violations.
Success Criteria: Skill docs explain phase-critical owner separation and model-tier guidance. Validator warns on weak small-model gate/source roles and fails Advisor/Implementer, Advisor/Critic, and Advisor/Gate owner collisions. Existing self-tests pass.
Human Decision Points: User may decide whether to merge/publish from the worktree after review.

# S1 Role Owner Table

Publish Intent: Publish
Boundary Status: Satisfied
Continuation Packet: CURRENT.md

Role | Owner | Context Boundary | Shared? | Notes
--- | --- | --- | --- | ---
Orchestrator | Main Codex | current Codex thread in worktree | No | owns task coordination and final report
Implementer | OpenAI Worker Implementer | worktree edit context | No | owns documentation and validator patch
Critic | Opus Critic | Claude delegate session 7847d508-047c-4bd0-912f-0de562d85cf2 | No | post-implementation critique only, not advisor or gate
Quality Gate | Opus 4.7 Gate Reviewer | Claude delegate max-effort review context | No | owns final external review verdict after local validation
Advisor | Opus Advisor | Claude delegate session 405b7c89-40d9-4fd4-94c0-320dcf210344 | No | advisory only

Run-Specific Responsibility Matrix:

Phase-Critical Action | Owner Resolution | Required Record | Override? | Notes
--- | --- | --- | --- | ---
S6 integration closure | Orchestrator | Integration summary in final response | No |
S7 gate verdict | Quality Gate | test and validator output | No |
S7 gate outcome append and replay coordination | Orchestrator | final response | No |
Gate-requested rework | Implementer for docs/code patch issue; Orchestrator for process record issue | refreshed diff and test output | No | Gate names the applicable owner in its verdict
Re-gate after corrective work | Quality Gate | fresh test and validator output | No | Gate repeats review after rework output exists
S8 publish readiness verification | Orchestrator | git diff/status and test evidence | No |
S8 publish, commit, check-in, or submit | Orchestrator only if user asks to commit/push | git evidence | No | no commit requested yet

# S2 Context Pack

Core Context: Thread handoff says main thread should orchestrate only, Implementer changes code/docs, Publish Worker handles upload/restart/scoped commit when assigned, Runtime Verifier handles live checks, Quality Gate reads artifacts/diff only, and Advisor/Opus gives debate without acting as gate or implementer.
Optional Context: Opus pre-implementation critique recommends docs-first model-tier guidance and a mechanical Advisor/Gate collision check, plus warning-only small-model heuristics.
Forbidden Scope: Original checkout writes, broad vendor lock-in, full workflow rewrite.
Stable Prefix: Existing harness skill boundary and continuation rules remain canonical.

# S3 Task Graph

Task | Owner | Context Boundary | Depends On | Outputs | Writable Area | Validation Checkpoint | Fallback
--- | --- | --- | --- | --- | --- | --- | ---
Add thin Orchestrator and model-tier policy docs | Implementer | worktree edit context | S2 Context Pack | documentation diff | README.md, SKILL.md, references/*.md, agents/openai.yaml | quick_validate.py skill check and rg spot checks | Return to S3
Add validator warning/error support | Implementer | worktree edit context | S2 Context Pack | validator and fixtures diff | scripts/validate_harness_run.py, tests/fixtures | validate_harness_run.py --self-test | Return to S3

# S7 Gate Decision

Verdict: Pending
Evidence: Not yet run.

# Continuation Packet

Current Checkpoint: checkpoints/0001-S1.md
