# Format — session-state.md (bookmark)

Location: `envs/<env>/session-state.md`. **Always overwritten, never appended.** A pointer, not a log.

```markdown
**Last touched:** YYYY-MM-DD
**Current unit:** <week / module / level / exercise>
**Just finished:** <one line>
**Next move:** <specific action, file, and item — never "continue">
**Energy:** <low / medium / high>
```

## Rules

- No timestamps, no minutes.
- **Next move** must be executable cold, e.g. "do problem 3 from `roadmap.md` unit 2", not "continue unit 2".
- An env may carry extra sections below the header (a deadlines table, a glossary). Preserve them verbatim on every overwrite.
- **Next move** may carry tutor-directed notes in italics (a pending Socratic question, "stay Socratic, do NOT write the test code"). This is encouraged for mid-thought pauses.
