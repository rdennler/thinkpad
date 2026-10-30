# Schema Guide

The authoritative schema is `harness/memory/schema.toml`. This page is the human summary and the recipe for extending it.

## Types

| Type | Required | Optional | Typical relations |
|---|---|---|---|
| Env | name, path | tier | none |
| Concept | name, domain | definition, refs | `part_of` Env, `relates_to` Concept |
| Exercise | name, env | level, source, status | `practices` Concept, `part_of` Env |
| Session | date, env | unit, mode | `part_of` Env |
| Learning | summary, source | confidence | `about` Concept, `learned_in` Session, `supersedes` Learning |
| Mnemonic | name, expansion | domain | `reinforces` Concept |
| Resource | name, kind (book, article, url, pdf, video, recording, tool, course) | locator | `about` Concept, `authored_by` Person |
| Person | name | role | none |
| Project | name, status | path | `uses` Concept or Resource |
| Card | note_id, env | refs | `refs` Concept, `part_of` Env |

## Relations

`part_of`, `about`, `practices`, `learned_in`, `reinforces`, `relates_to`, `uses`, `authored_by`, `supersedes` (acyclic), `refs`. Each lists the endpoint types it allows.

## Schema keys

- Per type: `required`, `optional`, `forbidden_properties`, `<field>_enum`.
- Per relation: `from_types`, `to_types` (empty means any), `cardinality` (`one_to_one`, `one_to_many`, `many_to_one`), `acyclic`.
- A type with `required` or `optional` rejects any property not listed.

## Adding a type or relation (local overlay)

Edit `memory/ontology/schema.toml` (create it if missing). It merges over the base: tables merge, lists append.

```toml
[types.Question]
required = ["text", "env"]
optional = ["status"]
status_enum = ["open", "answered"]

[relations.asked_in]
from_types = ["Question"]
to_types = ["Session"]
```

Schema first, then data. Run `python3 harness/scripts/ontology.py validate` afterwards. If a skill will write the new type, declare it in that skill's `graph_writes`; `thinkpad-lint` checks declared types against the **base** schema, so a skill that depends on an overlay type should be a local skill, not a shipped one.

## Useful queries

```sh
python3 harness/scripts/ontology.py list --type Env
python3 harness/scripts/ontology.py related --id env:my-env --dir incoming --rel part_of
python3 harness/scripts/ontology.py query --type Card --where '{"env":"my-env"}'
```
