# Format — tracker/progress.md (the swim lane)

The bird's-eye view across all envs. The agent owns this file; never let it drift behind the per-env bookmarks. Created on first `swim lane` or `wrap up` if missing.

## Four sections (fixed order, fixed names)

### Section 1 — Where I Left Off

One row per `active` env; the env name links to its bookmark.

```markdown
| Env | Last Touched | Position | Next Move |
|---|---|---|---|
| **[my-env](../envs/my-env/session-state.md)** | YYYY-MM-DD | <unit> | <specific next move> |
```

### Section 2 — Upcoming Dates

External dates the learner has told you about (interviews, exams, deadlines), soonest first. Omit the section's table if there are none and write `*None.*`.

```markdown
| Due | Item | Env |
|---|---|---|
```

### Section 3 — This Week (date range in heading)

A checkbox grid built from the envs' `cadence` values:

```markdown
| Day | Block | Done? |
|---|---|---|
| Mon May 25 | my-env (Tier 1) | ☐ |
```

### Section 4 — Parking Lot

Bulleted items to revisit later. **Not actions for today.** Touched only when the learner asks.

## Maintenance

- **On `wrap up`:** update only the wrapped env's Section 1 row; tick today's Section 3 box.
- **On `swim lane`:** read every `active` env's `session-state.md`; rewrite Sections 1–2; rebuild Section 3 if it's a new week; leave Section 4 alone; report in one short paragraph.
