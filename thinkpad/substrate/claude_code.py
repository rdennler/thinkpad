# Copyright 2026 thinkPad contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
"""Claude Code substrate: the repo is a local plugin marketplace, `harness/` is the plugin.

`skills/` and `agents/` are discovered natively: inside the repo through the `.claude/skills` and
`.claude/agents` symlinks, elsewhere through the plugin loader. The other components reach the
model through the root CLAUDE.md, which imports them.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from .. import config
from .base import COMPONENTS, Install


class ClaudeCode:
    name = "claude-code"

    def surface(self, root: Path) -> dict[str, Path]:
        return {key: root / "harness" / folder for key, folder in COMPONENTS.items()}

    def materialise(self, root: Path) -> Install:
        return Install(
            commands=(
                ("claude", "plugin", "marketplace", "add", str(root)),
                ("claude", "plugin", "install", f"{config.PLUGIN}@{config.MARKETPLACE}"),
            ),
            notes=("Only needed to use the tutor outside this repo; inside it, skills load from .claude/skills.",),
        )

    def preflight(self) -> None:
        if shutil.which("claude") is None:
            raise RuntimeError(
                "`claude` not found on PATH. Install Claude Code: https://claude.com/claude-code"
            )
