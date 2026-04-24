# Harness Engineering Workflow Template

Abstracted from the OpenAI article "Engineering for Agents: Building with Codex in an Agent-First World" dated 2026-02-11.

Use this when:
- multiple agents must be started for research, design, implementation, review, or repair work
- you want to shift humans from personally doing the work to designing the environment, clarifying intent, and building feedback loops
- you want to reduce context drift, repeated work, review bottlenecks, and AI residue spread

Do not use this when:
- there is no stable repository or record system
- the environment cannot provide basic tooling, validation, or a minimum quality gate
- the task itself is highly ambiguous and the goal cannot converge quickly

## 1. First Principles

1. Humans steer; agents execute.
2. Fix the environment before blaming the model.
3. The repository is the record system; knowledge outside the repo does not exist by default.
4. `AGENTS.md` is an index, not an encyclopedia.
5. Use progressive disclosure for context; never dump everything at once.
6. Constraints must be mechanically enforced, not merely documented.
7. UI, logs, metrics, and traces must be readable by agents.
8. At high throughput, waiting costs more than correction; workflows should move in small fast steps.
9. Continuously manage entropy and clean up residue by encoding human taste into system rules.
10. Eliminate non-coding bottlenecks first, especially validation, testing, deployment, troubleshooting, and review.
11. Keep context design stable where possible: prefer append-only updates and avoid rewriting stable prefixes.
12. External feedback is the primary counterweight to hallucination; do not rely only on model-internal reasoning.
13. Any change that depends on pre-existing state must be validated against a real pre-existing state surface.
14. When a single agent approaches context limits, split with subagents rather than forcing everything into one window.
15. By default, humans shift from line-by-line reviewers to result acceptors.

## 2. Operating Model

### Human Responsibilities

- define goals, non-goals, constraints, and success criteria
- design the execution environment, state transitions, and quality gates
- intervene only for disputes, priorities, acceptance criteria, and release decisions

### Agent Responsibilities

- retrieve, decompose, implement, validate, review, and refactor
- produce inspectable outputs under fixed contracts
- use standard tools to read code, logs, tests, and runtime signals directly

### Default Rule

If a task fails, ask first:
- what tooling is missing
- what structure is missing
- what constraints are missing
- what records are missing
- what feedback loop is missing

Do not ask why the agent was "not trying hard enough" before you ask those questions.

## 3. Required Environment

Before starting, the workflow should at minimum have this skeleton:

```text
repo/
  AGENTS.md
  ARCHITECTURE.md
  docs/
    design-docs/
    product-specs/
    references/
  exec-plans/
    active/
    completed/
  generated/
  scripts/
  tools/
```

Environment requirements:
- `AGENTS.md` keeps only entry points, navigation, role rules, and hard no-go zones
- `docs/` stores real knowledge; do not hide key constraints in chat history
- `exec-plans/` records plans, decision logs, progress, and rollback points
- `generated/` stores regenerable assets such as schemas, indexes, and derived documents
- `scripts/` and `tools/` allow agents to execute common operations directly
- tools should prefer structured output over long natural-language explanations
- error messages must be clear enough to support agent reflection and correction
- high-frequency tools should prefer low latency to avoid idle feedback loops
- keep system instructions and core prefixes as stable as possible to reduce context cache invalidation

AI-friendly tools to prioritize:
- LSP or static analyzers
- unit, integration, and acceptance test entry points
- browser automation or UI validation tools
- log, metric, and trace query entry points
- deployment, rollback, and rollout-status read interfaces

## 4. Standard Roles

| Role | Objective | Inputs | Outputs | Must Not Do |
|---|---|---|---|---|
| `Orchestrator` | split work, assign, converge | goals, constraints, source material | `Task Brief`, `Task Graph`, `Integration Ledger`, `Decision Log` | deeply substitute for other agents on specialist subproblems |
| `Source Analyst` | extract facts, evidence, and terminology | raw materials | `Claims List`, `Evidence Map`, `Glossary` | design the solution directly |
| `Principle Mapper` | abstract engineering principles from material | claims, evidence | `Principle Set`, `Mapping Table` | write implementation details |
| `Workflow Designer` | design steps, dependencies, and fallbacks | principles, task goals | `Workflow Draft` | overstep into arbitration |
| `Implementer` | produce code or documentation outputs | task brief, context pack | patch, draft, tests | rewrite upstream goals |
| `Runtime Verifier` | produce runtime evidence against real state surfaces | task graph, context pack, running system state | `Runtime Evidence Record` | substitute synthetic state for the required pre-existing state without explicit approval |
| `Critic` | find gaps, conflicts, and risks | drafts, process records | `Risk Register`, `Revision Requests` | become the primary narrative writer |
| `Quality Gate` | decide whether the work passes gate review | artifacts from all phases | `Pass`, `Conditional Pass`, `Fail` | modify the content directly |
| `Template Editor` | package the result into reusable assets | approved content | `Reusable Template`, `Runbook` | change the core conclusions |
| `Human Decision Maker` | make directional decisions | pending decisions, residual risks | `Decision Log` | fall back to executing every detail personally |

Artifact schemas and ownership are canonical in `artifact-registry.md`.

For escalation thresholds, count distinct workflow roles that need active ownership in the current run, not task count or subtask count.
`Runtime Verifier` may be added to `Lite` without immediate escalation when it is the only optional role beyond the default four and the workflow still centers on one primary implementation path.

## 5. Phase-by-Phase Workflow

### Step S0. Task Brief

Objective:
Compress the work into one task statement so multiple goals do not run together.

Inputs:
- user request
- source material
- time, scope, and delivery constraints

Method:
- define `Goal`
- define `Non-goals`
- define `Constraints`
- define `Success Criteria`
- define `Human Decision Points`

Outputs:
- `Task Brief`

Acceptance:
- the goal is singular
- completion can be judged
- non-goals are explicit

Fallback:
- if the goal is ambiguous, do not start downstream agents

### Step S1. Environment Design

Objective:
Design the execution environment before starting agents.

Inputs:
- `Task Brief`

Method:
- define directory structure
- define file naming
- define a unified output format
- define status, version, and log fields
- define read and write boundaries
- record whether explicit user-visible delegation is available for the run
- define `Role Owner Table`
- mark whether the run is intended for final publish and whether required separation is mechanically satisfied
- enforce tier-specific owner separation before downstream work starts

Outputs:
- `Execution Environment Spec`
- `Role Owner Table`

Acceptance:
- all agents use the same skeleton
- artifacts can be merged, traced, and audited
- every role already has a clear owner
- a `Full` workflow intended to pass final gate and publish uses at least 3 distinct owners
- a publishable `Full` workflow maps those owners to at least 3 distinct delegated agent identifiers from explicit user-visible subagents before downstream execution starts
- each delegated agent identifier maps to only one owner within the run
- hidden or background-only tool-driven delegation such as `spawn_agent` does not satisfy the delegated-agent requirement for this skill
- if required explicit user-visible delegation is unavailable or not allowed, stop as a fatal `Boundary Integrity` failure and tell the user final-result quality is uncontrollable
- in a publishable `Full` workflow, `Implementer`, `Critic`, and `Quality Gate` have different owners
- in a publishable `Full` workflow, `Quality Gate` does not share an owner with `Orchestrator`

Fallback:
- if outputs cannot be merged cleanly, fix the environment before continuing

### Step S2. Context Packaging

Objective:
Distribute the minimum context needed for each role.

Inputs:
- `Execution Environment Spec`
- raw materials

Method:
- split into `Core Context`
- split into `Optional Context`
- define `Forbidden Scope`
- label facts, inferences, and unknowns
- keep a stable prefix and append only task-state context at the end
- turn high-reuse instructions into stable system rules instead of rewriting them every round
- compress long histories into status summaries instead of replaying full transcripts

Outputs:
- one `Context Pack` per role

Acceptance:
- each agent receives only what is required for the current task
- key sources are traceable
- core prefixes stay as stable as possible
- new context is primarily appended rather than repeatedly rewritten

Fallback:
- if overreach and hallucination rise, shrink context and increase constraints

### Step S3. Task Graph

Objective:
Break the task into subproblems that can run in parallel and be accepted cleanly.

Inputs:
- `Task Brief`
- `Context Pack`

Method:
- define parallel blocks
- define serial dependencies
- define owner
- bind delegated agent identifiers where explicit user-visible delegation is available
- define named outputs and `Writable Area` for every task
- define termination conditions
- define human decision points
- identify any task whose correctness depends on pre-existing state and assign a `Runtime Verifier` or equivalent runtime-validation owner
- mark context-overload risk points
- predefine subagent split strategies for high-complexity work
- for publishable delegated `Full` runs, instantiate the minimum required distinct explicit user-visible subagents before deep execution starts
- In `Full`, have `Orchestrator` publish `Task Graph` first, then have `Workflow Designer` consume that graph plus the mapped principles to publish `Workflow Draft` within the same `S3` stage.

Outputs:
- `Task Graph`
- `Workflow Draft` in `Full`, after `Task Graph` is published and `Workflow Designer` is active

Acceptance:
- every node has exactly one owner
- every delegated node is bound to one concrete agent identifier
- every delegated `Owner` / `Agent ID` pair matches the `Role Owner Table`
- dependencies are clear and there are no responsibility gaps
- no very long chain is forced into one agent

Fallback:
- if two agents are doing the same thing, refactor the task tree

### Step S4. Parallel Execution

Objective:
Let agents work in parallel within explicit boundaries.

Inputs:
- `Task Graph`
- role-specific `Context Pack`
- fixed output contract

Method:
- run analysis, design, implementation, and risk scanning in parallel where appropriate
- produce output in a unified format
- write intermediate results only to each role's own area
- use tool calls to obtain external factual feedback instead of text-only reasoning
- require real state-surface validation for any change whose correctness depends on pre-existing state
- split work to subagents when the primary agent's context pressure becomes too high

Outputs:
- the set of subtask artifacts

Acceptance:
- output fields are consistent
- conclusions can be traced to sources
- no role oversteps into final sign-off
- key steps are backed by external validation signals

Fallback:
- failures fall back only to the responsible node

### Step S5. Risk Scan

Objective:
Produce stable risk conclusions before gate review instead of hiding risk checks inside integration.

Inputs:
- the set of subtask artifacts
- `Runtime Evidence Record` when state-surface validation is required

Method:
- `Critic` scans source reliability, role boundaries, verifiability, context expansion, and tool friendliness
- `Critic` treats missing real state-surface validation as an open risk rather than closing it from static reasoning alone
- record every risk with evidence, owner, and required action

Outputs:
- `Risk Register`

Schema:
- `Risk`
- `Severity`
- `Evidence`
- `Owner`
- `Required Action`
- `Status`

Acceptance:
- key risks have explicit owners
- every high-risk item includes evidence and required action

Fallback:
- if a high-risk item cannot be assigned to an owner, fall back to `Task Graph`

### Step S6. Integration

Objective:
Converge from parallel divergence into one unified draft.

Inputs:
- outputs from all agents
- `Runtime Evidence Record` when state-surface validation is required
- `Risk Register`

Method:
- deduplicate
- disambiguate
- mark conflicts
- merge into one unified draft
- preserve an integration ledger with complete evidence fields
- append conflict resolution, human decisions, and gate-requested rework to the same `Decision Log`

Outputs:
- `Unified Draft`
- `Open Questions`
- `Integration Ledger`
- `Decision Log`

Ledger Schema:
- `Agent`
- `Claim`
- `Artifact Name`
- `Owner`
- `Evidence Source`
- `Decision`
- `Next Step Or Fallback`

Acceptance:
- no repeated narration
- conflicts are marked explicitly
- the mapping from principles to execution steps closes the loop
- conflict decisions are recorded instead of silently flattened

Fallback:
- if conflicts are substantial, hand them to `Critic` or a human for arbitration

### Step S7. Quality Gate

Objective:
Use a fixed rubric to decide whether the workflow can proceed.

Inputs:
- `Unified Draft`
- `Runtime Evidence Record` when state-surface validation is required
- `Risk Register`
- `Integration Ledger`

Method:
- apply the canonical gate rules from `checklists.md` strictly
- produce a `Gate Decision` that satisfies the canonical verdict, evidence, and replay requirements
- if `checklists.md` is temporarily unavailable, restore it from version control first; use the minimum rules in this section only when the workflow must continue, and realign with the canonical checklist before publish
- if `artifact-registry.md` is temporarily unavailable, restore it from version control first; do not rewrite `Gate Decision` field names from memory before it is restored; if no prior valid gate artifact exists to reuse, do not continue through the gate
- after gate review, `Orchestrator` must append the gate outcome to `Decision Log` before rework or publish

Outputs:
- `Gate Decision`

Gate Decision Schema:
- canonical field names live in `artifact-registry.md`

Acceptance:
- the `Gate Decision` conforms to the canonical rules in `checklists.md`
- blocking gate failures are not waved through

Fallback:
- do not enter `S7` without `Integration Ledger`
- use the canonical replay rules from `checklists.md`

### Step S8. Publish and Learn

Objective:
Publish the asset and capture improvements for the next round.

Inputs:
- the approved final draft

Method:
- verify that the latest `Gate Decision` verdict is `Pass` before publish starts
- freeze the version
- record decisions
- summarize rework patterns
- extract reusable rules

Outputs:
- `Published Version`
- `Decision Log`
- `Next Iteration Notes`

Decision Log Owner:
- produced by `Orchestrator` by default
- if `Human Decision Maker` exists, that role's final decision must be appended to the same `Decision Log`

Published Version Owner:
- produced by `Template Editor` by default
- if a separate publish owner is assigned for the run, that owner may publish instead

Decision Log Schema:
- `Decision`
- `Decision Owner`
- `Reason`
- `Affected Artifact`
- `Recorded At`
- `Next Step`

Acceptance:
- reusable
- traceable
- ready to run again next time
- result acceptance is clear and does not depend on line-by-line human review
- `Full` runs missing required explicit user-visible delegation or owner separation are fatal `Boundary Integrity` failures and may not be presented as publish-ready
- final publish evidence includes at least 3 distinct delegated agent identifiers across the required separated owners

Fallback:
- if oral explanation is still required, return to the templated steps and fill in the missing skeleton

## 6. Mechanical Constraints

All agents must obey:

- answer only the questions owned by their role
- label all conclusions as `Fact`, `Inference`, or `Open Question`
- do not silently rewrite upstream assumptions
- do not consume undeclared context
- do not modify the shared final-draft area unless explicitly authorized
- do not claim completion without meeting acceptance criteria

Suggested unified output fields for analysis, design, and execution roles:

```text
Objective
Inputs
Method
Outputs
Acceptance
Risks
Escalation
Fact / Inference / Open Question
```

When a role is required to produce a canonical artifact schema such as `Gate Decision` or `Decision Log`, that role-specific schema overrides the default field set above.

## 7. Quality Gates

Canonical gate definitions live in `checklists.md`.
This template assumes:
- blocking gates must pass before publish
- `Risk Register` and `Integration Ledger` are required inputs to gate review
- `Runtime Evidence Record` is a required input to gate review whenever correctness depends on pre-existing state
- gate decisions follow the canonical field-population and replay rules in `checklists.md`
- `Reusability` and `Entropy Control` are non-blocking by default unless the task explicitly makes them release-critical

## 8. Observability and Entropy

### Observability

For every step, record:
- input version
- executing agent
- timestamp
- core conclusion
- reason for failure
- fallback target

Prefer signals that agents can read directly:
- UI state
- DOM snapshots
- screenshots
- logs
- metrics
- traces
- test results
- LSP diagnostics
- deployment and rollout status
- structured error codes and locations

### Entropy Control

- maintain glossaries in one place
- keep `AGENTS.md` short
- inject background knowledge progressively instead of broadcasting the whole package
- run periodic refactor and cleanup work
- encode gold principles into rules, lint, or structural tests
- prefer append-only context growth instead of repeatedly rewriting stable prefixes
- summarize long histories periodically to avoid ReAct loops exploding the context
- force a summary or a subagent split when there are more than 3 unresolved questions, more than 2 rework rounds on the same step, or more than 4 upstream artifacts to reread

## 9. AI-Friendly Tooling Heuristics

When designing tools for agents, prioritize three properties:

1. Fast
- the slower the feedback, the higher the autoregressive waiting cost for the agent

2. Structured
- return clear fields, status values, and locations instead of vague narration

3. Clear Errors
- good error messages are often more valuable than success messages
- errors must help the agent localize, reflect, and repair quickly

Capabilities that are good candidates for tool interfaces:
- code diagnostics
- test execution
- page interaction and screenshots
- deployment status reads
- log and trace queries
- acceptance checks

## 10. Minimal Example

Scenario:
Read an engineering article and produce a reusable multi-agent workflow template.

Minimal execution order:

1. `S0` `Orchestrator` writes `Task Brief` and opens `Decision Log`
2. `S1` `Orchestrator` produces `Execution Environment Spec` and `Role Owner Table`
3. `S2` `Orchestrator` produces `Context Pack`
4. `S2` `Source Analyst` extracts claims and evidence from the article
5. `S2` `Principle Mapper` compresses them into engineering principles
6. `S3` `Orchestrator` produces `Task Graph`
7. `S3` `Workflow Designer` consumes `Task Graph` and produces `Workflow Draft`
8. `S4` `Implementer` executes and produces `Execution Output Record`
9. `S4` `Runtime Verifier` validates real state surfaces and produces `Runtime Evidence Record` when required
10. `S5` `Critic` produces `Risk Register`
11. `S6` `Orchestrator` produces `Integration Ledger` and updates `Decision Log`
12. `S7` `Quality Gate` decides whether the work passes gate review
13. `S7` `Orchestrator` appends the gate outcome to `Decision Log`
14. `S8` `Template Editor` packages the final template
15. `S8` humans arbitrate disputes and version freeze only, then append `Decision Log`

## 11. Anti-Patterns

- one giant `AGENTS.md`
- knowledge trapped in chat tools
- using "add more prompting" instead of building the system
- multiple agents modifying the same final draft at the same time
- merging directly with no quality gate
- writing only the happy path and ignoring exception paths
- manually cleaning AI residue without systematizing the rules
- rewriting the system prompt or stable prefix every round
- leaving validation, testing, deployment, and troubleshooting as human fallback work
- lacking structured error feedback, so the agent cannot correct quickly
- insisting on a single agent even when the context has already overflowed
- keeping humans in line-by-line review instead of result acceptance

## 12. Starter Checklist

- [ ] goals, non-goals, and success criteria are defined
- [ ] `AGENTS.md` is an entry point, not an encyclopedia
- [ ] key knowledge has been moved into the repo
- [ ] role boundaries are clear
- [ ] output contracts are clear
- [ ] acceptance criteria are clear
- [ ] fallback paths are clear
- [ ] observable signals are directly readable by agents
- [ ] ongoing entropy control exists
- [ ] humans retain only critical arbitration responsibilities
- [ ] high-frequency tools are fast, structured, and have clear errors
- [ ] core prefixes are stable and context is append-first
- [ ] a subagent strategy is already defined for single-agent overload
- [ ] human acceptance focuses on results and metrics, not line-by-line rechecking
