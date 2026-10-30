#!/usr/bin/env python3
"""Register failure rate for an env, from its interaction log.

    python3 harness/scripts/interaction-stats.py envs/<env>/interactions.jsonl [YYYY-MM-DD [YYYY-MM-DD]]

Prints counts per outcome and fail_reason, and (jargon + two-ideas) / total.
`productive-struggle` is not a tutor failure and is excluded from the rate numerator.
"""
import json
import sys
from collections import Counter


def main(path, start="0000-00-00", end="9999-99-99"):
    rows = [json.loads(line) for line in open(path) if line.strip()]
    rows = [r for r in rows if start <= r["date"] <= end]
    reasons = Counter(r["fail_reason"] for r in rows if r["outcome"] == 0)
    total = len(rows)
    print(f"total {total}: {total - sum(reasons.values())} landed, {dict(reasons)}")
    if total:
        rate = (reasons["jargon"] + reasons["two-ideas"]) / total
        print(f"register failure rate: {rate:.0%}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
