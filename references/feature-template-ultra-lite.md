# Feature Template Ultra Lite

Use this when:
- a single small feature
- a single bugfix
- a small documentation or configuration change
- no parallel multi-agent work is needed
- no full risk scan or integration ledger is needed
- one owner and one direct validation path are enough to justify final publish

Do not use this for:
- cross-module refactors
- work that needs multiple roles in parallel
- complex validation chains
- unclear requirement boundaries
- work that is likely to require multiple rework rounds
- changes that affect correctness-critical behavior such as integrity, durability, recovery, ordering, security, or externally visible contract semantics

## 1. Fill This In

```text
Goal:

Scope:

Constraints:

Owner:

Validation:

Done When:
```

## 2. Minimal Flow

1. Write `Goal` and `Done When` clearly.
2. Assign a single `Owner`.
3. Execute the change.
4. Validate with the most direct external feedback available.
5. Stop once `Done When` is satisfied.

## 3. Default Rules

- Do not split into multiple agents by default.
- Do not create a `Risk Register` by default.
- Do not create an `Integration Ledger` by default.
- Do not open the full quality gate by default.
- `Ultra Lite` is intentionally single-owner. Do not simulate role separation inside this tier; escalate instead.
- Any change that depends on pre-existing state must still be validated against a real pre-existing state surface.
- Prefer the shortest validation loop that can close the task.
- Humans review the result, not every line.
- Default `Owner` maps to `Implementer`.
- Add an `Orchestrator` only when the goal, scope, or acceptance criteria are still unclear.
- If you need a role prompt, start with `Implementer`; add `Orchestrator` only when boundaries remain unclear.
- A final publish from `Ultra Lite` is acceptable only when the task remains low-risk, tightly bounded, and closed by one strong validation path.

## 4. Validation Options

Pick the cheapest and most direct option first:
- unit tests
- manual or automated page verification
- LSP / lint / typecheck
- logs or API response checks
- successful build

Rules:
- A successful build alone is not enough for correctness-critical changes.
- If correctness depends on pre-existing state, validate against the real existing surface that matters; a freshly seeded substitute is not automatically equivalent.
- If validation depends on more than one independent signal to be credible, escalate to `workflow-template-lite.md`.

## 5. If Validation Fails

Handle it in this order:

1. If the scope is unchanged, the owner is unchanged, and the same validation path can still close the loop, let the current `Owner` fix it and retry once.
2. If the second attempt still fails, or the work starts to require a second owner, a second validation source, or more explicit risk tracking, escalate immediately to `workflow-template-lite.md`.
3. When escalating to `Lite`, convert the Ultra Lite fields into the canonical Lite artifacts below instead of copying labels forward verbatim.

`Task Brief` seed:

```text
Goal: <Goal>
Non-goals: <Out-of-scope items from Scope, or N/A>
Constraints: <Constraints>
Success Criteria: <Done When>
Human Decision Points: <Boundary calls that need a human, or N/A>
```

`Context Pack` seed:

```text
Core Context: <Current implementation facts and in-scope area>
Optional Context: <Related files, tests, logs, or prior notes>
Forbidden Scope: <Out-of-scope items from Scope>
Stable Prefix: <Reuse the current task wording if it is already stable>
Required Tools: <Validation path and required tools>
```

`Role Owner Table` seed:

```text
Role | Owner | Context Boundary | Shared? | Notes
Orchestrator | <Assign if needed for boundary clarification> | <Main or delegated context> | <Yes/No> | Add when Lite needs explicit coordination
Implementer | <Owner> | <Main or delegated context> | <Yes/No> | Carried forward from Ultra Lite
Runtime Verifier | <Assign when state-surface validation is needed> | <Main or delegated context> | <Yes/No> | Add when correctness depends on pre-existing state or independent dynamic verification
Critic | <Assign> | <Main or delegated context> | <Yes/No> | Required in Lite
Quality Gate | <Assign> | <Main or delegated context> | <Yes/No> | Required in Lite
```

## 6. Escalate To Lite If

Escalate to `workflow-template-lite.md` if any of the following is true:
- a second owner is needed
- multiple validation sources are needed
- correctness depends on pre-existing state and the real state surface is not trivially available to the single owner
- the second rework round would be needed
- the scope starts expanding
- requirement boundaries need human arbitration
- explicit risk tracking needs to be preserved
- an external context is assigned to `Critic` but not `Quality Gate` while the main context owns implementation, because `Lite` must apply the `External-Critic-Only Quality Gate Rule`
- the only available validation is a weak validation path from Section 4, such as a successful build or a coarse manual check
- the task affects correctness-critical behavior such as integrity, durability, recovery, ordering, security, or externally visible contract semantics
- the task would need role separation to make the final publish decision credible

## 7. Example

```text
Goal:
Fix the incorrect default value for the date filter on the gallery page.

Scope:
Change only the frontend filter initialization logic. Do not change the backend API.

Constraints:
Do not change the existing API contract. Do not affect other filters.

Owner:
Implementer

Validation:
Open the page locally, confirm the default date is correct, and run the related frontend tests.

Done When:
The page shows the correct default date, the tests pass, and there are no console errors.
```
