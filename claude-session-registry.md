# Claude Session Registry

This file is the local registry for persistent Claude collaboration lanes.
Use it with `$delegating-with-claude`.

Purpose:
- avoid repeated Claude cold starts
- keep one stable Claude lane per long-lived collaboration pattern
- persist `SESSION_ID` in the workspace instead of relying on chat memory

## Default Policy

- prefer one fixed primary Claude lane for this template project
- reuse the same `SESSION_ID` on follow-up review turns unless context materially changes
- generate a compact structured handoff before each first-turn delegation
- on resume, do not resend the full handoff unless the context materially changed
- if the lane drifts too far from current context, create a new lane and mark the old one as archived

## Primary Lane

| Lane | Purpose | Skill | SESSION_ID | Status | Last Used |
|---|---|---|---|---|---|
| `claude-primary-review` | cross-model review, governance review, final sign-off | `$delegating-with-claude` | `ed88939f-53f7-4e4a-8f16-205de39ab230` | `active` | `2026-03-25` |

## Resume Rules

- first delegation:
  - synthesize a structured handoff
  - call `claude_delegate.py`
  - capture returned `SESSION_ID`
  - write it back into this registry
- follow-up delegation:
  - reuse the same lane and `SESSION_ID`
  - send only the new task or delta unless context materially changed
- lane reset:
  - create a new lane only when the previous Claude thread is no longer a good fit
  - preserve the old `SESSION_ID` as historical record

## Reset Modes

- `reuse`
  - keep the same lane and `SESSION_ID`
  - use when the task is still the same collaboration thread
  - send only the new delta unless context materially changed

- `refresh`
  - keep the same lane and `SESSION_ID`
  - regenerate a compact handoff
  - use when the task is still related, but the working summary needs cleanup

- `cold_start`
  - do not reuse the previous `SESSION_ID`
  - create a new lane or replace the primary lane with a new session
  - mark the old lane `archived` or `paused`
  - use when the old Claude thread has drifted, become noisy, or should be treated as a clean reviewer again

## Selection Rules

Choose `reuse` when:
- the task class is unchanged
- recent findings are still reliable
- only a small delta needs review

Choose `refresh` when:
- the task is still related
- the old thread is useful
- but the summary needs to be recompressed before continuing

Choose `cold_start` when:
- the task type changed materially
- the old thread accumulated too much stale context
- Claude starts reusing outdated conclusions
- you explicitly want a clean independent review

## Handoff Schema

Use the default compact schema from `$delegating-with-claude`:

- `summary`
- `relevant_files`
- `findings`
- `constraints`
- `next_step`

Optional:

- `repo_facts`
- `open_questions`

## Update Template

When a Claude session is created, update the primary lane row like this:

```text
| `claude-primary-review` | cross-model review, governance review, final sign-off | `$delegating-with-claude` | `<SESSION_ID>` | `active` | `<YYYY-MM-DD>` |
```

## Notes

- this registry is the persistence layer; chat memory is only a convenience layer
- when I say "reuse Claude lane", I should first consult this file
- unless you ask for more lanes, I will default to reusing `claude-primary-review`
