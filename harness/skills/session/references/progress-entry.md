# Format — progress.md entry (journal)

Location: `envs/<env>/progress.md`. **Append-only.** `tp:session` writes an entry on `wrap up`, never on pause or checkpoint. `tp:grill` appends one summary line after grading; nothing else writes here.

```markdown
## YYYY-MM-DD — <unit / exercise / module>

- **Did:** <one or two lines>
- **Clicked:** <what landed>
- **Still fuzzy:** <what didn't>
- **Interactions:** <one aggregate sentence from the interaction log, if the env keeps one>
- **Next session starts with:** <specific pointer>
```

## Rules

- One entry per wrap-up, newest at the bottom. Never edit or delete past entries (`reset week` included).
- **Clicked** and **Still fuzzy** are retro fuel. Keep them honest and concrete; `tp:retro` harvests them.
- No minutes. Counts of sessions or cards are fine.
- On wrap-up this entry is written **and** the swim-lane row is updated and today's box ticked (see `swim-lane.md`).
