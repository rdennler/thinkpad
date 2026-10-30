# Format — Retro Files

## Retro file — `memory/retros/YYYY-MM-DD-<env>.md`

`<env>` is the env folder name, lowercase. A second retro the same day gets suffix `-2`.

```markdown
# Retro — <env> — YYYY-MM-DD

## Summary

<2–4 lines: period covered, what was worked on, overall read.>

## Learnings

- <durable insight, concrete: what clicked and why>

## Mnemonics & Reframes

- **<name>** — <expansion / the reframe and when it applies>

## Friction

- <what dragged: environment, format, pedagogy, scheduling>

## Proposed Changes

- <change to the env or a skill — proposal only, never applied here>
```

An empty section keeps its heading and says `*None.*`

## Improvement queue — `memory/retros/improvement-queue.md`

Append-only checklist, one line per actionable proposal:

```markdown
- [ ] [my-env] 2026-01-15 — Add a "trace it on paper" rung to the hint ladder for pointer bugs
```

- The env tag is the env folder name in brackets; use `[platform]` for cross-env items.
- Humans (or the `retro-reflector` subagent) work the queue. `tp:retro` only appends. Checked items stay.

## Proposal drafts — `memory/retros/proposals/`

Drafted **only by the `retro-reflector` subagent**: one file per queue item, `YYYY-MM-DD-<slug>.md` or `.diff`, holding the concrete new text for human review in git. `tp:retro` never writes here and never edits skills in place.
