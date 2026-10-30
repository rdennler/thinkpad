# Format — reverse-engineering inventory

Location: `envs/<env>/reverse-engineering/inventory.md`. One entry per target; this is the pause/resume ledger for `tp:reverse-engineer`.

```markdown
## <target name> — <url or repo>

**Kind:** web | source
**Status:** active | paused | done
**Authorization:** <public site / owned by learner / permission from X — one line>
**Last touched:** YYYY-MM-DD
**Current rung:** <rung number and name>
**Just finished:** <one line>
**Next move:** <specific>
**Energy:** <low / medium / high>

### Evidence cards

- **R2 Surface** — <one-line finding> · evidence: `<selector or file:line>`
- **R3 Wire** — `GET /api/x` returns `{ids: [...]}` · evidence: request #4
```

## Rules

- A new target with no entry gets a new entry at rung 1.
- A resume phrase naming a known target continues from its **Next move** with zero recap. The entry's **Kind** picks the ladder.
- Evidence cards are one line each: a finding plus a pointer. **Never** store tokens, cookies, session ids, or personal data; write `<redacted:kind>`.
- "Done" means all rungs landed, including the rebuild.
