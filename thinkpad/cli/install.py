# Copyright 2026 thinkPad contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
"""thinkpad-install: wire the harness into a runtime. `--dry-run` only prints the commands."""

from __future__ import annotations

import argparse
import subprocess
import sys

from .. import config
from ..substrate import SUBSTRATES


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--substrate", default="claude-code", choices=sorted(SUBSTRATES))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    sub = SUBSTRATES[args.substrate]()
    install = sub.materialise(config.ROOT)
    if not args.dry_run:
        try:
            sub.preflight()
        except RuntimeError as e:
            print(f"FAIL {e}")
            return 1
    for cmd in install.commands:
        print("$", " ".join(cmd))
        if not args.dry_run:
            subprocess.run(cmd, check=True)
    for note in install.notes:
        print(note)
    return 0


if __name__ == "__main__":
    sys.exit(main())
