---
name: memory
description: Typed knowledge-graph memory. Triggers on "remember this", "what do I know about X", "link X to Y", "add to memory", "log this learning". All reads and writes go through harness/scripts/ontology.py, which validates every write against the schema.
metadata:
  api: 1
  kind: engine
  mode: infra
  terminal: plumbing
  triggers: ["remember this", "what do I know about X", "link X to Y", "add to memory", "log this learning"]
  reads: ["memory/ontology/graph.jsonl", "harness/memory/schema.toml", "memory/ontology/schema.toml"]
  writes: ["memory/ontology/graph.jsonl", "memory/ontology/schema.toml"]
  requires: ["bin:python3"]
  graph_reads: ["*"]
  graph_writes: ["*"]
---

# tp:memory — Typed Knowledge Graph

Durable, queryable memory for everything the learner has met. Concepts, learnings, mnemonics, resources, cards and envs are typed nodes linked by typed relations.

- **`memory/ontology/graph.jsonl`**: the graph. An append-only log of operations (`create`, `update`, `delete`, `relate`, `unrelate`). Created on first write. Never edit it by hand.
- **`harness/memory/schema.toml`**: the type system, shipped with the harness and read-only.
- **`memory/ontology/schema.toml`**: optional local overlay. Add types or relations here; it is merged over the base schema.

**Terminal:** running `harness/scripts/ontology.py` counts as session plumbing and is allowed inside learning sessions.

## The engine

Never write graph lines yourself. Call the script; it validates before it appends and refuses with the reason if the write is invalid.

```sh
python3 harness/scripts/ontology.py create --type Concept --id concept:photosynthesis \
    --props '{"name":"photosynthesis","domain":"biology"}'
python3 harness/scripts/ontology.py relate --from concept:photosynthesis --rel part_of --to env:my-env
python3 harness/scripts/ontology.py update --id concept:photosynthesis --props '{"definition":"how plants turn light, water and CO2 into sugar"}'
python3 harness/scripts/ontology.py query --type Concept --where '{"domain":"biology"}'
python3 harness/scripts/ontology.py related --id env:my-env --dir incoming
python3 harness/scripts/ontology.py validate
```

Refusals cover: unknown type, missing required property, undeclared property, bad enum value, unknown relation, a missing endpoint, wrong endpoint types, cardinality, and cycles on acyclic relations.

## Procedures

**"Remember this" / "log this learning"**

1. Pick the type from `references/schema-guide.md`. None fits means propose an overlay addition and ask the learner; don't force a type.
2. `query` for an existing id first. If it exists, `update` it instead of creating.
3. `create`, then `relate` to the Env (`part_of`) and any Concept it is `about`.
4. Confirm in one line: the id and the relations added.

**"What do I know about X"**

1. `query` by type and `--where`, or `list`; use `related --dir both` to walk one hop.
2. Answer in prose and cite ids so the learner can follow up ("link that to …").

**"Link X to Y"**: `relate`. If the relation isn't in the schema, say so and propose an overlay addition.

## Ids

`<type-lowercase>:<kebab-slug>`, stable and human-readable (`concept:big-o`, `env:my-env`). Renaming a concept changes `name`, never the id.

## Invariants

1. Every write goes through `ontology.py`. No hand-edited graph lines.
2. The base schema is never edited by an agent; extensions go in the overlay, with the learner's approval.
3. Secrets and credentials never enter the graph.
4. A graph from the older one-node-per-line format imports with `ontology.py migrate --from <file>`, then `validate`.
