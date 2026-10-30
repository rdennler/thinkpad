# Anki × thinkPad — How It Works (plain English)

Cheat sheet. Rationale + full decision table: `anki-integration.md`. Skill mechanics: `harness/skills/anki/`.

## The idea in one paragraph

You learn in sessions. When something is worth remembering, you say **"card this"** and dictate the card — Claude creates it in real Anki desktop (via the AnkiConnect add-on) with tags linking it to the env, today's session, and the concept in your knowledge graph. You review in the **Anki app on your own time** (costs zero tokens). Claude never gets notified — instead it *pulls*: at session resume it asks Anki "any leeches in this env?", and at wrap-up it pulls today's review count and fails into the journal. Cards you keep failing (4 lapses → Anki tags them `leech`) show up as an offer at your next resume: "relearn first, or continue?"

## What you say, what happens

| You say | What happens |
|---|---|
| "card this" / "make a card" (mid-session) | You dictate content (your phrasing — that's the point). Claude picks cloze or flip, tags it (`env::`, `session::`, `concept::`), dedups against existing cards for that concept, adds it, logs it to the ontology graph. One-line confirm, session continues. |
| "help me phrase this" | Claude offers wording variants, you pick. Only on request — default is you author. |
| *(nothing — just review in Anki app)* | Normal. Primary review surface. Anki's scheduler is the source of truth. |
| `resume` an env | Claude checks that env's deck for `leech`-tagged cards. Any found → "N leeches on X — relearn first, or continue?" Your call, never forced. Relearn = re-teach socratically using that card's session tag to find the original notes; leech tag cleared after. |
| `wrap up` | Today's Anki reviews for the env's deck (count, fails) folded into the journal automatically. |
| "what should I do today" | Daily plan includes one leech line across envs ("env-a: 2, env-b: 0"). Awareness only. |
| "anki review" / "flash review" | Chat-based review: 5 cards per message, you answer all 5 in one reply, capped at 20 cards. For leech drills / short bursts — bulk reviewing belongs in the app (token cost). |
| "check my leeches" | Leech readout on demand. |

## Rules that keep the loop alive

1. **Create cards only through "card this"** — cards typed directly into the Anki UI have no tags, so resume/wrap-up flows can't see them. (Old pre-thinkPad decks are like this — fine, they just live outside the loop.)
2. **Text only** — no images/audio, so cards render in chat.
3. **Anki must be running** for any of this. If it's closed: interactive asks halt and wait for you; resume/wrap-up/schedule just skip the Anki part silently.
4. Two card types: **fill-in-the-blank** (cloze) and **flip** (front/back).
5. Decks: one per env, named after the env folder. Created automatically on first card.

## One-time settings (do once per new env deck)

Anki → deck options: **Leeches → threshold 4, action "Tag Only"** (not suspend — suspended cards vanish from review; tag-only keeps them circulating while the env re-teaches).

Add-on: AnkiConnect, code `2055492159`.

## Troubleshooting

| Problem | Fix |
|---|---|
| "Anki isn't running" halts | Open Anki.app, say "go". |
| Ping fails with Anki open | AnkiConnect add-on missing/disabled → Tools → Add-ons. Test: `curl -s localhost:8765 -X POST -d '{"action":"version","version":6}'` → `{"result": 6, ...}` |
| `answerCards` unknown action | Update AnkiConnect (old version). |
| Leech never clears | It's removed after a relearn session; manually: Browse → select card → remove `leech` tag. |
| Card exists but resume never surfaces it | Probably untagged (made in Anki UI). Re-create via "card this", or add the three tags by hand in Browse. |
