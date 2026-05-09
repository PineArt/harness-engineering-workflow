# Harness Artifact Validator Run

Run ID: 2026-05-02-harness-artifact-validator
Tier: Lite
Run Workspace: `exec-plans/active/2026-05-02-harness-artifact-validator/`
Telemetry Mode: Off

## S0 Task Brief

Goal:
Add a mechanical artifact validator so invalid publishable `Lite`/`Full` role-boundary artifacts cannot close `S1`, enter `S2`, or receive a publish/pass gate by wording alone.

Scope:
- Add `scripts/validate_harness_run.py`.
- Add regression fixtures, including the corpview bad `S1`/`S7` artifact pair.
- Require validator execution at `S1` closure / `S2` entry and before `S7` pass or publish-readiness verdicts.

Non-goals:
- Do not require S1 and S7 to be in separate files.
- Do not restrict valid owners to humans or fixed governance-domain labels.
- Do not add nested-run inheritance semantics.

Success Criteria:
- `python scripts/validate_harness_run.py --self-test` passes.
- The corpview regression fixture fails validation before `S2`.
- Valid single-runbook and valid separate-file fixtures pass.
- Skill validation still passes.
- Opus final review sees the validator and fixture evidence before approval.

S0 Closure: Complete. Task brief and run workspace exist before implementation.

## S1 Role Owner Table

Publish Intent: Non-publish exploration
Boundary Status: Non-publish

Role | Owner | Context Boundary | Shared? | Notes
--- | --- | --- | --- | ---
Orchestrator | Main Codex | current Codex thread | No | owns run workspace, validator contract, integration, and docs wiring
Implementer | Main Codex implementation pass | current Codex implementation context | No | owns local script, fixtures, and docs patch
Critic | Opus via delegating-with-claude | external Claude context session `85a78796-d08a-4e1b-a5c8-f78baea92f0c` | No | pre-mortem and joint retrospective
Quality Gate | Opus final gate via delegating-with-claude | fresh external Claude gate context, to be recorded after patch | No | must review final diff and validator evidence

Run-Specific Responsibility Matrix:

Phase-Critical Action | Owner Resolution | Required Record | Override? | Notes
--- | --- | --- | --- | ---
S6 integration closure | Orchestrator | this runbook | No | integrate script, fixture, and docs evidence
S7 gate verdict | Quality Gate | Opus final review output | No | review after validation evidence exists
S7 gate outcome append and replay coordination | Orchestrator | this runbook | No | rework if gate fails
Gate-requested rework | Owner named by Gate Decision | refreshed artifacts | Deferred field | required only if gate fails
Re-gate after corrective work | Quality Gate or named re-gate owner | fresh Gate Decision | Deferred field | required after blocking rework
S8 publish readiness verification | Orchestrator | validation summary | No | local docs and script repair
S8 publish, commit, submit, or check-in | Orchestrator if user asks | git evidence | No | user asked to implement; commit/push only if explicitly requested after this run

S1 Closure: Complete for non-publish exploration/local repair evidence. This run does not claim publish-ready boundary separation because Orchestrator and Implementer share the main Codex context.

## S2 Context Pack

Facts:
- Prior fixes clarified policy but did not mechanically reject invalid artifacts.
- The corpview run read the updated skill and still wrote invalid `S1`/`S7` artifacts.
- Valid harness records may be single runbooks, so validation must discover S1/S7 semantically rather than depend on file names.

Relevant Files:
- `scripts/validate_harness_run.py`
- `tests/fixtures/invalid/corpview-regression/`
- `tests/fixtures/valid/single-runbook/`
- `SKILL.md`
- `references/workflow-template-lite.md`
- `references/workflow-template.md`
- `references/artifact-registry.md`
- `references/checklists.md`
- `references/agent-prompts.md`

S2 Closure: Complete. Context pack is written before S3.

## S3 Task Graph

Task | Owner | Context Boundary | Inputs | Outputs | Writable Area | Acceptance
--- | --- | --- | --- | --- | --- | ---
Implement validator | Implementer | current Codex implementation context | S0-S2, Opus pre-mortem | script and fixtures | `scripts/`, `tests/fixtures/` | self-test passes, corpview fails, valid fixtures pass
Wire docs | Implementer | current Codex implementation context | validator contract | docs patch | skill docs | S1/S2/S7 require validator
Validate | Orchestrator | current Codex thread | patch | validation evidence | runbook | self-test, skill validation, diff check
Gate review | Quality Gate | external Claude gate context | final diff and evidence | gate verdict | runbook | no blocking findings

S3 Closure: Complete. Task graph is written before task-specific execution.

## S4 Execution Output Record

Implemented:
- `scripts/validate_harness_run.py`
- invalid regression fixtures under `tests/fixtures/invalid/`
- valid control fixtures under `tests/fixtures/valid/`
- docs wiring in `SKILL.md`, `README.md`, `agents/openai.yaml`, `references/artifact-registry.md`, `references/checklists.md`, `references/workflow-template-lite.md`, `references/workflow-template.md`, and `references/agent-prompts.md`

Validator behavior:
- discovers S1/S7/S8 semantically from Markdown sections rather than fixed file names
- accepts both single-runbook and separate-file valid fixtures
- rejects publish/pass/readiness claims when S1 lacks publish intent or contradicts non-publish intent
- rejects publishable partial/deferred/conditional boundary status
- rejects owner collisions after normalizing Main Codex/current-thread aliases
- rejects Quality Gate assignments to tool/runtime/validation evidence surfaces
- rejects S7 publish readiness when evidence says local-only or publish owner is unassigned

## S5 Runtime Evidence Record

Commands and results:
- `python scripts\validate_harness_run.py --self-test` returned `Self-test passed.`
- `python scripts\validate_harness_run.py exec-plans\active\2026-05-02-harness-artifact-validator` returned `Harness run validation passed.`
- `python scripts\validate_harness_run.py C:\proj\corpview\exec-plans\active\corpview-cost-profit-dera-chart-20260502` returned `Harness run validation failed.` with errors for missing publish intent, deferred boundary, owner collisions, tool-surface Quality Gate, missing S8 publish owner mapping, and local-only guarded publish conflict.
- `python C:\Users\wangsong\.codex\skills\.system\skill-creator\scripts\quick_validate.py .` returned `Skill is valid!`.
- `git diff --check` returned only Windows LF-to-CRLF warnings and no whitespace errors.

## S6 Integration Ledger

Artifact | Owner | Evidence | Decision
--- | --- | --- | ---
Validator script | Implementer | self-test passed | Accepted
Corpview regression fixture | Implementer | fails validation before S2 | Accepted
Valid single-runbook fixture | Implementer | passes validation | Accepted
Docs wiring | Implementer | skill validation passed | Accepted
Opus final gate | Quality Gate | pending | Pending

## S7 Gate Decision

Gate: Harness artifact validator repair
Verdict: Pass
Owner: Opus Quality Gate via `delegating-with-claude`
Session: `16e26469-b58c-4268-8f59-ee59b012b4d1`
Blocking: None
Evidence:
- Corpview regression fixture and real corpview run fail validation before S2.
- Valid single-runbook and separate-file fixtures pass.
- Docs wire the validator into S1 closure / S2 entry and S7 gate.
- `quick_validate.py` passed and `git diff --check` had no whitespace errors.
Residual Risks:
- unusual owner aliases or role-name variations may need future parser expansion
- validator remains a required command rather than an automatically invoked runtime hook
- publish/readiness detection is regex-based and depends on standard artifact wording
Return Step: N/A
Rework Owner: N/A
Re-gate Owner: N/A
Due Before: N/A

## S7 Delta Gate

After the initial Opus gate, `Orchestrator` found and fixed one false positive: non-publish runbooks with `Verdict: Pass` and separate publish-related residual-risk prose were being treated as publish-readiness claims.

Delta:
- narrowed `_has_publish_claim` so publish claims must appear on the same line as pass/ready/guarded wording, or on `Decision:`, `Verdict:`, or `Status:` lines

Validation after delta:
- self-test still passed
- current non-publish repair runbook passed
- real corpview run still failed with guarded-publish/local-only conflict and S1 boundary errors
- `py_compile`, `quick_validate.py`, and `git diff --check` passed, with only CRLF warnings from git

Delta Gate:
- Owner: Opus Quality Gate via `delegating-with-claude`
- Session: `16e26469-b58c-4268-8f59-ee59b012b4d1`
- Verdict: Pass
- Blocking findings: None
- Residual risk: unusual split-line verdict formatting could bypass publish-claim detection; standard artifact format mitigates this.

Second Delta Gate:
- Change: `_has_publish_claim` now treats publish claims only on `Decision:`, `Verdict:`, or `Status:` lines, or on short all-uppercase verdict-like lines. Ordinary explanatory prose no longer creates publish-readiness claims.
- Validation: self-test passed, current non-publish repair runbook passed, and the real corpview run still failed.
- Owner: Opus Quality Gate via `delegating-with-claude`
- Session: `16e26469-b58c-4268-8f59-ee59b012b4d1`
- Verdict: Pass
- Blocking findings: None
