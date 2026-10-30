# Hint Ladder

Climb one rung per stuck moment. Each rung gives less than the next and never gives the answer. Log each escalation as a teaching moment. The examples below come from different subjects on purpose; the moves are the same everywhere.

| Rung | Move | Example |
|---|---|---|
| 1 | **Restate the goal** as a question. | "What should be true of the sentence once the verb is right?" |
| 2 | **Narrow the search.** Point at where to look, not what's there. | "Look at the second step of your derivation." |
| 3 | **Predict.** Ask for the result on a tiny concrete case. | "Try your method on 2 + 2. What do you get?" |
| 4 | **Reference pointer.** A section of an authoritative source for *what it is*, plus a link that explains the *why*. | "Read the chapter section on tempo markings, then tell me which one fits bar 5." |
| 5 | **Contrast.** Show a *different* small example that exposes the same idea, then ask them to map it back. | A parallel case from another area of the subject. |
| 6 | **Name the concept.** Say what the idea is called and ask them to look for it. | "This is a sign error. Where could one hide?" |

Rules:

- Never skip to the answer. If rung 6 fails, stop and say so: "let's pause this and come back," then log `missing-prereq` and back up one concept.
- "I don't understand the question" is **not** an escalation. Rephrase the same question more simply at the same rung.
- Every link must be fetched and confirmed to resolve before you paste it. Never write a URL from memory.
- Link a Q&A thread only for the *theory*, never one whose top answer is the solution to the learner's exercise.

## Wording when `register = "plain"`

For envs where the material is genuinely new to the learner. The rungs do not relax; only the wording gets simpler.

1. **Plain words in the question.** No jargon about something the learner hasn't met. If a term is load-bearing, define it in one clause first, or ask about the thing without naming it.
2. **One idea per question.** Two clauses of new material become two questions. Ask the first.
3. **A small analogy on every new concept.** One or two lines, concrete. Draw from the Analogies section of `envs/<env>/tutor.md` first, then from "What the learner already knows" in `envs/<env>/CLAUDE.md`.
4. **Links are not the last rung.** Every hint about an unfamiliar mechanism carries a link: official docs for *what it does*, plus a Q&A thread for the *why*.
5. "Does that question make sense?" is legitimate. Rephrasing simpler at the same rung is not an escalation.

`tp:retro` reviews the register from the interaction log: failure rate = (jargon + two-ideas) / total. Step the register up as the learner levels.
