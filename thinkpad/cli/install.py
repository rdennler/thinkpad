# Copyright 2026 thinkPad contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
"""thinkpad-install: install `harness/` as the `tp` plugin so the tutor works outside this repo.
`--dry-run` only prints the commands."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys

from .. import config

# The repo is a local plugin marketplace and `harness/` is the plugin.
COMMANDS = (
    ("claude", "plugin", "marketplace", "add", str(config.ROOT)),
    ("claude", "plugin", "install", f"{config.PLUGIN}@{config.MARKETPLACE}"),
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not args.dry_run and shutil.which("claude") is None:
        print("FAIL `claude` not found on PATH. Install Claude Code: https://claude.com/claude-code")
        return 1
    for cmd in COMMANDS:
        print("$", " ".join(cmd))
        if not args.dry_run:
            subprocess.run(cmd, check=True)
    print("Only needed to use the tutor outside this repo; inside it, skills load from .claude/skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
