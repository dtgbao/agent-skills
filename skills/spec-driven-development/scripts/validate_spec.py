#!/usr/bin/env python3
"""Validate the structure of a spec artifact."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SUPPORTED = {"requirements.md", "bugfix.md", "design.md", "tasks.md"}
OPTIONAL_SECTIONS = {"design.md": {"Correctness Properties"}}
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})(.*)$")
H2_RE = re.compile(r"^## (.+?)\s*$")
REQUIREMENT_RE = re.compile(r"^### Requirement \d+:\s+\S.*$")
USER_STORY_RE = re.compile(r"^\*\*User Story:\*\*\s+\S.*$")
ACCEPTANCE_RE = re.compile(r"^#### Acceptance Criteria\s*$")
TABLE_HEADER_RE = re.compile(r"^\|\s*Task\s*\|\s*Depends On\s*\|\s*$")
TABLE_DIVIDER_RE = re.compile(r"^\|\s*:?-{3,}:?\s*\|\s*:?-{3,}:?\s*\|\s*$")
TASK_RE = re.compile(r"^- \[[ xX]\](?:\\?\*)?\s+(?P<number>\d+)\.\s+(?P<title>\S.*)$")
TASK_LABEL_RE = re.compile(
    r"^\s+-\s+\*\*(?P<label>RED|Verify RED|GREEN|Verify GREEN|REFACTOR|Reason|Approval|Check|Expected):\*\*\s+\S.*$"
)
TDD_CYCLE = ("RED", "Verify RED", "GREEN", "Verify GREEN", "REFACTOR")


@dataclass(frozen=True)
class Diagnostic:
    line: int
    code: str
    message: str


@dataclass(frozen=True)
class Fence:
    language: str
    content: str
    line: int


def visible_lines(lines: list[str]) -> list[str | None]:
    visible: list[str | None] = []
    marker: tuple[str, int] | None = None
    for line in lines:
        match = FENCE_RE.match(line)
        if marker is None:
            if match:
                marker = (match.group(1)[0], len(match.group(1)))
                visible.append(None)
            else:
                visible.append(line)
            continue

        visible.append(None)
        char, minimum = marker
        if re.fullmatch(rf"\s{{0,3}}{re.escape(char)}{{{minimum},}}\s*", line):
            marker = None
    return visible


def headings(lines: list[str | None]) -> dict[str, int]:
    result: dict[str, int] = {}
    for index, line in enumerate(lines):
        if line is not None and (match := H2_RE.fullmatch(line)):
            result.setdefault(match.group(1), index)
    return result


def section_bounds(lines: list[str | None], name: str) -> tuple[int, int] | None:
    start = headings(lines).get(name)
    if start is None:
        return None
    end = next(
        (index for index in range(start + 1, len(lines)) if lines[index] is not None and H2_RE.fullmatch(lines[index])),
        len(lines),
    )
    return start, end


def missing_section_code(kind: str, heading: str) -> str:
    if kind == "tasks" and heading == "Task Dependency Graph":
        return "tasks/missing-dependency-graph"
    slug = re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")
    return f"{kind}/missing-{slug}"


def required_section_diagnostics(name: str, visible: list[str | None]) -> list[Diagnostic]:
    template = Path(__file__).resolve().parents[1] / "assets" / "templates" / name
    required = headings(visible_lines(template.read_text(encoding="utf-8").splitlines()))
    present = headings(visible)
    optional = OPTIONAL_SECTIONS.get(name, set())
    kind = Path(name).stem
    return [
        Diagnostic(1, missing_section_code(kind, heading), f"Missing required section: ## {heading}")
        for heading in required
        if heading not in optional and heading not in present
    ]


def validate_requirements(visible: list[str | None]) -> list[Diagnostic]:
    bounds = section_bounds(visible, "Requirements")
    if bounds is None:
        return []
    start, end = bounds
    blocks = [
        index
        for index in range(start + 1, end)
        if visible[index] is not None and REQUIREMENT_RE.fullmatch(visible[index])
    ]
    if not blocks:
        return [
            Diagnostic(
                start + 1,
                "requirements/missing-requirement-block",
                "Requirements section is missing a numbered requirement block.",
            )
        ]

    diagnostics: list[Diagnostic] = []
    for position, block_start in enumerate(blocks):
        block_end = blocks[position + 1] if position + 1 < len(blocks) else end
        block = visible[block_start + 1 : block_end]
        if not any(line is not None and USER_STORY_RE.fullmatch(line) for line in block):
            diagnostics.append(
                Diagnostic(
                    block_start + 1,
                    "requirements/missing-user-story",
                    "Requirement block is missing **User Story:**",
                )
            )
        if not any(line is not None and ACCEPTANCE_RE.fullmatch(line) for line in block):
            diagnostics.append(
                Diagnostic(
                    block_start + 1,
                    "requirements/missing-acceptance-criteria",
                    "Requirement block is missing #### Acceptance Criteria",
                )
            )
    return diagnostics


def fenced_blocks(lines: list[str], start: int, end: int) -> list[Fence]:
    blocks: list[Fence] = []
    marker: tuple[str, int] | None = None
    language = ""
    content: list[str] = []
    opening_line = 0
    for index in range(start, end):
        line = lines[index]
        if marker is None:
            match = FENCE_RE.match(line)
            if match:
                marker = (match.group(1)[0], len(match.group(1)))
                language = match.group(2).strip().split(maxsplit=1)[0].lower() if match.group(2).strip() else ""
                opening_line = index + 1
                content = []
            continue

        char, minimum = marker
        if re.fullmatch(rf"\s{{0,3}}{re.escape(char)}{{{minimum},}}\s*", line):
            blocks.append(Fence(language, "\n".join(content), opening_line))
            marker = None
        else:
            content.append(line)
    return blocks


def valid_waves(value: object) -> bool:
    if not isinstance(value, dict) or not isinstance(value.get("waves"), list) or not value["waves"]:
        return False
    seen_tasks: set[int] = set()
    for wave in value["waves"]:
        if not isinstance(wave, dict) or type(wave.get("wave")) is not int or wave["wave"] <= 0:
            return False
        tasks = wave.get("tasks")
        if not isinstance(tasks, list) or not tasks:
            return False
        for task in tasks:
            if type(task) is not int or task <= 0 or task in seen_tasks:
                return False
            seen_tasks.add(task)
    return True


def has_dependency_table(visible: list[str | None], start: int, end: int) -> bool:
    for index in range(start, end - 2):
        if visible[index] is None or not TABLE_HEADER_RE.fullmatch(visible[index]):
            continue
        if visible[index + 1] is None or not TABLE_DIVIDER_RE.fullmatch(visible[index + 1]):
            continue
        for row in visible[index + 2 : end]:
            if row is None or not row.startswith("|"):
                break
            cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
            if len(cells) == 2 and all(cells):
                return True
    return False


def validate_tasks(lines: list[str], visible: list[str | None]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    graph = section_bounds(visible, "Task Dependency Graph")
    if graph is not None:
        start, end = graph
        blocks = fenced_blocks(lines, start + 1, end)
        json_blocks = [block for block in blocks if block.language == "json"]
        if not json_blocks:
            diagnostics.append(
                Diagnostic(
                    start + 1,
                    "tasks/missing-dag-json",
                    "Task Dependency Graph section is missing a JSON code block with wave definitions.",
                )
            )
        else:
            try:
                value = json.loads(json_blocks[0].content)
            except json.JSONDecodeError:
                diagnostics.append(
                    Diagnostic(json_blocks[0].line, "tasks/invalid-dag-json", "Task Dependency Graph JSON is invalid.")
                )
            else:
                if not valid_waves(value):
                    diagnostics.append(
                        Diagnostic(
                            json_blocks[0].line,
                            "tasks/invalid-dag-waves",
                            "Task Dependency Graph JSON must define nonempty waves with unique positive task identifiers.",
                        )
                    )
        if not any(block.language == "text" and block.content.strip() for block in blocks):
            diagnostics.append(
                Diagnostic(
                    start + 1,
                    "tasks/missing-dependency-tree",
                    "Task Dependency Graph section is missing a nonempty text dependency tree.",
                )
            )
        if not has_dependency_table(visible, start + 1, end):
            diagnostics.append(
                Diagnostic(
                    start + 1,
                    "tasks/missing-dependency-table",
                    "Task Dependency Graph section is missing a Task | Depends On table with a mapping row.",
                )
            )

    tasks = section_bounds(visible, "Tasks")
    if tasks is not None:
        start, end = tasks
        task_starts = [
            (index, match)
            for index in range(start + 1, end)
            if visible[index] is not None and (match := TASK_RE.fullmatch(visible[index]))
        ]
        if not task_starts:
            diagnostics.append(
                Diagnostic(start + 1, "tasks/missing-task-checkbox", "Tasks section is missing a numbered top-level task checkbox.")
            )
        for position, (task_start, match) in enumerate(task_starts):
            task_end = task_starts[position + 1][0] if position + 1 < len(task_starts) else end
            labels = [
                label_match.group("label")
                for line in visible[task_start + 1 : task_end]
                if line is not None and (label_match := TASK_LABEL_RE.fullmatch(line))
            ]
            title = match.group("title")
            if title.startswith("Checkpoint"):
                if not {"Check", "Expected"}.issubset(labels):
                    diagnostics.append(
                        Diagnostic(
                            task_start + 1,
                            "tasks/missing-checkpoint-verification",
                            "Checkpoint task must include nonempty Check and Expected entries.",
                        )
                    )
                continue
            if "[TDD Exception]" in title:
                if not {"Reason", "Approval", "Check"}.issubset(labels):
                    diagnostics.append(
                        Diagnostic(
                            task_start + 1,
                            "tasks/incomplete-tdd-exception",
                            "TDD exception task must include nonempty Reason, Approval, and Check entries.",
                        )
                    )
                continue

            cycle = tuple(label for label in labels if label in TDD_CYCLE)
            if cycle != TDD_CYCLE:
                diagnostics.append(
                    Diagnostic(
                        task_start + 1,
                        "tasks/incomplete-tdd-cycle",
                        "Behavior task must include RED, Verify RED, GREEN, Verify GREEN, and REFACTOR entries in that order.",
                    )
                )
    return diagnostics


def validate(path: Path) -> list[Diagnostic]:
    lines = path.read_text(encoding="utf-8").splitlines()
    visible = visible_lines(lines)
    diagnostics = required_section_diagnostics(path.name, visible)
    if path.name == "requirements.md":
        diagnostics.extend(validate_requirements(visible))
    elif path.name == "tasks.md":
        diagnostics.extend(validate_tasks(lines, visible))
    return diagnostics


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    path = parse_args(argv).document
    if path.name not in SUPPORTED:
        print(f"error: unsupported document: {path}", file=sys.stderr)
        return 2
    try:
        diagnostics = validate(path)
    except (OSError, UnicodeError):
        print(f"error: cannot read document: {path}", file=sys.stderr)
        return 2

    for diagnostic in diagnostics:
        print(f"{path}:{diagnostic.line}:1: error [{diagnostic.code}] {diagnostic.message}", file=sys.stderr)
    return 1 if diagnostics else 0


if __name__ == "__main__":
    raise SystemExit(main())
