# Getting started

## 1. Start

Install [Claude Code](https://claude.com/claude-code) if you haven't. Then:

```bash
git clone <this repo> thinkPad && cd thinkPad
claude
```

Say `I want to learn <topic>`. The tutor asks five short questions (what you want to be able to do, what you already know, how you like to be taught, which days you can show up, and whether you want questions, a project, or a coach beside you) and creates `envs/<topic>/`. It ends by telling you the phrase to start: `let's do <topic>`.

The skills load from `.claude/skills` the moment `claude` starts in this folder. There is no install step.

## 2. What it made

Everything about your topic is plain text in `envs/<topic>/`. Edit any of it.

- `env.toml`: tier, which days you show up, how strict the tutor is.
- `CLAUDE.md`: what you're learning, what you already know, what "done" means.
- `roadmap.md`: 5–10 units, each with a "done when" sentence.
- `tutor.md`: how you want to be taught: voice, how questions are asked, analogies to use or avoid, whether you want diagrams. Add to it any time by saying "remember I prefer …". It shapes *how* the tutor teaches, never *whether* it hands you the answer; that stays in `env.toml`.

Prefer to start from a template? Copy one from `examples/envs/` (`practice-drills`, `project`, `creative-draft`, `language-practice`, `math-science`, `_template`) into `envs/<name>/` and set `name` in its `env.toml`.

## 3. A session

| Say | Effect |
|---|---|
| `let's do <topic>` | Start or continue the env |
| `what should I do today` | Name today's block from your envs' cadences |
| `pause` / `checkpoint` | Save your spot |
| `status` | One-line readout |
| `wrap up` | Save, journal, tick the swim lane |
| `quiz me` / `test me` | A grill on what you have covered so far |
| `retro` | Debrief and queue improvements |

## 4. Env settings that matter

| Setting | Try this when |
|---|---|
| `terminal = "forbidden"` | You want zero chance of the agent running your code |
| `register = "plain"` | The topic is new to you; questions get simpler |
| `mode = "project"` | You are making a real artifact |
| `tier = "sprint"` + `expires` | A deadline is coming; it outranks everything until that date |

## 5. Optional extras

Each one is off until you want it, and the skill tells you what to set up the first time you ask.

- **Flashcards:** say `card this` during a session. Needs Anki desktop with the AnkiConnect add-on; see `harness/plugins/anki/`.
- **Reverse engineering a live site:** say `reverse engineer <url>`. Needs the Claude-in-Chrome extension; see [REVERSE-ENGINEERING.md](REVERSE-ENGINEERING.md).
- **Study material from PDFs or video:** say `extract this pdf`. Needs `pdftotext` and `ffmpeg`.
- **The tutor in other projects:** `python3 -m thinkpad.cli.install` registers the harness as a Claude Code plugin. Inside this repo it is not needed.

## Your data

`envs/`, `media/`, `tracker/` and `memory/` are git-ignored so personal progress never lands in a public fork by accident. Remove the lines at the bottom of `.gitignore` if you want to version them in a private repo.
