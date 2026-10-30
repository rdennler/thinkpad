# Copyright 2026 thinkPad contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
"""The routing rule from `tp:session`, as code so it can be checked and shown."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from .config import DAYS
from .spec import EnvSpec

FIELD = re.compile(r"^\*\*(.+?):\*\*\s*(.*)$", re.M)


def bookmark(env_dir: Path) -> dict[str, str]:
    """The header fields of `session-state.md`, or {} if there is none."""
    f = env_dir / "session-state.md"
    return dict(FIELD.findall(f.read_text())) if f.exists() else {}


def today_block(specs: list[EnvSpec], last_touched: dict[str, str], today: date) -> EnvSpec | None:
    """An unexpired sprint outranks all; else lower tier wins; ties go to the older bookmark.
    `last_touched` maps env name -> YYYY-MM-DD (missing or "(never)" sorts oldest)."""
    day = DAYS[today.weekday()]
    due = [s for s in specs if s.is_active(today) and any(c.split("-")[0] == day for c in s.cadence)]
    rank = lambda s: (0 if s.tier == "sprint" else s.tier, last_touched.get(s.name, ""))  # noqa: E731
    return min(due, key=rank, default=None)
