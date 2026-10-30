---
name: session
description: Names today's block and keeps every env's state files. Triggers on "what should I do today", "plan my day", resume, pause, checkpoint, status, meditate, wrap up, reset week, swim lane, "where was I", "done for today", "save my spot", or any session start where no env is named.
metadata:
  api: 1
  kind: engine
  mode: infra
  terminal: plumbing
  triggers: ["what should I do today", "plan my day", "resume", "pause", "checkpoint", "status", "meditate", "wrap up", "reset week", "swim lane", "where was I", "done for today"]
  reads: ["envs/*/env.toml", "envs/<env>/session-state.md", "envs/<env>/progress.md", "envs/<env>/interactions.jsonl", "tracker/progress.md"]
  writes: ["envs/<env>/session-state.md", "envs/<env>/progress.md", "tracker/progress.md"]
  requires: []
---

# tp:session — Where Am I, What Now

Two jobs: name today's block, and keep each env's bookmark and journal. The bird's-eye view is `tracker/progress.md`.

## Session start

1. **No folder under `envs/`?** Say "No envs yet. What do you want to learn?" and hand off to `tp:new-env`. Nothing else.
2. **No env named?** Today's scheduled block wins (below). "Most recently touched" is never a routing rule: it keeps routing into whatever the learner just did, and a Tier-1 env with zero blocks can never surface.
3. **Name the block first**, in one short line, before any other observation: "Today is Wed → my-env." A Tier-1 env that has never run outranks a stale one; say the count out loud ("my-env is 0 for 2 scheduled blocks"). Stale-env notes, debt and leech counts come after and never override the schedule.
4. Route into the env with `tp:learn` and run **resume**.

## Schedule

There is no hand-written weekly plan; the schedule is derived from each env's `env.toml`. The same rule is code in `thinkpad/schedule.py`, shown by `thinkpad-status`.

| Key | Meaning |
|---|---|
| `tier` | `1` primary, `2` secondary, `3` opportunistic, or `"sprint"` (temporary override with an `expires` date) |
| `cadence` | Days this env owns, e.g. `["mon", "thu"]`. A day may carry a slot: `"sat-am"`, `"sun-pm"` |
| `status` | `active` · `paused` · `archived`. Only `active` envs are routed |
| `expires` | Sprint envs only. After this date the env counts as `archived` |

1. Establish today's date and weekday. Collect `active` envs whose `cadence` includes today.
2. An unexpired `sprint` env outranks everything; otherwise Tier 1 outranks 2 outranks 3. Tied envs: the older bookmark wins.
3. If today's block is already ticked in the swim lane's Section 3, offer the next slot or rest. Never schedule the same env twice in one day.
4. No cadence match is a rest day. Say so. Do not invent a block.
5. Evening or catch-up slots go to Tier 2 and 3 only, never stacked. Paused and archived envs are never auto-routed; they still work if the learner names them.
6. Sessions are **named blocks, not durations**. Skipping one is guilt-free; "showed up" is the only metric.

## Two files per env

- **`envs/<env>/session-state.md`** is the bookmark. **Always overwritten, never appended.** A pointer, not a log. Shape: `references/session-state.md`.
- **`envs/<env>/progress.md`** is the journal. **Append-only.** This skill writes it only on `wrap up`; `tp:grill` appends its own one-line summary after grading. Shape: `references/progress-entry.md`.

## Actions

| Phrase (or natural variant) | Action |
|---|---|
| `resume` / "where was I?" / "pick up" | Read the env's `session-state.md` and `progress.md`. Continue from **Next move** with **zero recap**. |
| `pause` / "stopping here" / "gotta go" | **Overwrite** `session-state.md`. One-line confirm. Do not touch `progress.md`. |
| `checkpoint` / "save my spot" | Same as `pause`, but the session continues. |
| `status` / "where are we?" | One line: env / current unit / next move. |
| `meditate` / "how did that go" | Read today's lines from `interactions.jsonl` (`grep '"date": "<today>"'`, never the whole file). Reflect back 2–3 of the learner's own quotes: one thing derived unaided, one outcome-0 item. Ask them to re-explain the 0 in their words. Skippable; runs before `wrap up`. |
| `wrap up` / "done for today" | Overwrite `session-state.md`, append the entry to `progress.md`, update the env's row in `tracker/progress.md`, tick today's box. |
| `reset week` | Confirm once; then blank **Next move** back to the start of the current unit. Never delete `progress.md` entries. |
| `swim lane` / "bird's-eye" | Full refresh of `tracker/progress.md` (`references/swim-lane.md`). Report in one short paragraph. |

## Interaction log

Shape and reading rules: `harness/skills/learn/references/interaction-log.md`.

- **On `resume`:** after naming today's block, ask ONE retrieval question rebuilt from the env's last `outcome: 0` line: `grep '"outcome": 0' envs/<env>/interactions.jsonl | tail -1`. No file means skip.
- **On `meditate` / `wrap up`:** fold one aggregate sentence into the journal, e.g. `Interactions: 7 logged — 5 landed, 1 missing-prereq (fractions), 1 productive-struggle.` `productive-struggle` never counts against the tutor.

## Invariants

1. Bookmarks are overwritten, never appended. Journals are appended, never edited.
2. Never re-explain on resume unless asked.
3. **Next move** is specific (a file, an item, an action), never "continue".
4. `wrap up` also touches the swim lane.
5. Preserve any extra sections an env keeps below a file's standard header.
6. **No minutes.** Never put minutes in a journal entry, bookmark, swim lane, or reply; never total or average time. Counts of sessions and cards are fine.

## Optional hook: Anki

If Anki is set up (`harness/plugins/anki/`): on `resume`, run the leech check (`tp:anki` → Review) and offer a relearn block, never force it. On `wrap up`, fold today's card count and fails into the journal. On "what should I do today", one leech line across envs after the block is named. Anki closed means skip silently.

## Pedagogy

Inside a learning session the `tp:learn` contract is binding. This skill only manages state files.
