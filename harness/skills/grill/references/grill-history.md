# Format — `envs/<env>/grill/history.md` (grill ledger)

Append-only journal of every `tp:grill` session (quiz, test or assignment) in an env. Read in full before generating questions (uniqueness and weighting); one dated section is appended after grading. Never edit prior sections.

```markdown
# Grill History — <env>

<!-- append-only; newest at bottom -->

## 2026-01-15 — quiz — photosynthesis — 6/8 (75%)

| # | Topic | Question gist | Result |
|---|---|---|---|
| 1 | inputs | name the two inputs and where each enters the cell | ✔ |
| 2 | light vs dark stage | which stage needs light directly, and why | ✘ |

**Weak spots:** light vs dark stage; where ATP is used.
**Debrief:** walked the two stages in order; clicked via a flow sketch. 1 Anki card made.
```

Rules:

1. Heading = `date — mode — scope — score`. Mode is quiz / test / assignment. An assignment's score is added at grading time.
2. **Question gist, not full text.** One line, enough to recognize a repeat.
3. Result: ✔ / ✘ / ½ (partial).
4. The weak-spots line is mandatory; it drives the next grill's weighting.
5. The debrief line: one sentence on what un-stuck the misses, plus the count of cards made (content lives in Anki and the graph).
6. Dates only, no timestamps.
