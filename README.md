# thinkPad

> ***This repository has been archived. Please visit [yat (your-ai-tutor)](https://github.com/rdennler/yat) instead.***

**A harness that turns Claude into a Socratic tutor.**

A *harness* is the system around a model that lets it act as an agent: prompts, tools, memory, skills, orchestration. thinkPad is a harness built for one job. It makes the agent teach by asking questions, so the learner writes every line that matters and the agent never finishes the work for them.

You bring a topic. thinkPad gives you an env for it, a session loop that remembers where you stopped, a schedule that tells you what to do today, retros that improve the harness, and a ladder for learning how real websites work by reverse engineering them in your own Chrome.

## Start

You need [Claude Code](https://claude.com/claude-code). Nothing else.

```bash
git clone <this repo> thinkPad && cd thinkPad
claude
```

Then say what you want to learn:

> I want to learn <topic>

The tutor interviews you, makes an env for it, and tells you the one phrase to start. Next time, just open `claude` here and say `what should I do today`.

## What you get

| You say | What happens |
|---|---|
| "I want to learn <topic>" | `tp:new-env` interviews you and scaffolds `envs/<topic>/` |
| "let's do my-env" | `tp:learn` runs a Socratic session from the env's spec |
| "what should I do today" | `tp:session` reads every env's cadence and names today's block |
| "wrap up" | `tp:session` saves the bookmark, journals the session, ticks the swim lane |
| "quiz me" / "test me" | `tp:grill` asks only about what you have learned, never repeating a question |
| "retro" | `tp:retro` debriefs you and queues concrete improvements to the harness |
| "reverse engineer <url>" | `tp:reverse-engineer` walks a seven-rung ladder in your Chrome |
| "card this" | `tp:anki` makes a flashcard in Anki, if you have it |

`tp:` is how these docs name the skills. Inside this repo they load as project skills, so Claude Code lists them by folder name (`/learn`, `/session`, `/grill`). You only see `/tp:learn` after installing the plugin (see [For contributors](#for-contributors)). Either way you rarely type the name: routing is by phrase.

## How it is built

Everything that shapes the tutor lives under [`harness/`](harness/) as plain files: system prompt, guardrails, memory schema, tool guidance, subagents, skills, scripts, plugins. Your topic is data, one `env.toml` per env, and the pedagogy never has to change to add one. Skills load straight from the repo through `.claude/skills`, so there is nothing to install. Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), and [docs/CONCEPT.md](docs/CONCEPT.md) for why it exists.

Your data lives in `envs/`, `media/`, `tracker/` and `memory/`. They ship empty and are git-ignored by default.

## Docs

- [Getting started](docs/GETTING-STARTED.md): your first env and first session
- [Concept](docs/CONCEPT.md): what thinkPad is for
- [Architecture](docs/ARCHITECTURE.md): components, axes, the two recursion loops
- [Skill API](docs/SKILL-API.md): the manifest every skill declares
- [Reverse engineering a site](docs/REVERSE-ENGINEERING.md): the Chrome ladder
- [Contributing](CONTRIBUTING.md)

## For contributors

The Python package (3.11+, no dependencies) holds the checks and the optional plugin install. Run from the repo root, no `pip install` needed:

```bash
python3 -m thinkpad.cli.lint       # skill manifests, env specs, cross-references
python3 -m unittest discover tests
python3 -m thinkpad.cli.status     # today's block, each env's bookmark, a graph summary
python3 -m thinkpad.cli.install    # optional: install the `tp` plugin to use the tutor outside this repo
```

`pip install -e .` adds these as `thinkpad-lint`, `thinkpad-status`, `thinkpad-new` and `thinkpad-install`.

## License

Apache 2.0. See [LICENSE](LICENSE).
