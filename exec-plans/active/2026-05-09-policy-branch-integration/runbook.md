# Harness Policy Branch Integration

## S0 Task Brief

Publish Intent: Publish

Goal: integrate the completed `codex/harness-run-telemetry` and `codex/harness-p0-p2-compact-recovery` policy branches into current `main`, which already includes `codex/harness-step-slicing`.

Non-goals: redesign the workflow policy beyond conflict resolution; use Claude as implementer; drop existing fixtures or weaken validator behavior to pass tests.

Success Criteria:
- `main` includes S3 implementation slicing, telemetry validation, and continuation checkpoint validation.
- `scripts/validate_harness_run.py --self-test` passes.
- focused stage smoke checks pass for valid fixtures.
- `git diff --check` passes.
- Opus post-review finds no blocking/P1/P2 merge issues.
- `main` is pushed to `origin/main`.

Telemetry Mode: Off

Closure: S0 written before merge work starts.

## S1 Role Owner Table

Boundary Status: Satisfied

Role | Owner | Context Boundary | Shared? | Notes
---|---|---|---|---
Orchestrator | Main Codex | current Codex thread | No | owns merge plan, integration, and publish loop
Implementer | Main Codex | current Codex thread | Yes | performs conflict resolution because user required GPT/Codex implementer
Critic | Opus Pre/Post Review | Claude delegate review session | No | reviews strategy and final diff
Quality Gate | Main Codex Validator Gate | local validator and git checks | No | non-publish-separation gate for this repo maintenance merge

Run-Specific Responsibility Matrix:

Phase-Critical Action | Owner Resolution | Required Record | Override? | Notes
---|---|---|---|---
S6 integration ledger | Orchestrator | runbook integration notes | No |
S7 gate verdict | Quality Gate | validation commands and Opus review summary | No |
S8 publish readiness verification | Orchestrator | final status and push evidence | No |
S8 publish, commit, check-in, or submit | Orchestrator | commit/push evidence | No |
Gate-requested rework | Orchestrator | refreshed diff and validation | Deferred field |
Re-gate after corrective work | Quality Gate | fresh validation and review | Deferred field |

Closure: S1 written before S2 and before merge actions. Current run is a controlled repo-maintenance publish where Opus is critic only and implementation remains Codex-owned by user instruction.

## S2 Context Pack

Core Context:
- Current `main` is `b6d31a2 Require S3 implementation checkpoints`.
- Unmerged branches are `d628f5d Add harness run telemetry validation` and `1508d5c Add continuation checkpoint validation`.
- Both branches diverged from `e105807` and touch `scripts/validate_harness_run.py`, workflow templates, registry/checklists, and fixtures.
- Opus pre-review recommends manual section-wise integration preserving all three policies.

Optional Context:
- Existing branch `codex/harness-step-slicing` is already merged into `main`.
- `codex/ignore-python-bytecode` is stale and not a policy branch to merge.

Forbidden Scope:
- removing S3 checkpoint fixtures.
- making telemetry or continuation checks warning-only to avoid conflicts.
- using Claude as implementer.

Stable Prefix:
- preserve validator behavior for S1 publish checks, S3 task graph checkpoint checks, telemetry mode checks, and continuation checkpoint checks.

Required Tools:
- `git merge`
- `python scripts\validate_harness_run.py --self-test`
- focused `validate_harness_run.py` stage smoke checks
- `git diff --check`
- Opus review via `delegating-with-claude`

Closure: S2 written before S3.

## S3 Task Graph

Task | Owner | Context Boundary | Depends On | Outputs | Writable Area | Validation Checkpoint | Fallback
---|---|---|---|---|---|---|---
Merge telemetry branch | Main Codex | integration worktree | S0-S2 | merged telemetry schema, docs, validator, fixtures | integration worktree | `python scripts\validate_harness_run.py --self-test` | resolve by section and rerun
Merge continuation branch | Main Codex | integration worktree | telemetry merge | merged continuation schema, docs, validator, fixtures | integration worktree | `python scripts\validate_harness_run.py --self-test` | resolve by section and rerun
Final integration validation | Main Codex | integration worktree | both merges | validation evidence | integration worktree | self-test, focused stage checks, `git diff --check`, Opus post-review | fix and re-gate
Publish to main | Main Codex | installed skill worktree | validation pass | pushed `origin/main` | installed skill checkout | `git status --short --branch` and HEAD equals origin/main | stop before push if dirty or divergent

Closure: S3 written before S4 merge execution.
