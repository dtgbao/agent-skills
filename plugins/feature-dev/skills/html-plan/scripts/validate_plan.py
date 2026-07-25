#!/usr/bin/env python3
"""Validate the structural and portability contract of an html-plan artifact."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable


APPROACH_ATTRIBUTES = (
    "data-approach-card",
    "data-approach-tab",
    "data-blueprint",
    "data-approval-choice",
)
REQUIRED_IDS = {
    "plan-shell",
    "evidence",
    "approach-comparison",
    "blueprint-tabs",
    "recommendation",
    "approval",
    "decision-notes",
    "copy-approval",
}
REQUIRED_BLUEPRINT_SECTIONS = {
    "component-design",
    "implementation-map",
    "build-sequence",
    "risks",
}
PLACEHOLDER_PATTERNS = {
    "unfilled template token": re.compile(r"\{\{[A-Z][A-Z0-9_:-]*\}\}"),
    "unfilled plan content": re.compile(r"\bPLAN_TODO\b"),
    "unresolved decision marker": re.compile(r"\bPLAN_UNRESOLVED\b"),
}


class ContractParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: Counter[str] = Counter()
        self.approaches: dict[str, list[str]] = {
            attribute: [] for attribute in APPROACH_ATTRIBUTES
        }
        self.blueprint_sections: dict[str, Counter[str]] = {}
        self._article_stack: list[str | None] = []
        self.selected_tabs: list[str] = []
        self.visible_blueprints: list[str] = []
        self.pressed_choices: list[str] = []
        self.diagram_scripts: dict[str, str] = {}
        self.custom_diagrams: set[str] = set()
        self.external_scripts: list[str] = []
        self.external_styles: list[str] = []
        self.external_images: list[str] = []
        self.forbidden_embeds: Counter[str] = Counter()
        self.inline_style_count = 0
        self.inline_script_count = 0
        self._diagram_approach: str | None = None
        self._diagram_buffer: list[str] = []

    def handle_starttag(
        self, tag: str, attrs_list: list[tuple[str, str | None]]
    ) -> None:
        attrs = {key: value if value is not None else "" for key, value in attrs_list}

        if tag == "article":
            self._article_stack.append(attrs.get("data-blueprint"))

        if element_id := attrs.get("id"):
            self.ids[element_id] += 1

        for attribute in APPROACH_ATTRIBUTES:
            if approach := attrs.get(attribute):
                self.approaches[attribute].append(approach)

        if approach := attrs.get("data-blueprint"):
            self.blueprint_sections[approach] = Counter()
            if "hidden" not in attrs:
                self.visible_blueprints.append(approach)

        if section := attrs.get("data-section"):
            active_blueprint = next(
                (value for value in reversed(self._article_stack) if value), None
            )
            if active_blueprint:
                self.blueprint_sections.setdefault(active_blueprint, Counter())[section] += 1

        if attrs.get("data-approach-tab") and attrs.get("aria-selected") == "true":
            self.selected_tabs.append(attrs["data-approach-tab"])
        if (
            attrs.get("data-approval-choice")
            and attrs.get("aria-pressed") == "true"
        ):
            self.pressed_choices.append(attrs["data-approval-choice"])

        if tag == "script":
            if source := attrs.get("src"):
                self.external_scripts.append(source)
            else:
                self.inline_script_count += 1
            if approach := attrs.get("data-diagram-data"):
                self._diagram_approach = approach
                self._diagram_buffer = []

        if tag == "style":
            self.inline_style_count += 1

        if tag == "link" and "stylesheet" in attrs.get("rel", "").lower():
            self.external_styles.append(attrs.get("href", ""))

        if tag == "img":
            source = attrs.get("src", "")
            if source and not source.startswith("data:"):
                self.external_images.append(source)

        if tag in {"iframe", "object", "embed"}:
            self.forbidden_embeds[tag] += 1

        if tag == "svg" and (approach := attrs.get("data-custom-diagram")):
            self.custom_diagrams.add(approach)

    def handle_data(self, data: str) -> None:
        if self._diagram_approach is not None:
            self._diagram_buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._diagram_approach is not None:
            self.diagram_scripts[self._diagram_approach] = "".join(
                self._diagram_buffer
            )
            self._diagram_approach = None
            self._diagram_buffer = []
        if tag == "article" and self._article_stack:
            self._article_stack.pop()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate an interactive HTML architecture plan."
    )
    parser.add_argument("plan", type=Path, help="Path to the generated .html plan")
    return parser.parse_args()


def duplicates(values: Iterable[str]) -> set[str]:
    counts = Counter(values)
    return {value for value, count in counts.items() if count > 1}


def validate_diagram(approach: str, raw: str, errors: list[str]) -> None:
    try:
        diagram = json.loads(raw)
    except json.JSONDecodeError as error:
        errors.append(f"diagram {approach!r} contains invalid JSON: {error}")
        return

    lanes = diagram.get("lanes")
    nodes = diagram.get("nodes")
    edges = diagram.get("edges")
    if not isinstance(lanes, list) or len(lanes) < 2:
        errors.append(f"diagram {approach!r} needs at least two lanes")
    elif any(not isinstance(lane, str) or not lane.strip() for lane in lanes):
        errors.append(f"diagram {approach!r} lanes must be non-empty labels")
    if not isinstance(nodes, list) or len(nodes) < 3:
        errors.append(f"diagram {approach!r} needs at least three nodes")
        return
    if not isinstance(edges, list) or len(edges) < 2:
        errors.append(f"diagram {approach!r} needs at least two edges")
        return

    node_ids = [node.get("id") for node in nodes if isinstance(node, dict)]
    if len(node_ids) != len(nodes) or any(not value for value in node_ids):
        errors.append(f"diagram {approach!r} has a node without an id")
        return
    if repeated := duplicates(node_ids):
        errors.append(
            f"diagram {approach!r} repeats node ids: {', '.join(sorted(repeated))}"
        )

    known = set(node_ids)
    for node in nodes:
        if not all(node.get(field) for field in ("label", "detail", "source")):
            errors.append(
                f"diagram {approach!r} node {node.get('id')!r} needs label, detail, and source"
            )
        lane = node.get("lane")
        if (
            not isinstance(lane, int)
            or isinstance(lane, bool)
            or not isinstance(lanes, list)
            or lane < 0
            or lane >= len(lanes)
        ):
            errors.append(
                f"diagram {approach!r} node {node.get('id')!r} has an invalid lane"
            )
        order = node.get("order")
        if not isinstance(order, int) or isinstance(order, bool) or order < 0:
            errors.append(
                f"diagram {approach!r} node {node.get('id')!r} has an invalid order"
            )
    for edge in edges:
        if not isinstance(edge, dict) or edge.get("from") not in known:
            errors.append(f"diagram {approach!r} has an edge with an unknown source")
        if not isinstance(edge, dict) or edge.get("to") not in known:
            errors.append(f"diagram {approach!r} has an edge with an unknown target")


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    if path.suffix.lower() != ".html":
        return ["plan path must end in .html"]
    if not path.is_file():
        return [f"plan does not exist: {path}"]

    source = path.read_text(encoding="utf-8")
    parser = ContractParser()
    try:
        parser.feed(source)
    except Exception as error:  # HTMLParser can expose malformed author edits.
        return [f"HTML could not be parsed: {error}"]

    for label, pattern in PLACEHOLDER_PATTERNS.items():
        if pattern.search(source):
            errors.append(label)

    for element_id in sorted(REQUIRED_IDS):
        count = parser.ids[element_id]
        if count != 1:
            errors.append(f"id={element_id!r} must occur once; found {count}")

    if repeated_ids := {key for key, count in parser.ids.items() if count > 1}:
        errors.append(f"duplicate ids: {', '.join(sorted(repeated_ids))}")

    approach_sets: dict[str, set[str]] = {}
    for attribute, values in parser.approaches.items():
        approach_sets[attribute] = set(values)
        if len(values) != 3 or len(set(values)) != 3:
            errors.append(f"{attribute} must identify exactly three unique approaches")
    if len({frozenset(values) for values in approach_sets.values()}) != 1:
        errors.append(
            "approach cards, tabs, blueprints, and approval choices must use the same ids"
        )

    approaches = approach_sets["data-blueprint"]
    if len(parser.selected_tabs) != 1:
        errors.append("exactly one approach tab must start selected")
    if len(parser.visible_blueprints) != 1:
        errors.append("exactly one blueprint must start visible")
    if len(parser.pressed_choices) != 1:
        errors.append("exactly one approval choice must start pressed")
    if (
        len(parser.selected_tabs) == 1
        and len(parser.visible_blueprints) == 1
        and parser.selected_tabs[0] != parser.visible_blueprints[0]
    ):
        errors.append("the initially selected tab and visible blueprint must match")
    if (
        len(parser.selected_tabs) == 1
        and len(parser.pressed_choices) == 1
        and parser.selected_tabs[0] != parser.pressed_choices[0]
    ):
        errors.append("the initially selected tab and approval choice must match")

    for approach in sorted(approaches):
        present = set(parser.blueprint_sections.get(approach, Counter()))
        missing = REQUIRED_BLUEPRINT_SECTIONS - present
        if missing:
            errors.append(
                f"blueprint {approach!r} is missing sections: {', '.join(sorted(missing))}"
            )
        if (
            approach not in parser.diagram_scripts
            and approach not in parser.custom_diagrams
        ):
            errors.append(f"blueprint {approach!r} needs diagram data or custom SVG")

    for approach, raw in parser.diagram_scripts.items():
        if approach not in approaches:
            errors.append(f"diagram data references unknown approach {approach!r}")
        validate_diagram(approach, raw, errors)
    for approach in sorted(parser.custom_diagrams - approaches):
        errors.append(f"custom SVG references unknown approach {approach!r}")

    if parser.inline_style_count < 1:
        errors.append("plan needs inline CSS")
    if parser.inline_script_count < 1:
        errors.append("plan needs inline JavaScript")
    if parser.external_scripts:
        errors.append("external scripts are not self-contained")
    if parser.external_styles:
        errors.append("external stylesheets are not self-contained")
    if parser.external_images:
        errors.append("images must use embedded data URLs")
    if parser.forbidden_embeds:
        errors.append("iframe, object, and embed elements are not self-contained")
    if re.search(r"@import\b|url\(\s*['\"]?https?://", source, re.IGNORECASE):
        errors.append("CSS imports or remote URLs violate the self-contained boundary")

    return errors


def main() -> int:
    args = parse_args()
    path = args.plan.resolve()
    errors = validate(path)
    if errors:
        print(f"FAIL {path}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS {path}")
    print("- three comparable, tabbed blueprints")
    print("- blueprint visual and implementation contracts present")
    print("- approval handoff controls present")
    print("- self-contained resource boundary preserved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
