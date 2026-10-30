# Copyright 2026 thinkPad contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
"""thinkpad-status: today's block, every env's bookmark, and a summary of the graph."""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from datetime import date

from .. import config
from ..schedule import bookmark, today_block
from ..spec import load_env


def _graph_entities() -> list[dict]:
    path = config.ROOT / "memory" / "ontology" / "graph.jsonl"
    if not path.exists():
        return []
    spec = importlib.util.spec_from_file_location("ontology", config.HARNESS / "scripts" / "ontology.py")
    onto = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(onto)
    return list(onto.load_graph(path)[0].values())


def main() -> int:
    today = date.today()
    dirs = sorted(d for d in config.ENVS.glob("*") if (d / "env.toml").exists()) if config.ENVS.exists() else []
    specs = [load_env(d) for d in dirs]
    marks = {s.name: bookmark(config.ENVS / s.name) for s in specs}
    touched = {n: m.get("Last touched", "") for n, m in marks.items()}

    print(f"{today:%a %Y-%m-%d}")
    if not specs:
        print("No envs yet. Start claude and say: I want to learn <topic>")
        return 0
    block = today_block(specs, touched, today)
    print(f"Today: {block.name}" if block else "Today: rest day (no env owns it)")
    print("\nEnvs")
    for s in specs:
        m = marks[s.name]
        flag = "" if s.is_active(today) else f" [{s.status if s.status != 'active' else 'expired'}]"
        print(f"  {s.name} (tier {s.tier}){flag}  last: {m.get('Last touched', '-')}")
        print(f"    next: {m.get('Next move', '-')}")

    entities = _graph_entities()
    if entities:
        print("\nGraph:", ", ".join(f"{n} {t}" for t, n in sorted(Counter(e["type"] for e in entities).items())))
        for e in [e for e in entities if e["type"] == "Learning"][-3:]:
            print(f"  learned: {e['properties']['summary']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
