# Missing Task Checkpoint Runbook

## S1 Role Owner Table

Publish Intent: Publish
Boundary Status: Satisfied

Role | Owner | Context Boundary | Shared? | Notes
--- | --- | --- | --- | ---
Orchestrator | Main Codex | current Codex thread | No | owns run workspace
Implementer | Local Worker Agent | local worker context 019x | No | owns patch
Critic | Opus Critic | opus critic session | No | owns risk scan
Quality Gate | Opus Gate | opus gate session | No | owns gate

Run-Specific Responsibility Matrix:

Phase-Critical Action | Owner Resolution | Required Record | Override? | Notes
--- | --- | --- | --- | ---
S7 gate verdict | Quality Gate | Gate Decision | No |
S8 publish, commit, submit, or check-in | Orchestrator | publish evidence | No |

## S2 Context Pack

Context is current and publish-scoped.

## S3 Task Graph

Task | Owner | Context Boundary | Depends On | Outputs | Writable Area | Fallback
--- | --- | --- | --- | --- | --- | ---
Patch several things | Implementer | local worker context 019x | S2 Context Pack | Execution Output Record | src/mixed | Return to S3

## S7 Gate Decision

Verdict: Pass
Evidence: this fixture should fail before gate because the implementation node has no validation checkpoint.
