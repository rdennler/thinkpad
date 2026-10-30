# Copyright 2026 thinkPad contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
"""The two values the rest of the system reads: `EnvSpec` and `SkillManifest`.

An env is a plain value (one `env.toml`), not a code path. A skill's API is the `metadata:`
block of its SKILL.md frontmatter. Both validate at construction, so a bad file fails loudly.
"""

from __future__ import annotations

import json
import re
import tomllib
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from . import config


def _one_of(name: str, value, allowed) -> None:
    if value not in allowed:
        raise ValueError(f"{name} must be one of {allowed}, got {value!r}")


@dataclass(frozen=True)
class EnvSpec:
    """Static description of one learning env."""

    name: str
    title: str
    tier: int | str = 2
    status: str = "active"
    cadence: tuple[str, ...] = ()
    mode: str = "socratic"
    terminal: str = "plumbing"
    register: str = "plain"
    exit_test: str = "spoken"
    grill: bool = True
    anki_deck: str = ""
    expires: str = ""  # sprint envs only, YYYY-MM-DD

    def __post_init__(self) -> None:
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", self.name):
            raise ValueError(f"name must be lowercase kebab-case, got {self.name!r}")
        _one_of("tier", self.tier, config.TIERS)
        _one_of("status", self.status, config.STATUSES)
        _one_of("mode", self.mode, config.MODES)
        _one_of("terminal", self.terminal, config.TERMINALS)
        _one_of("register", self.register, config.REGISTERS)
        _one_of("exit_test", self.exit_test, config.EXIT_TESTS)
        for slot in self.cadence:
            day, _, part = slot.partition("-")
            _one_of("cadence day", day, config.DAYS)
            if part:
                _one_of("cadence slot", part, config.SLOTS)
        if self.tier == "sprint":
            if not self.expires:
                raise ValueError("a sprint env needs `expires` (YYYY-MM-DD)")
            date.fromisoformat(self.expires)
        if self.mode == "project" and self.terminal == "forbidden":
            raise ValueError("mode 'project' needs terminal 'plumbing' or 'allowed'")

    def is_active(self, today: date) -> bool:
        if self.status != "active":
            return False
        return not (self.expires and today > date.fromisoformat(self.expires))


def load_env(path: Path) -> EnvSpec:
    """Read `<path>/env.toml`; the folder name must equal `name`."""
    data = tomllib.loads((path / "env.toml").read_text())
    data["cadence"] = tuple(data.get("cadence", ()))
    spec = EnvSpec(**data)
    if spec.name != path.name:
        raise ValueError(f"{path}: name {spec.name!r} must equal the folder name {path.name!r}")
    return spec


@dataclass(frozen=True)
class SkillManifest:
    """The public API of one skill, read from SKILL.md frontmatter."""

    name: str
    description: str
    kind: str
    mode: str
    terminal: str
    triggers: tuple[str, ...] = ()
    reads: tuple[str, ...] = ()
    writes: tuple[str, ...] = ()
    requires: tuple[str, ...] = ()
    graph_reads: tuple[str, ...] = ()  # ontology types, or "*" for all
    graph_writes: tuple[str, ...] = ()
    api: int = 1
    extra: dict = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:
        if self.api != 1:
            raise ValueError(f"unsupported manifest api {self.api!r}")
        _one_of("kind", self.kind, config.SKILL_KINDS)
        _one_of("mode", self.mode, config.SKILL_MODES)
        _one_of("terminal", self.terminal, config.TERMINALS)
        if not self.description.strip():
            raise ValueError("description must not be empty")


def parse_frontmatter(text: str) -> dict:
    """Parse the small YAML subset skills use: `key: value`, and one nested level with
    inline JSON lists. Zero dependencies on purpose."""
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with '---' frontmatter")
    body = text[4 : text.index("\n---", 4)]
    out: dict = {}
    nested: dict | None = None
    for line in body.splitlines():
        if not line.strip():
            continue
        key, sep, value = line.strip().partition(":")
        if not sep:
            raise ValueError(f"bad frontmatter line: {line!r}")
        value = value.strip()
        if line.startswith("  "):
            if nested is None:
                raise ValueError(f"indented line outside a block: {line!r}")
            nested[key] = _scalar(value)
        elif value == "":
            nested = out.setdefault(key, {})
        else:
            nested = None
            out[key] = _scalar(value)
    return out


def _scalar(value: str):
    if value.startswith("[") or value.isdigit():
        return json.loads(value)
    return value


def load_skill(skill_dir: Path) -> SkillManifest:
    fm = parse_frontmatter((skill_dir / "SKILL.md").read_text())
    meta = dict(fm.get("metadata") or {})
    if fm.get("name") != skill_dir.name:
        raise ValueError(f"{skill_dir}: frontmatter name {fm.get('name')!r} != folder name")
    missing = [k for k in ("kind", "mode", "terminal") if k not in meta]
    if missing:
        raise ValueError(f"{skill_dir.name}: metadata is missing {missing}")
    known = {"api", "kind", "mode", "terminal", "triggers", "reads", "writes", "requires", "graph_reads", "graph_writes"}
    return SkillManifest(
        name=fm["name"],
        description=fm.get("description", ""),
        kind=meta["kind"],
        mode=meta["mode"],
        terminal=meta["terminal"],
        triggers=tuple(meta.get("triggers", ())),
        reads=tuple(meta.get("reads", ())),
        writes=tuple(meta.get("writes", ())),
        requires=tuple(meta.get("requires", ())),
        graph_reads=tuple(meta.get("graph_reads", ())),
        graph_writes=tuple(meta.get("graph_writes", ())),
        api=meta.get("api", 1),
        extra={k: v for k, v in meta.items() if k not in known},
    )
