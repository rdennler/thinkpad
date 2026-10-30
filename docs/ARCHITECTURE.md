# Architecture

Three things stay separate: the **pedagogy** (how the tutor teaches), the **runtime** (Claude Code), and the **env** (what the learner is studying). The pedagogy is a set of plain files under `harness/`. An env is one `env.toml`. Two feedback loops improve the harness over time.

## What is under `harness/`

Each is a folder. Edit any of them to change how the tutor behaves.

| Folder | Role | Reaches the model via |
|---|---|---|
| `system-prompt/` | Identity, routing, standing rules | root `CLAUDE.md` import |
| `guardrails/` | Socratic rules, terminal rule, web safety | root `CLAUDE.md` import; web safety is read by `tp:reverse-engineer` when a browser is involved |
| `memory/` | The typed graph's schema (`schema.toml`) | `tp:memory` |
| `tool-guidance/` | How to use tools (Chrome, ...) | skills reference it |
| `agents/` | Delegated roles (`retro-reflector`) | `.claude/agents` symlink, or plugin loader |
| `skills/` | Repeatable behaviours with a declared API; each owns the shapes of the files it writes in `references/` | `.claude/skills` symlink, or plugin loader |
| `scripts/` | Deterministic helpers: `ontology.py` (validated graph engine), `interaction-stats.py` | skills run them |
| `plugins/` | Optional integrations (Anki, Chrome) | docs plus skill `requires` |

## Envs are data

An env is a value, not a code path. Skills read `env.toml` instead of hard-coding env names, so adding a topic never touches the harness. The spec is parsed by `thinkpad/spec.py`; the daily schedule is derived from it in `thinkpad/schedule.py`.

## Two ways to load

Inside the repo, `.claude/skills` and `.claude/agents` are symlinks into `harness/`, so Claude Code loads them with no install. To use the tutor elsewhere, `thinkpad-install` registers the repo as a local plugin marketplace and installs `harness/` as the `tp` plugin. The files are the same either way.

## Two feedback loops

- **Session level:** `resume` → `meditate` → `wrap up`. What the learner just did changes the next session's opener (a retrieval question from the last miss).
- **Harness level:** `retro` → `memory/retros/improvement-queue.md` → `retro-reflector` drafts proposals → a human reviews them in git. **Agents never edit `harness/skills/` directly;** git is the gate.

## Teaching style is per-env data

`envs/<env>/tutor.md` is the learner's description of how they want to be taught. It is data, not harness: `tp:learn` reads it each session. Precedence is guardrails, then `env.toml`, then `tutor.md`, then the default voice, so a style preference can change tone, question style, analogies and visuals but never the Socratic rules. Details: `harness/skills/learn/references/tutor-voice.md`.

## Data vs harness

`harness/` is code and ships with the repo. `envs/`, `media/`, `tracker/`, `memory/` are the learner's data, ship empty, and are git-ignored by default.

## Lint before a session

`thinkpad-lint` validates every skill manifest, env spec and cross-reference, so a broken file is caught before it reaches the model.
