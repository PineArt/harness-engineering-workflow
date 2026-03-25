# Feature Template Ultra Lite

Use this when:
- a single small feature
- a single bugfix
- a small documentation or configuration change
- no parallel multi-agent work is needed
- no full risk scan or integration ledger is needed

Do not use this for:
- cross-module refactors
- work that needs multiple roles in parallel
- complex validation chains
- unclear requirement boundaries
- work that is likely to require multiple rework rounds

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
- Prefer the shortest validation loop that can close the task.
- Humans review the result, not every line.
- Default `Owner` maps to `Implementer`.
- Add an `Orchestrator` only when the goal, scope, or acceptance criteria are still unclear.
- If you need a role prompt, start with `Implementer`; add `Orchestrator` only when boundaries remain unclear.

## 4. Validation Options

Pick the cheapest and most direct option first:
- unit tests
- manual or automated page verification
- LSP / lint / typecheck
- logs or API response checks
- successful build

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
Role | Owner | Notes
Orchestrator | <Assign if needed for boundary clarification> | Add when Lite needs explicit coordination
Implementer | <Owner> | Carried forward from Ultra Lite
Critic | <Assign> | Required in Lite
Quality Gate | <Assign> | Required in Lite
```

## 6. Escalate To Lite If

Escalate to `workflow-template-lite.md` if any of the following is true:
- a second owner is needed
- multiple validation sources are needed
- the second rework round would be needed
- the scope starts expanding
- requirement boundaries need human arbitration
- explicit risk tracking needs to be preserved
- the only available validation is a weak validation path from Section 4, such as a successful build or a coarse manual check

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
