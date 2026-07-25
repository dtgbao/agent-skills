#!/usr/bin/env python3
"""Create a dated interactive architecture-plan artifact from the fixed shell."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path
from typing import NoReturn


SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create docs/plans/YYYY-MM-DD-<feature>.html from the html-plan shell."
    )
    parser.add_argument("feature_slug", help="Lowercase hyphenated feature name")
    parser.add_argument(
        "--date",
        default=dt.date.today().isoformat(),
        help="Plan date in YYYY-MM-DD form (default: today)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace the resolved output file if it already exists",
    )
    return parser.parse_args()


def fail(message: str) -> NoReturn:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def parse_date(value: str) -> str:
    try:
        return dt.date.fromisoformat(value).isoformat()
    except ValueError:
        fail(f"invalid date {value!r}; expected YYYY-MM-DD")


def find_git_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        fail("run this command from inside the target git repository")
    return Path(result.stdout.strip()).resolve()


def display_title(slug: str) -> str:
    return slug.replace("-", " ").capitalize()


def main() -> int:
    args = parse_args()
    if not SLUG_RE.fullmatch(args.feature_slug):
        fail("feature_slug must contain lowercase letters, digits, and single hyphens")

    plan_date = parse_date(args.date)
    skill_dir = Path(__file__).resolve().parent.parent
    template = skill_dir / "assets" / "architecture-plan.html"
    if not template.is_file():
        fail(f"missing template: {template}")

    root = find_git_root()
    output_dir = root / "docs" / "plans"
    output = output_dir / f"{plan_date}-{args.feature_slug}.html"
    if output.exists() and not args.force:
        fail(f"refusing to overwrite existing plan: {output}")

    source = template.read_text(encoding="utf-8")
    replacements = {
        "{{PLAN_DATE}}": plan_date,
        "{{PLAN_SLUG}}": args.feature_slug,
        "{{PLAN_TITLE}}": display_title(args.feature_slug),
    }
    for token, value in replacements.items():
        source = source.replace(token, value)

    output_dir.mkdir(parents=True, exist_ok=True)
    output.write_text(source, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
