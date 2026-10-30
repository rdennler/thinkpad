# Copyright 2026 thinkPad contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
"""Static checks for the harness. Returns problems as strings; empty means clean."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

from . import config
from .spec import load_env, load_skill

MAX_TUTOR_CHARS = 6000  # tutor.md loads every session
LEAKS = re.compile(r"/Users/|[\w.+-]+@[\w-]+\.[\w.]+")
SKILL_REF = re.compile(r"`tp:([a-z0-9-]+)`|\btp:([a-z0-9-]+)\b")
# Subject-specific terms that must not leak into shipped, subject-neutral skills.
SUBJECT_TERMS = re.compile(r"\bkatas?\b|JavaScript|\bPython\b|\bnpm\b|\bvenv\b|closures?\b|off-by-one|\bMDN\b")
# Skills that are legitimately about software or tooling.
SOFTWARE_SKILLS = {"reverse-engineer", "media"}
REF_FILE = re.compile(r"`(references/[A-Za-z0-9_./-]+\.md)`")


def lint_skills(skills_dir: Path = config.SKILLS, schema: Path = config.SCHEMA) -> list[str]:
    problems: list[str] = []
    names = {p.name for p in skills_dir.iterdir() if (p / "SKILL.md").exists()}
    types = set(tomllib.loads(schema.read_text()).get("types", {}))
    for name in sorted(names):
        d = skills_dir / name
        try:
            manifest = load_skill(d)
        except (ValueError, KeyError) as e:
            problems.append(f"{name}: {e}")
            continue
        for t in manifest.graph_reads + manifest.graph_writes:
            if t != "*" and t not in types:
                problems.append(f"{name}: graph type {t!r} is not in the schema")
        for md in d.rglob("*.md"):
            text = md.read_text()
            rel = md.relative_to(skills_dir)
            if LEAKS.search(text):
                problems.append(f"{rel}: personal path or name")
            if name not in SOFTWARE_SKILLS and (m := SUBJECT_TERMS.search(text)):
                problems.append(f"{rel}: subject-specific term {m.group(0)!r}; keep shipped skills subject-neutral")
            for a, b in SKILL_REF.findall(text):
                if (a or b) not in names:
                    problems.append(f"{rel}: unknown skill tp:{a or b}")
        for ref in REF_FILE.findall((d / "SKILL.md").read_text()):
            if not (d / ref).exists():
                problems.append(f"{name}: missing {ref}")
    return problems


def lint_docs(root: Path = config.ROOT, skills_dir: Path = config.SKILLS) -> list[str]:
    """`tp:<skill>` references outside the skills folder (system prompt, docs, examples) must resolve too."""
    names = {p.name for p in skills_dir.iterdir() if (p / "SKILL.md").exists()}
    problems: list[str] = []
    for md in sorted(root.rglob("*.md")):
        rel = md.relative_to(root)
        if rel.parts[0] in ("envs", "media", "memory", "tracker", "extras") or skills_dir in md.parents:
            continue
        if any(part.startswith(".") or part == "node_modules" for part in rel.parts):
            continue
        for a, b in SKILL_REF.findall(md.read_text()):
            if (a or b) not in names:
                problems.append(f"{rel}: unknown skill tp:{a or b}")
    return problems


def lint_envs(envs_dir: Path = config.ENVS) -> list[str]:
    problems: list[str] = []
    if not envs_dir.exists():
        return problems
    for d in sorted(p for p in envs_dir.iterdir() if p.is_dir()):
        try:
            load_env(d)
        except (ValueError, TypeError, FileNotFoundError) as e:
            problems.append(f"envs/{d.name}: {e}")
        tutor = d / "tutor.md"
        if tutor.exists():
            n = len(tutor.read_text().strip())
            if n == 0:
                problems.append(f"envs/{d.name}/tutor.md: empty (delete it or fill it in)")
            elif n > MAX_TUTOR_CHARS:
                problems.append(f"envs/{d.name}/tutor.md: {n} chars, over {MAX_TUTOR_CHARS}; it loads every session")
    return problems

