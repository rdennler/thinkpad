# Copyright 2026 thinkPad contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
"""thinkpad-new: copy an example env into envs/<name>/ and set its name."""

from __future__ import annotations

import argparse
import re
import shutil
import sys

from .. import config
from ..spec import load_env


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("name", help="lowercase kebab-case env name")
    ap.add_argument("--template", default="_template")
    args = ap.parse_args()
    src, dst = config.EXAMPLES / args.template, config.ENVS / args.name
    if not src.is_dir():
        print(f"FAIL no template {args.template!r}; have: {sorted(p.name for p in config.EXAMPLES.iterdir())}")
        return 1
    if dst.exists():
        print(f"FAIL {dst} already exists")
        return 1
    shutil.copytree(src, dst)
    toml = dst / "env.toml"
    toml.write_text(re.sub(r'^name = ".*"', f'name = "{args.name}"', toml.read_text(), count=1, flags=re.M))
    try:
        load_env(dst)
    except ValueError as e:
        shutil.rmtree(dst)
        print(f"FAIL {e}")
        return 1
    print(f"created envs/{args.name}. Edit env.toml, CLAUDE.md and roadmap.md, then say: let's do {args.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
