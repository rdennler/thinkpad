#!/usr/bin/env python3
"""Typed knowledge graph: create, query, relate, validate. Every write is checked first.

Adapted from the `ontology` skill v1.0.4 by oswalpalash (MIT-0, https://clawhub.ai). Changes:
the schema is TOML (stdlib, no PyYAML) with a read-only harness base plus a local overlay;
create/update/relate validate against the schema before appending; dates replace timestamps;
`migrate` imports the older one-node-per-line format; `schema-append` is gone (edit the
overlay file instead).

    python3 harness/scripts/ontology.py create --type Concept --id concept:photosynthesis \
        --props '{"name":"photosynthesis","domain":"biology"}'
    python3 harness/scripts/ontology.py relate --from concept:photosynthesis --rel part_of --to env:my-env
    python3 harness/scripts/ontology.py query --type Concept --where '{"domain":"biology"}'
    python3 harness/scripts/ontology.py related --id env:my-env --dir incoming
    python3 harness/scripts/ontology.py validate

The graph is an append-only log of operations: create, update, delete, relate, unrelate.
Paths resolve inside THINKPAD_ROOT (default: the repo root).
"""

from __future__ import annotations

import argparse
import json
import os
import tomllib
import uuid
from datetime import date
from pathlib import Path

ROOT = Path(os.environ.get("THINKPAD_ROOT", Path(__file__).resolve().parents[2])).resolve()
BASE_SCHEMA = Path(__file__).resolve().parents[1] / "memory" / "schema.toml"
DEFAULT_GRAPH = "memory/ontology/graph.jsonl"
DEFAULT_OVERLAY = "memory/ontology/schema.toml"


def safe_path(user_path: str, label: str) -> Path:
    """Resolve inside ROOT; refuse anything that escapes it."""
    p = Path(user_path).expanduser()
    p = (p if p.is_absolute() else ROOT / p).resolve()
    if not p.is_relative_to(ROOT):
        raise SystemExit(f"Invalid {label}: must stay within '{ROOT}'")
    return p


# --- schema -----------------------------------------------------------------


def merge_schema(base: dict, extra: dict) -> dict:
    for key, value in extra.items():
        if isinstance(base.get(key), dict) and isinstance(value, dict):
            merge_schema(base[key], value)
        elif isinstance(base.get(key), list) and isinstance(value, list):
            base[key] += [v for v in value if v not in base[key]]
        else:
            base[key] = value
    return base


def load_schema(overlay: Path | None = None, base: Path = BASE_SCHEMA) -> dict:
    schema = tomllib.loads(base.read_text())
    if overlay is not None and overlay.exists():
        merge_schema(schema, tomllib.loads(overlay.read_text()))
    return schema


# --- graph log --------------------------------------------------------------


def load_graph(path: Path) -> tuple[dict, list]:
    entities: dict = {}
    relations: list = []
    if not path.exists():
        return entities, relations
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        op = rec.get("op")
        if op == "create":
            entities[rec["entity"]["id"]] = rec["entity"]
        elif op == "update" and rec["id"] in entities:
            entities[rec["id"]]["properties"].update(rec.get("properties", {}))
            entities[rec["id"]]["updated"] = rec.get("date")
        elif op == "delete":
            entities.pop(rec["id"], None)
        elif op == "relate":
            relations.append({k: rec.get(k) for k in ("from", "rel", "to")} | {"properties": rec.get("properties", {})})
        elif op == "unrelate":
            relations = [r for r in relations if (r["from"], r["rel"], r["to"]) != (rec["from"], rec["rel"], rec["to"])]
    return entities, relations


def append_op(path: Path, rec: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(rec) + "\n")


# --- validation -------------------------------------------------------------


def entity_errors(eid: str, type_name: str, props: dict, schema: dict) -> list[str]:
    ts = schema.get("types", {}).get(type_name)
    if ts is None:
        return [f"{eid}: unknown type '{type_name}' (known: {sorted(schema.get('types', {}))})"]
    errs = [f"{eid}: missing required property '{p}'" for p in ts.get("required", []) if p not in props]
    errs += [f"{eid}: contains forbidden property '{p}'" for p in ts.get("forbidden_properties", []) if p in props]
    declared = set(ts.get("required", [])) | set(ts.get("optional", []))
    if declared:
        errs += [f"{eid}: undeclared property '{p}' for {type_name}" for p in props if p not in declared]
    for key, allowed in ts.items():
        if key.endswith("_enum"):
            field = key[: -len("_enum")]
            if props.get(field) and props[field] not in allowed:
                errs.append(f"{eid}: '{field}' must be one of {allowed}, got '{props[field]}'")
    return errs


def relation_errors(rel_type: str, entities: dict, relations: list, schema: dict) -> list[str]:
    rs = schema.get("relations", {}).get(rel_type)
    if rs is None:
        return [f"{rel_type}: unknown relation (known: {sorted(schema.get('relations', {}))})"]
    rels = [r for r in relations if r["rel"] == rel_type]
    errs: list[str] = []
    for r in rels:
        a, b = entities.get(r["from"]), entities.get(r["to"])
        if not a or not b:
            errs.append(f"{rel_type}: references missing entity ({r['from']} -> {r['to']})")
            continue
        if rs.get("from_types") and a["type"] not in rs["from_types"]:
            errs.append(f"{rel_type}: from {r['from']} is {a['type']}, expected one of {rs['from_types']}")
        if rs.get("to_types") and b["type"] not in rs["to_types"]:
            errs.append(f"{rel_type}: to {r['to']} is {b['type']}, expected one of {rs['to_types']}")
    card = rs.get("cardinality")
    if card in ("one_to_one", "many_to_one"):
        errs += _dupes(rel_type, rels, "from", card)
    if card in ("one_to_one", "one_to_many"):
        errs += _dupes(rel_type, rels, "to", card)
    if rs.get("acyclic") and _has_cycle(rels):
        errs.append(f"{rel_type}: cyclic dependency detected")
    return errs


def _dupes(rel_type: str, rels: list, end: str, card: str) -> list[str]:
    seen: dict = {}
    for r in rels:
        seen[r[end]] = seen.get(r[end], 0) + 1
    return [f"{rel_type}: {end} entity {k} violates cardinality {card}" for k, n in seen.items() if n > 1]


def _has_cycle(rels: list) -> bool:
    graph: dict = {}
    for r in rels:
        graph.setdefault(r["from"], []).append(r["to"])
    state: dict = {}  # 1 = on stack, 2 = done

    def visit(n) -> bool:
        state[n] = 1
        for m in graph.get(n, []):
            if state.get(m) == 1 or (m not in state and visit(m)):
                return True
        state[n] = 2
        return False

    return any(n not in state and visit(n) for n in list(graph))


def validate_graph(graph: Path, schema: dict) -> list[str]:
    entities, relations = load_graph(graph)
    errs = [e for i, ent in entities.items() for e in entity_errors(i, ent["type"], ent["properties"], schema)]
    for rel_type in {r["rel"] for r in relations} | set(schema.get("relations", {})):
        errs += relation_errors(rel_type, entities, relations, schema)
    return errs


def _fail(errs: list[str]) -> None:
    raise SystemExit("Refused, nothing written:\n  - " + "\n  - ".join(errs))


# --- operations -------------------------------------------------------------


def create_entity(type_name: str, props: dict, graph: Path, schema: dict, eid: str | None = None) -> dict:
    eid = eid or f"{type_name.lower()[:4]}_{uuid.uuid4().hex[:8]}"
    entities, _ = load_graph(graph)
    errs = [f"{eid}: already exists (use update)"] if eid in entities else []
    errs += entity_errors(eid, type_name, props, schema)
    if errs:
        _fail(errs)
    today = date.today().isoformat()
    entity = {"id": eid, "type": type_name, "properties": props, "created": today, "updated": today}
    append_op(graph, {"op": "create", "entity": entity, "date": today})
    return entity


def update_entity(eid: str, props: dict, graph: Path, schema: dict) -> dict | None:
    entities, _ = load_graph(graph)
    if eid not in entities:
        return None
    merged = entities[eid]["properties"] | props
    errs = entity_errors(eid, entities[eid]["type"], merged, schema)
    if errs:
        _fail(errs)
    today = date.today().isoformat()
    append_op(graph, {"op": "update", "id": eid, "properties": props, "date": today})
    return entities[eid] | {"properties": merged, "updated": today}


def delete_entity(eid: str, graph: Path) -> bool:
    entities, _ = load_graph(graph)
    if eid not in entities:
        return False
    append_op(graph, {"op": "delete", "id": eid, "date": date.today().isoformat()})
    return True


def create_relation(src: str, rel_type: str, dst: str, props: dict, graph: Path, schema: dict) -> dict:
    entities, relations = load_graph(graph)
    new = {"from": src, "rel": rel_type, "to": dst, "properties": props}
    errs = relation_errors(rel_type, entities, relations + [new], schema)
    if errs:
        _fail(errs)
    rec = {"op": "relate", **new, "date": date.today().isoformat()}
    append_op(graph, rec)
    return rec


def query_entities(type_name: str | None, where: dict, graph: Path) -> list:
    entities, _ = load_graph(graph)
    return [
        e for e in entities.values()
        if (not type_name or e["type"] == type_name) and all(e["properties"].get(k) == v for k, v in where.items())
    ]


def get_related(eid: str, rel_type: str | None, graph: Path, direction: str = "outgoing") -> list:
    entities, relations = load_graph(graph)
    out = []
    for r in relations:
        if rel_type and r["rel"] != rel_type:
            continue
        for d, here, there in (("outgoing", r["from"], r["to"]), ("incoming", r["to"], r["from"])):
            if here == eid and direction in (d, "both") and there in entities:
                out.append({"relation": r["rel"], "direction": d, "entity": entities[there]})
    return out


def migrate_legacy(src: Path, graph: Path) -> int:
    """Import the older format: one node per line {id,type,props,relations,created}, last line
    per id wins. Writes ops without validating; run `validate` afterwards."""
    nodes: dict = {}
    for line in src.read_text().splitlines():
        if line.strip():
            rec = json.loads(line)
            nodes[rec["id"]] = rec
    existing, _ = load_graph(graph)
    n = 0
    for rec in nodes.values():
        if rec["id"] in existing:
            continue
        day = rec.get("created") or date.today().isoformat()
        ent = {"id": rec["id"], "type": rec["type"], "properties": rec.get("props", {}), "created": day, "updated": day}
        append_op(graph, {"op": "create", "entity": ent, "date": day})
        n += 1
    for rec in nodes.values():
        for r in rec.get("relations", []):
            append_op(graph, {"op": "relate", "from": rec["id"], "rel": r["rel"], "to": r["to"], "properties": {}, "date": rec.get("created")})
    return n


# --- cli --------------------------------------------------------------------


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description="Ontology graph operations")
    sub = ap.add_subparsers(dest="command", required=True)

    def cmd(name: str, *flags: tuple):
        p = sub.add_parser(name)
        p.add_argument("--graph", "-g", default=DEFAULT_GRAPH)
        p.add_argument("--schema", "-s", default=DEFAULT_OVERLAY, help="local overlay merged over the harness schema")
        for args, kw in flags:
            p.add_argument(*args, **kw)

    cmd("create", (("--type", "-t"), {"required": True}), (("--props", "-p"), {"default": "{}"}), (("--id",), {}))
    cmd("get", (("--id",), {"required": True}))
    cmd("query", (("--type", "-t"), {}), (("--where", "-w"), {"default": "{}"}))
    cmd("list", (("--type", "-t"), {}))
    cmd("update", (("--id",), {"required": True}), (("--props", "-p"), {"required": True}))
    cmd("delete", (("--id",), {"required": True}))
    cmd("relate", (("--from",), {"dest": "src", "required": True}), (("--rel", "-r"), {"required": True}),
        (("--to",), {"dest": "dst", "required": True}), (("--props", "-p"), {"default": "{}"}))
    cmd("related", (("--id",), {"required": True}), (("--rel", "-r"), {}),
        (("--dir", "-d"), {"choices": ["outgoing", "incoming", "both"], "default": "outgoing"}))
    cmd("validate")
    cmd("migrate", (("--from",), {"dest": "src", "required": True, "help": "legacy graph.jsonl"}))
    a = ap.parse_args(argv)

    graph = safe_path(a.graph, "graph path")
    schema = load_schema(safe_path(a.schema, "schema path"))
    show = lambda obj: print(json.dumps(obj, indent=2))  # noqa: E731

    if a.command == "create":
        show(create_entity(a.type, json.loads(a.props), graph, schema, a.id))
    elif a.command == "get":
        show(load_graph(graph)[0].get(a.id) or f"Entity not found: {a.id}")
    elif a.command == "query":
        show(query_entities(a.type, json.loads(a.where), graph))
    elif a.command == "list":
        show(query_entities(a.type, {}, graph))
    elif a.command == "update":
        show(update_entity(a.id, json.loads(a.props), graph, schema) or f"Entity not found: {a.id}")
    elif a.command == "delete":
        print(f"Deleted: {a.id}" if delete_entity(a.id, graph) else f"Entity not found: {a.id}")
    elif a.command == "relate":
        show(create_relation(a.src, a.rel, a.dst, json.loads(a.props), graph, schema))
    elif a.command == "related":
        show(get_related(a.id, a.rel, graph, a.dir))
    elif a.command == "validate":
        errs = validate_graph(graph, schema)
        print("\n".join(["Validation errors:"] + [f"  - {e}" for e in errs]) if errs else "Graph is valid.")
        raise SystemExit(1 if errs else 0)
    elif a.command == "migrate":
        print(f"Imported {migrate_legacy(safe_path(a.src, 'legacy graph'), graph)} entities. Run validate next.")


if __name__ == "__main__":
    main()
