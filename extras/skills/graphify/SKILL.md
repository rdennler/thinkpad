---
name: graphify
description: Render the typed knowledge graph (memory/ontology/graph.jsonl) as Mermaid in markdown, or standalone HTML for big graphs. Triggers on "visualize my knowledge graph", "graph my learning".
metadata:
  api: 1
  kind: infra
  mode: infra
  terminal: allowed
  triggers: ["visualize my knowledge graph", "graph my learning"]
  reads: ["memory/ontology/graph.jsonl"]
  writes: ["media/out/"]
  requires: []
  graph_reads: ["*"]
  graph_writes: []
---

# tp:graphify — Knowledge Graph Visualization

Renders `memory/ontology/graph.jsonl` (typed nodes + relations; types defined in `harness/memory/schema.toml`) into a visual graph.

**Terminal exemption:** infra skill — MAY use terminal commands freely (jq for graph stats, opening HTML output). The learning-session file-tools-only rule does not apply.

## Inputs

1. Read `harness/memory/schema.toml` (and `memory/ontology/schema.toml` if present) for the types and relations.
2. Get current state from the engine, not the raw log: `python3 harness/scripts/ontology.py list` and `related` (see `references/rendering.md`).
3. `jq` is fine for counting: nodes per type, edge counts — decide output format from size *before* rendering.

## Output Formats

| Graph size (post-filter) | Format | Destination |
|---|---|---|
| ≤ ~50 nodes | Mermaid `graph LR` in a markdown file | `media/out/graph-YYYY-MM-DD.md` (or inline in chat if small) |
| > ~50 nodes | Standalone HTML (Mermaid via CDN, or simple vis) | `media/out/graph-YYYY-MM-DD.html`, then `open` it |

## Rendering Rules

- **Group by type**: one Mermaid `subgraph` per node type (Concept, Learning, Resource, ...).
- **Relations as labeled edges**: `A -->|relation| B`.
- **Short labels**: truncate node labels to ~30 chars with `…`; never dump long descriptions into a node.
- **Cap ~50 rendered nodes.** If the graph is bigger, either:
  - filter by type (ask, or use the type(s) the user mentioned — "graph my chemistry learning" → filter to that env's nodes), or
  - go HTML, still keeping labels short.
- **Filterable by type**: always tell the user which types were included/excluded and offer per-type re-renders. In HTML output, include simple per-type toggle checkboxes if feasible; otherwise one section per type.
- Mermaid IDs must be sanitized (alphanumeric + underscore); keep an id→label mapping, never put raw punctuation in IDs.
- Orphan nodes (no edges): render in a compact "unlinked" subgraph or omit with a count — say which you did.

## Optional — graphify.net

For full-repo structural analysis (beyond the ontology graph), graphify.net exists as an external option. **Reference only** — mention it when the user wants whole-repo visualization; do not upload anything without the user explicitly asking.

## Invariants

- Never modify the graph or either schema file — this skill is strictly read-and-render.
- Every render states: node count shown / total, types included, edges shown.
- Outputs land in `media/out/`, dated; don't overwrite a previous day's render.

References: `references/rendering.md` (Mermaid templates, HTML skeleton, filtering recipes).
