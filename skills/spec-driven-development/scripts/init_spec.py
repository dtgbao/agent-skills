#!/usr/bin/env python3
"""Create a spec scaffold under docs/specs."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SLUG_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
ARTIFACTS = {
    "feature": ("requirements.md", "design.md", "tasks.md"),
    "bugfix": ("bugfix.md", "design.md", "tasks.md"),
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", help="lowercase hyphenated spec name")
    parser.add_argument("--title", help="human-readable title; defaults from slug")
    parser.add_argument("--kind", choices=ARTIFACTS, default="feature")
    parser.add_argument("--spec-root", type=Path, default=Path("docs/specs"))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not SLUG_PATTERN.fullmatch(args.slug):
        print("error: slug must contain only lowercase letters, digits, and single hyphens", file=sys.stderr)
        return 2

    title = args.title or args.slug.replace("-", " ").title()
    template_root = Path(__file__).resolve().parents[1] / "assets" / "templates"
    target = args.spec_root / args.slug
    if target.exists():
        print(f"error: target already exists: {target}", file=sys.stderr)
        return 1

    rendered: dict[str, str] = {}
    for name in ARTIFACTS[args.kind]:
        template = (template_root / name).read_text(encoding="utf-8")
        rendered[name] = template.replace("{{SPEC_TITLE}}", title).replace("{{SPEC_SLUG}}", args.slug)

    target.mkdir(parents=True)
    for name, content in rendered.items():
        path = target / name
        path.write_text(content, encoding="utf-8")
        print(f"Created {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
