# Skill API

A skill is a folder `harness/skills/<name>/` with a `SKILL.md`. Its public API is the `metadata:` block in the frontmatter. `thinkpad-lint` enforces it, so skills stay uniform and discoverable.

```markdown
---
name: grill
description: What it does and when it triggers.
metadata:
  api: 1
  kind: engine
  mode: socratic
  terminal: forbidden
  triggers: ["quiz me", "test me"]
  reads: ["envs/<env>/session-state.md"]
  writes: ["envs/<env>/grill/history.md"]
  requires: []
---
```

## Fields

| Field | Values | Meaning |
|---|---|---|
| `name` | folder name | These docs call it `tp:<name>`. In this repo it loads as a project skill, `/<name>`; through the plugin it is `/tp:<name>`. Routing is by phrase, so the learner rarely types either |
| `description` | one or two sentences | Used by the runtime to decide when to load the skill |
| `api` | `1` | Manifest version |
| `kind` | `engine` · `infra` · `integration` · `reference` | `engine`: core behaviour. `infra`: tooling that is not a learning session. `integration`: needs an outside service. `reference`: read by other skills, never triggered |
| `mode` | `socratic` · `infra` | Whether the Socratic contract applies while it runs |
| `terminal` | `forbidden` · `plumbing` · `allowed` | See `harness/guardrails/terminal-rule.md` |
| `triggers` | list of phrases | What the learner says. Empty for `reference` skills |
| `reads` / `writes` | list of paths | The files it touches, `<env>` as the placeholder. Writes are the contract: nothing else is modified |
| `graph_reads` / `graph_writes` | ontology type names, or `"*"` | Which graph types it reads or creates. Checked against `harness/memory/schema.toml`. Omit if none |
| `requires` | `bin:<cmd>`, `mcp:<server>`, `service:<name>` | What must exist for it to work |

## Rules (checked by `thinkpad-lint`)

1. The frontmatter `name` equals the folder name.
2. `kind`, `mode` and `terminal` are present and in range.
3. Every `tp:<skill>` mentioned anywhere resolves to a real skill.
4. Every `references/<file>.md` named in `SKILL.md` exists.
5. Every type in `graph_reads` / `graph_writes` exists in the schema (or is `"*"`).
6. No personal paths or names (`/Users/...`, email addresses).

## Writing a good skill

- **One job.** If the description needs "and", split it.
- **Triggers are phrases a person says**, not file names.
- **File shapes live in `references/` of the skill that writes the file.** Other skills point at that path; they don't redefine it.
- **Keep SKILL.md short** and push detail into `references/`.
- **Declare writes honestly.** A skill that edits a file it didn't declare is a bug.
- **Learning skills never run the learner's work.** Use `terminal: forbidden` or `plumbing`.

## Adding one

1. Create `harness/skills/<name>/SKILL.md` with the manifest.
2. Add a route in `harness/system-prompt/SYSTEM.md` if it is user-triggered.
3. Run `thinkpad-lint` and `python3 -m unittest discover tests`.
