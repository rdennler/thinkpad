---
name: new-env
description: Scaffold a new learning env from a template. Triggers on "new env", "add a learning environment", "I want to learn <topic>", "set up an env for <topic>". Creates envs/<env>/ with env.toml, CLAUDE.md, roadmap.md and a first bookmark.
metadata:
  api: 1
  kind: engine
  mode: infra
  terminal: allowed
  triggers: ["new env", "add a learning environment", "I want to learn <topic>"]
  reads: ["examples/envs/", "harness/memory/schema.toml"]
  writes: ["envs/<env>/", "envs/<env>/tutor.md", "memory/ontology/graph.jsonl"]
  requires: []
  graph_reads: []
  graph_writes: ["Env"]
---

# tp:new-env — Scaffold an Env

An env is a folder under `envs/` with a spec, a content contract, a roadmap and a bookmark. Behaviour comes from the engine skills, so a new env needs no new skill.

## Procedure

1. **Interview (5 questions, one at a time):**
   - What do you want to learn, and what will you be able to *do* when you're done?
   - What do you already know that I can use for analogies?
   - How do you like to be taught? Visual or spoken, big picture first or small steps first, any analogies that work well or that you hate? (Skip anything they have no opinion on.)
   - How often can you show up (days of the week)?
   - Should I teach by questions (`socratic`), by making a real thing together (`project`), or sit beside you while you create (`passenger`)?
2. **Pick the closest template** in `examples/envs/` (`practice-drills`, `project`, `creative-draft`, `language-practice`, `math-science`, or `_template`). Copy it to `envs/<env>/`.
3. **Fill in `env.toml`** from the answers. Run `python3 -m thinkpad.cli.lint` and fix anything it reports.
4. **Write `CLAUDE.md`** from the template: the content contract, what the learner already knows, the exit-test wording. Keep it about the *material*; pedagogy lives in `tp:learn`.
5. **Write `tutor.md`** from the learner's answer to the teaching-style question, in their own words, using the template's sections. Leave sections empty rather than inventing preferences.
6. **Draft `roadmap.md`**: 5–10 units, each with a "done when" sentence. Keep it short. The learner edits it.
7. **Write the first bookmark** (`session-state.md`, shape in `harness/skills/session/references/session-state.md`) with a specific first move.
8. **Register in the graph:** `python3 harness/scripts/ontology.py create --type Env --id env:<env> --props '{"name":"<env>","path":"envs/<env>","tier":<tier from env.toml>}'`.
9. Tell the learner the one command to start: "say `let's do <env>`".

Never fill the roadmap with content the learner hasn't chosen. Never start teaching during scaffolding.
