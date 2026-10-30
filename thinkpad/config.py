# Copyright 2026 thinkPad contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
"""Paths and vocabularies shared by the spec, lint and the CLI."""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(os.environ.get("THINKPAD_ROOT", Path(__file__).resolve().parent.parent))
HARNESS = ROOT / "harness"
SKILLS = HARNESS / "skills"
SCHEMA = HARNESS / "memory" / "schema.toml"
ENVS = ROOT / "envs"
EXAMPLES = ROOT / "examples" / "envs"

PLUGIN = "tp"
MARKETPLACE = "thinkpad"

# env.toml vocabularies
TIERS = (1, 2, 3, "sprint")
STATUSES = ("active", "paused", "archived")
MODES = ("socratic", "project", "passenger")
TERMINALS = ("forbidden", "plumbing", "allowed")
REGISTERS = ("plain", "fluent")
EXIT_TESTS = ("spoken", "written", "none")
DAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
SLOTS = ("am", "pm")

# skill manifest vocabularies
SKILL_KINDS = ("engine", "infra", "integration", "reference")
SKILL_MODES = ("socratic", "infra")
