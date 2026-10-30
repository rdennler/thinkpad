# Copyright 2026 thinkPad contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
"""thinkpad-check: preflight before a session. Checks the runtime, then the harness."""

from __future__ import annotations

import argparse
import sys

from ..substrate import SUBSTRATES
from . import lint as lint_cli


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--substrate", default="claude-code", choices=sorted(SUBSTRATES))
    args = ap.parse_args()
    try:
        SUBSTRATES[args.substrate]().preflight()
    except RuntimeError as e:
        print(f"FAIL {e}")
        return 1
    print(f"ok runtime: {args.substrate}")
    return lint_cli.main()


if __name__ == "__main__":
    sys.exit(main())
