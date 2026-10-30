# Copyright 2026 thinkPad contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
"""The Substrate interface: what an agent runtime owns, env-free.

A substrate knows how to install the harness's eight components into one runtime and how to
check that runtime is healthy. It knows nothing about any learning env.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, runtime_checkable

# The eight editable components, each a folder under harness/ (scripts and plugins included).
COMPONENTS = {
    "system_prompt": "system-prompt",
    "guardrails": "guardrails",
    "memory": "memory",
    "tool_guidance": "tool-guidance",
    "subagents": "agents",
    "skills": "skills",
    "scripts": "scripts",
    "plugins": "plugins",
}


@dataclass(frozen=True)
class Install:
    """A materialised harness: the commands that wire it into the runtime."""

    commands: tuple[tuple[str, ...], ...]
    notes: tuple[str, ...] = ()


@runtime_checkable
class Substrate(Protocol):
    name: str

    def surface(self, root: Path) -> dict[str, Path]:
        """Component name -> folder, for every component this runtime exposes."""

    def materialise(self, root: Path) -> Install:
        """The commands that install the harness at `root`. Pure: runs nothing."""

    def preflight(self) -> None:
        """Health checks before anything is installed. Raises RuntimeError with the fix."""
