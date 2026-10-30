---
name: anki
description: Anki integration via AnkiConnect. Card creation from a learning session ("card this", "make a card"), and the review loop: leech check, review-count sync at wrap up, optional batched chat review ("anki review", "check my leeches"). Also called by tp:session on resume and wrap up.
metadata:
  api: 1
  kind: integration
  mode: infra
  terminal: plumbing
  triggers: ["card this", "make a card", "anki card", "anki review", "check my leeches", "anki stats"]
  reads: ["memory/ontology/graph.jsonl", "envs/<env>/env.toml"]
  writes: ["memory/ontology/graph.jsonl"]
  requires: ["service:ankiconnect"]
  graph_reads: ["Concept", "Card"]
  graph_writes: ["Card", "Concept"]
---

# tp:anki — Cards and the Review Loop

Real Anki desktop plus the AnkiConnect add-on (localhost:8765); Anki's scheduler is the single source of truth. Design record and setup: `harness/plugins/anki/anki-integration.md`. First use: if Anki or AnkiConnect is missing, point the learner at that file's setup section and stop.

**Terminal: plumbing.** curl to AnkiConnect never touches the learner's work. A card ask does not suspend the active env's pedagogy contract: make the card, return to the session.

## Gate first, always

POST JSON to `http://127.0.0.1:8765`: `{"action": <name>, "version": 6, "params": {...}}`. Ping `{"action":"version","version":6}` before anything else.

- **Interactive** (the learner asked): connection refused → halt, "Anki isn't running — open it, then say go." Retry on confirm. Never proceed blind.
- **Embedded** (`tp:session` calling on resume / wrap up / today's plan): Anki closed → skip silently, one-line note, never block the parent flow.

## Decks and tags

One deck per env, named after the env folder; `anki_deck` in `env.toml` overrides. Deck missing → `createDeck` silently. Every card gets exactly three tags: `env::<env>`, `session::YYYY-MM-DD` (today), `concept::<node-id>`. Tags are the whole linkage; cards made directly in the Anki UI have none and fall out of the loop. Text only, no media, so chat review can render them.

## Card ("card this")

**The learner authors the content.** They think through the phrasing and memory hooks; that is the point. Never draft card content unprompted; on "help me phrase this", offer variants and they pick.

1. Gate. Resolve env → deck and tag (active session env; ask if ambiguous).
2. Take the learner's wording. Type by shape: **cloze** (model `Cloze`, field `Text` with `{{c1::answer}}`, optional `Back Extra`) or **basic** (model `Basic`, `Front` / `Back`).
3. **Concept key:** find the matching `Concept` node (`ontology.py query --type Concept`); none → create one (`part_of` the env) first.
4. **Dedup:** `findNotes` with `"tag:concept::<node-id>"`. Hits → show them, ask add-anyway or skip.
5. `addNote` with deck, model, fields, the three tags, `options: {"allowDuplicate": false, "duplicateScope": "deck"}`.
6. Log a `Card` node (`ontology.py create --type Card`, `note_id` = returned id), `refs` → the Concept, `part_of` the env.
7. Confirm in one line: deck, type, tags. Back to the session.

## Review

Anki desktop is the primary review surface and costs zero tokens. Chat review is for leech drills and short bursts only.

**Leech check** (resume, today's plan, "check my leeches"): `findCards {"query": "deck:<Deck> tag:leech"}`, then `cardsInfo` for question text and concept tags. On resume: offer, never force: "N leeches on <concepts> — relearn first, or continue?" Relearn = follow the `session::` tag to that day's `progress.md` entry, re-teach under the `tp:learn` contract, then `removeTags` `leech` so the signal resets. On today's plan: one line across envs, awareness only.

**Count sync** (wrap up): `cardReviews {"deck": "<Deck>", "startID": <ms epoch of local midnight>}` (compute midnight with `date`, never hard-code). Hand `tp:session` two counts: cards reviewed, fails (`buttonPressed` = 1). Ignore `reviewDurationMs`: the harness never reports minutes.

**Batched chat review** ("anki review"): due cards `findCards {"query": "deck:<Deck> is:due"}`, cap 20 (more → point to Anki desktop). Present **5 per message**, question side only, HTML stripped; the learner answers all 5 in one reply. Cloze: compare to the deletion, suggest a grade, they confirm. Basic: show the back, they self-grade. Grades Again/Hard/Good/Easy → ease 1–4, pushed with `answerCards`. First use in a session, confirm the action exists (`apiReflect {"scopes":["actions"],"actions":["answerCards"]}`); missing → tell the learner to update AnkiConnect, never fake-grade. End with one line: reviewed, fails, leeches surfaced.

## Invariants

- Never mutate scheduling except through `answerCards` with the learner's confirmed grades.
- Three tags on every card, no exceptions. Cards are created only through this skill.
- Embedded flows never block the parent flow.
- Relearning happens under `tp:learn`; this skill only surfaces the signal.
