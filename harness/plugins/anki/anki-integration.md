# Anki Integration — Design Record

Real Anki desktop + AnkiConnect instead of a custom flashcard app: AnkiConnect gives the same integration surface for free.

## Decisions

| Question | Decision |
|---|---|
| Build vs buy | Real Anki desktop + AnkiConnect add-on (2055492159). No custom app. |
| Primary review surface | **Anki desktop, on the learner's own time. Zero tokens.** Chat review is the exception, not the rule. |
| Review stats | Anki's revlog is the record. Pull today's card count and fails per deck at wrap-up. Durations are never pulled: the harness reports no minutes. |
| Link key | Ontology graph (`memory/ontology/graph.jsonl`). Tags on every card: `env::<env>`, `session::YYYY-MM-DD`, `concept::<node-id>`. Card also logged as a graph node. |
| Card creation | `tp:anki` skill only — the learner drives content (their phrasing, their hooks), Claude executes (creates note, assigns tags, logs to graph). Cards created directly in the Anki UI lose tags and fall out of the loop — don't. |
| Card types | Cloze (fill-in-the-blank) and Basic (flip). Text-only — no media, so chat flows can render them. |
| Deck layout | Flat, one deck per env. No subdecks — tags carry structure. |
| Relearn signal | Anki-native leech detection, threshold ~4, action **Tag Only** (not suspend). Pull-based: queried at schedule + resume; Anki never pushes. |
| Relearn action | Offered at env `resume` ("N leeches on X — relearn first, or continue?"), never forced. One-line awareness in the tp:session daily plan. Retros read leech history as input. |
| Chat review | `tp:anki` batch mode: 5 cards per message, ≤20 per invocation. For leech drills and short tracked bursts only. |
| Grading in chat | Cloze: Claude checks the answer, suggests a grade, the learner confirms. Basic: the learner self-grades ("2: good"). Pushed via `answerCards`. |
| Availability gate | Every AnkiConnect flow pings first (`version` action). Anki closed → halt, tell the learner, resume on their confirm. Wrap-up/schedule stat pulls skip silently instead. |
| Terminal rule | Both skills are `terminal: plumbing`: curl to AnkiConnect is integration plumbing. The active env's Socratic contract is untouched. |

## Architecture

```
learning session ──tp:anki──► AnkiConnect ──► Anki desktop (scheduler = source of truth)
     ▲                              │
     │  leeches / revlog (pull)     │ tags: env:: session:: concept::
     └──tp:anki◄─────────────┘
              │
              ├─ resume: leech check → offer relearn block
              ├─ wrap up: revlog sync → journal count/fails
              └─ schedule: one-line leech awareness per env
```

- **Anki's scheduler is the single source of truth.** Desktop and chat reviews coexist; both write to the same revlog.
- **Relearn loop:** leech tag → resume offers relearn → session tag on the card points back to that day's checkpoint notes/retro → re-teach socratically → card stays in Anki rotation.
- **Deck ↔ env mapping:** one deck per env, named after the env folder. Env tag = lowercase deck name.

## Token policy

Turns are the cost driver, not card text. Desktop review = 0 tokens. Chat review batches 5 cards/message (30 cards ≈ 7 turns, not 30) and caps at 20 cards. Stat pulls are single queries, a few hundred tokens.

## Setup (one-time, the learner)

1. Install Anki desktop.
2. Install AnkiConnect: Anki → Tools → Add-ons → Get Add-ons → code `2055492159` → restart Anki.
3. Deck options preset (apply to each env deck): Leeches → threshold **4**, action **Tag Only**.
4. Decks are created on demand by `tp:anki` (`createDeck`) — nothing to pre-create.

## Skill

`harness/skills/anki/SKILL.md`: card creation, tagging, graph logging, dedup; leech check, count sync, batched chat review.

Hooks live in `tp:session`: resume leech offer, wrap-up count sync, daily leech line.
