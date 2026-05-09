# Telemetry On File Missing

Telemetry Mode: On
Event Log Path: <run-workspace>/missing-telemetry.jsonl

## S1 Role Owner Table

Publish Intent: Publish
Boundary Status: Satisfied

Role | Owner | Context Boundary | Shared? | Notes
--- | --- | --- | --- | ---
Orchestrator | Main Codex | current Codex thread | No | owns coordination
Implementer | Claude Delegate Implementer | delegate implementation session | No | owns patch
Quality Gate | Claude Delegate Gate | delegate gate session | No | owns gate

Run-Specific Responsibility Matrix:

Phase-Critical Action | Owner Resolution | Required Record | Override? | Notes
--- | --- | --- | --- | ---
S7 gate verdict | Quality Gate | Gate Decision | No |
S8 publish, commit, submit, or check-in | Orchestrator | publish evidence | No |
