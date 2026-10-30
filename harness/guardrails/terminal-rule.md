# Terminal Rule

Whether the agent may run commands during a learning session is set per env by `terminal` in `env.toml`. Envs whose subject involves no software (a language, music, math on paper) should use `forbidden`.

| Value | Meaning |
|---|---|
| `forbidden` | The agent uses file tools only and never runs, builds or checks the learner's work. Harness bookkeeping is the one exception: `ontology.py` calls and `interactions.jsonl` appends never touch the learner's work. |
| `plumbing` | Commands are allowed for setup that is not the learning target: installing tools, downloading materials, converting files, session state, interaction-log appends, calls to optional integrations (AnkiConnect), and graph reads/writes through `harness/scripts/ontology.py` (it validates every write). **Never** run the learner's own work to check it or read its result back as the answer. |
| `allowed` | The learner is making a real artifact that needs running or building (an app, a script, a recording). Running it is legitimate. The Socratic "no direct answers" rule still holds. |

Grade answers by reading, never by executing, unless `terminal = "allowed"`.

**Infra skills** (`mode: infra` in their manifest) and platform maintenance may use the terminal freely. They are not learning sessions.

The manifest field `terminal` on each skill states which side it is on. `thinkpad-lint` checks that every skill declares one.
