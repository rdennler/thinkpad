# Copyright 2026 thinkPad contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
"""thinkpad-lint: validate skill manifests, env specs and the component layout."""

from __future__ import annotations

import sys

from .. import lint


def main() -> int:
    problems = lint.lint_components() + lint.lint_skills() + lint.lint_docs() + lint.lint_envs()
    for p in problems:
        print(f"FAIL {p}")
    print("ok" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
