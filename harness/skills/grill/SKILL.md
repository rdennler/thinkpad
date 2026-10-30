---
name: grill
description: Quiz, test or take-home assignment on material the learner has already covered in an env, keyed to their current position. Triggers on "quiz me", "pop quiz", "test me", "test time", "give me an assignment", "grade my assignment". Manual invocation only.
metadata:
  api: 1
  kind: engine
  mode: socratic
  terminal: forbidden
  triggers: ["quiz me", "pop quiz", "test me", "test time", "give me an assignment", "grade my assignment"]
  reads: ["envs/<env>/session-state.md", "envs/<env>/progress.md", "envs/<env>/grill/history.md", "envs/<env>/assignments/"]
  writes: ["envs/<env>/grill/history.md", "envs/<env>/progress.md", "envs/<env>/assignments/"]
  requires: []
---

# tp:grill — Quiz, Test, Assignment

One engine, three modes. The phrase picks the mode: "quiz me" → **quiz**, "test me" → **test**, "give me an assignment" / "grade my assignment" → **assignment**. Everything outside the mode table below is shared and binding.

## Which envs

Any env with `grill = true` in its `env.toml`. Envs with nothing quizzable (pure creative drafting) set `grill = false`. If an env limits scope ("theory only"), its `CLAUDE.md` says so under **Grill scope**; obey it.

**Resolving the env:** a named env or topic wins; else the env of the active session; else ask. Never guess.

## What counts as learned

1. Read the env's `session-state.md`. Eligible material is everything up to that position, **never ahead of it**.
2. Read `progress.md` for clicked / fuzzy signals, and recent `memory/retros/` entries if present.
3. Read `grill/history.md` in full for past questions and misses. Never repeat a question, verbatim or as a trivial reskin; a new angle on an old topic is the point.
4. Weighting: recency-biased. The last 1–2 sessions dominate, older material is interleaved for retention, and anything missed or marked fuzzy is weighted **up**.
5. An inline override ("quiz me on the dark stage only", "3-question quiz") narrows scope or size; all other rules hold.

## The modes

| | quiz | test | assignment |
|---|---|---|---|
| **Register** | low-stakes reinforcement | exam | take-home, integrates recent material |
| **Size** | 5–8 questions, mixed formats (recall, apply, spot-the-error, translate) | 12–20 questions in sections Recall → Application → Integration; integration spans several units | one task, small by default; needs two or more recent ideas, never drills one atom |
| **Feedback** | right after each answer: confirm, correct, or nudge | **none until every answer is in**: no hints, no Socratic rescue. State the section structure and an honor-system time cap up front. This override beats the env contract mid-test; the contract resumes at grading | none until the learner brings it back |
| **Artifact** | chat only | chat only | `envs/<env>/assignments/YYYY-MM-DD-<slug>.md` (create the folder on first use): task, scope, concrete **acceptance criteria**, space for the work. No due dates, no nagging |
| **Grading** | running | all at once: per-section breakdown, total, weak spots | on "grade my assignment": against the stated acceptance criteria only, no goalpost moves. Append a graded header (date, score, weak spots) to the file; never rewrite the learner's work |

## Grading and debrief (all modes)

- Score is a plain fraction plus percent (11/14 — 79%) and a weak-spot list. No letter grades, no pass/fail. **Never guilt.**
- **The debrief is the point, not the score.** Walk each miss topic by topic until it clicks, Socratically where the env is Socratic.
- Grade code by reading, never by running.
- **Anki cards on request only.** The learner phrases the card (`tp:anki`). Offer once at the end of the debrief; never force.

## Write-backs (after every graded session)

1. Append the session to `envs/<env>/grill/history.md` in the shape from `references/grill-history.md`. Create the file on first use.
2. Append one summary line to the env's `progress.md` (mode, scope, score, weak spots). The swim lane picks it up from there. **Never write `tracker/progress.md` directly.**

## Rules

- Register follows the env's own contract (`env.toml` `register`, and `tutor.md`).
- **Manual invocation only.** No cadence, no auto-routing from `tp:session`, no new standing obligations.
