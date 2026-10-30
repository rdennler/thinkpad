---
name: retro
description: Retrospective engine for any learning env. Triggers on "retro", "retrospective", "run a retro on <env>", "let's debrief". Debriefs Socratically, files learnings, queues improvements.
metadata:
  api: 1
  kind: engine
  mode: socratic
  terminal: plumbing
  triggers: ["retro", "retrospective", "let's debrief"]
  reads: ["envs/<env>/progress.md", "envs/<env>/session-state.md", "envs/<env>/interactions.jsonl", "memory/retros/"]
  writes: ["memory/retros/", "memory/ontology/graph.jsonl"]
  requires: []
  graph_reads: ["Concept"]
  graph_writes: ["Learning", "Mnemonic", "Concept"]
---

# tp:retro — Retrospective Engine

Turns a stretch of sessions into durable memory and concrete improvements to the env or the harness. This is the session-level recursion loop: what the learner reports changes what the next sessions do.

## Procedure

### 1. Gather

Read the env's `progress.md` (mine **Clicked** and **Still fuzzy**) and `session-state.md`. Find the period since the last retro (the env's most recent file in `memory/retros/`). If the env keeps `interactions.jsonl`, run `python3 harness/scripts/interaction-stats.py envs/<env>/interactions.jsonl <start> <end>` for the period's register failure rate; it feeds lane 4.

### 2. Debrief (Socratic: the learner talks, you ask)

Walk four lanes, one at a time, each question grounded in something specific from the files. Question bank: `references/debrief.md`.

1. **What clicked.** Which ideas landed, and what made them land?
2. **What was hard.** Where did sessions stall, and what kind of stuck was it?
3. **What strategy emerged.** A repeatable move, mnemonic or reframe worth naming?
4. **What should change about the environment itself.** Contract, formats, hint style, pacing?

Never answer for the learner; reflect their words back and sharpen. 1–2 questions at a time.

### 3. Write the retro file

`memory/retros/YYYY-MM-DD-<env>.md` with sections Summary / Learnings / Mnemonics & Reframes / Friction / Proposed Changes. Exact shape: `references/retro.md`.

### 4. Queue improvements

Append each actionable proposal to `memory/retros/improvement-queue.md` as `- [ ] [<env>] YYYY-MM-DD — <concrete proposal>`.

### 5. Log to the graph (`tp:memory`)

Through `tp:memory` (`harness/scripts/ontology.py`), create each durable **Learning** (`about` → Concept, `part_of` → Env) and each **Mnemonic** (`reinforces` → Concept). Create missing Concept nodes first. The script refuses invalid writes; fix and retry. Confirm ids in one line.

## Hard rules

- **Retro never edits skills, env contracts, or plans.** Proposals only. The `retro-reflector` subagent drafts diffs into `memory/retros/proposals/`; a human reviews them in git.
- Debrief before writing. No learner input means no retro file; offer to reschedule instead.
- Proposals must be concrete enough to act on ("add X to `hint-ladder.md` rung 3"), not vibes ("improve hints").
- One retro file per run; never rewrite past ones.
