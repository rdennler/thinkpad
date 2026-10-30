# Architecture

thinkPad follows the structure of [Harness²](https://github.com/google-research/harness2): a harness is a set of editable components, an env is a plain value, a substrate installs the harness into a runtime, and two recursion loops improve it.

## The eight components

Each is a folder under `harness/`. Edit any of them to change how the tutor behaves.

| Component | Folder | Role | Reaches the model via |
|---|---|---|---|
| System prompt | `system-prompt/` | Identity, routing, standing rules | root `CLAUDE.md` import |
| Guardrails | `guardrails/` | Socratic rules, terminal rule, web safety | root `CLAUDE.md` import; web safety is read by `tp:reverse-engineer` when a browser is involved |
| Memory | `memory/` | The typed graph's schema (`schema.toml`) | `tp:memory` |
| Tool guidance | `tool-guidance/` | How to use tools (Chrome, ...) | skills reference it |
| Subagents | `agents/` | Delegated roles (`retro-reflector`) | `.claude/agents` symlink, or plugin loader |
| Skills | `skills/` | Repeatable behaviours with a declared API; each owns the shapes of the files it writes in `references/` | `.claude/skills` symlink, or plugin loader |
| Scripts | `scripts/` | Deterministic helpers: `ontology.py` (validated graph engine), `interaction-stats.py` | skills run them |
| Plugins | `plugins/` | Optional integrations (Anki, Chrome) | docs plus skill `requires` |

By runtime role: **context construction** (system prompt, guardrails, memory, skills), **tool interface** (tool guidance, scripts), **orchestration** (subagents), **middleware** (plugins).

## Three axes, kept separate

| Axis | Harness² | thinkPad |
|---|---|---|
| Method | recursion, prompts, selection | pedagogy: `tp:learn`, hint ladder, retro |
| Substrate | OpenCode, Codex | Claude Code (`thinkpad/substrate/claude_code.py`) |
| Task spec | `BenchSpec` value + adapter | `EnvSpec`: one `env.toml` |

An env is a value, not a code path. Skills read `env.toml` instead of hard-coding env names, so adding a topic never touches the harness.

## Two ways to load

Inside the repo, `.claude/skills` and `.claude/agents` are symlinks into `harness/`, so Claude Code loads them with no install. To use the tutor elsewhere, the substrate installs the same folders as the `tp` plugin. The components are the same files either way.

## The substrate protocol

```python
class Substrate(Protocol):
    name: str
    def surface(self, root) -> dict[str, Path]: ...   # component -> folder
    def materialise(self, root) -> Install: ...        # pure: the commands that install it
    def preflight(self) -> None: ...                   # raises with the fix, runs before anything installs
```

Another runtime implements the same three methods.

## Two recursion loops

- **Task-level (session):** `resume` → `meditate` → `wrap up`. What the learner just did changes the next session's opener (a retrieval question from the last miss).
- **Harness-level:** `retro` → `memory/retros/improvement-queue.md` → `retro-reflector` drafts proposals → a human reviews them in git. **Agents never edit `harness/skills/` directly;** git is the gate.

## Teaching style is per-env data

`envs/<env>/tutor.md` is the learner's description of how they want to be taught. It sits in the context-construction layer but is data, not harness: `tp:learn` reads it each session. Precedence is guardrails, then `env.toml`, then `tutor.md`, then the default voice, so a style preference can change tone, question style, analogies and visuals but never the Socratic rules. Details: `harness/skills/learn/references/tutor-voice.md`.

## Data vs harness

`harness/` is code and ships with the repo. `envs/`, `media/`, `tracker/`, `memory/` are the learner's data, ship empty, and are git-ignored by default.

## Preflight before spending effort

`thinkpad-check` verifies the runtime and lints every skill manifest and env spec, the way `harness2-check` does before spending model budget.
