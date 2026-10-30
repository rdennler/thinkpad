# Interaction Log — `envs/<env>/interactions.jsonl`

Per-env, append-only JSONL. One line per **teaching moment**, not per message. Written live by whichever skill is running the learning session (`tp:learn`, `tp:reverse-engineer`); aggregated at `meditate` / `wrap up` by `tp:session`. Purpose: empirical data on which explanation strategies land, feeding the register review in `tp:retro`.

## Line shape (exact keys)

```json
{"date": "2026-01-15", "env": "my-env", "concept": "compound interest", "outcome": 1, "fail_reason": null, "note": "restated it as interest earning interest, unaided"}
{"date": "2026-01-15", "env": "my-env", "concept": "percent change", "outcome": 0, "fail_reason": "missing-prereq", "note": "added 20% twice and called it 40%"}
```

- **date**: session date, `YYYY-MM-DD`. No timestamps.
- **env**: the env folder name.
- **concept**: the specific idea in play, few words. Same wording as the graph node or Anki card when one exists.
- **outcome**: `1` = the learner parsed the question and engaged correctly. `0` = it didn't land.
- **fail_reason**: `null` when outcome is 1. When 0, exactly one of:
  - `jargon`: question wording above register. Fix: simpler words.
  - `two-ideas`: packed question. Fix: split it.
  - `missing-prereq`: sequencing hole. Fix: back up one concept. A misconception graph-node candidate.
  - `productive-struggle`: understood the question, wrestling with the idea. **Not a tutor failure.** Excluded from the register failure rate.
- **note**: one short line of evidence. A decisive quote of the learner's words is best.

## What counts as a teaching moment (log these, nothing else)

- A new concept introduced
- A hint-ladder escalation
- A gate check (verbalization gate, predict, restate)
- A quiz-style probe mid-session

## Reading rules: never read the whole file

It grows forever. Pull only the lines needed:

- Resume retrieval opener: `grep '"outcome": 0' envs/<env>/interactions.jsonl | tail -1`
- Meditate / wrap-up: `grep '"date": "<today>"' envs/<env>/interactions.jsonl`
- Register review: `grep -c` per `fail_reason` over a date range.

Raw lines never get copied into markdown files; the journal gets one aggregate sentence.

## Aggregation

Count today's lines per outcome and `fail_reason`. **Register failure rate = (jargon + two-ideas) / total.**
