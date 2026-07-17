#!/usr/bin/env python3
"""Validate the structure and cross-artifact integrity of a spec artifact."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


SUPPORTED = {"requirements.md", "bugfix.md", "design.md", "tasks.md"}
OPTIONAL_SECTIONS = {"design.md": {"Correctness Properties"}}
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})(.*)$")
H2_RE = re.compile(r"^## (.+?)\s*$")
H3_RE = re.compile(r"^### (.+?)\s*$")
REQUIREMENT_RE = re.compile(r"^### Requirement (?P<number>\d+):\s+\S.*$")
USER_STORY_RE = re.compile(r"^\*\*User Story:\*\*\s+\S.*$")
ACCEPTANCE_RE = re.compile(r"^#### Acceptance Criteria\s*$")
ACCEPTANCE_ITEM_RE = re.compile(r"^(?P<number>\d+)\.\s+\S.*$")
BUGFIX_ID_RE = re.compile(r"\*\*(?P<id>[CEU]B\d+)\*\*")
PARENT_TASK_RE = re.compile(
    r"^- \[(?P<checked>[ xX])\](?P<optional>\\?\*)?\s+(?P<id>\d+)\.\s+(?P<title>\S.*)$"
)
CHILD_TASK_RE = re.compile(
    r"^  - \[(?P<checked>[ xX])\](?P<optional>\\?\*)?\s+(?P<id>\d+\.\d+)\s+(?P<title>\S.*)$"
)
TASK_LABEL_RE = re.compile(
    r"^\s+-\s+\*\*(?P<label>RED|Verify RED|GREEN|Verify GREEN|REFACTOR|Reason|Approval|Check|Expected):\*\*\s+\S.*$"
)
TRACE_RE = re.compile(r"^\s+-\s+_(?P<kind>Requirements|Bugfix):\s+(?P<ids>[^_]+)_\s*$")
TASK_ID_RE = re.compile(r"\d+(?:\.\d+)?\Z")
NATIVE_LANGUAGES_EXCLUDED = {"", "text", "mermaid"}
TABLE_DIVIDER_CELL_RE = re.compile(r":?-{3,}:?")


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


@dataclass
class TaskNode:
    id: str
    title: str
    line: int
    checked: bool
    optional: bool
    parent_id: str | None
    labels: list[str] = field(default_factory=list)
    trace_kind: str | None = None
    trace_ids: tuple[str, ...] = ()
    kind: str = "unknown"
    children: list["TaskNode"] = field(default_factory=list)


@dataclass(frozen=True)
class GraphTask:
    id: str
    depends_on: tuple[str, ...]
    wave: int
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


def subsection_bounds(lines: list[str | None], start: int, end: int) -> list[tuple[int, int]]:
    starts = [
        index
        for index in range(start + 1, end)
        if lines[index] is not None and H3_RE.fullmatch(lines[index])
    ]
    return [
        (subsection_start, starts[position + 1] if position + 1 < len(starts) else end)
        for position, subsection_start in enumerate(starts)
    ]


def missing_section_code(kind: str, heading: str) -> str:
    if kind == "tasks" and heading == "Task Dependency Graph":
        return "tasks/missing-dependency-graph"
    slug = re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")
    return f"{kind}/missing-{slug}"


def design_template(path: Path) -> Path:
    templates = Path(__file__).resolve().parents[1] / "assets" / "templates"
    return templates / ("design-bugfix.md" if (path.parent / "bugfix.md").is_file() else "design.md")


def required_section_diagnostics(path: Path, visible: list[str | None]) -> list[Diagnostic]:
    template = design_template(path) if path.name == "design.md" else Path(__file__).resolve().parents[1] / "assets" / "templates" / path.name
    required = headings(visible_lines(template.read_text(encoding="utf-8").splitlines()))
    present = headings(visible)
    optional = OPTIONAL_SECTIONS.get(path.name, set())
    kind = path.stem
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
                Diagnostic(block_start + 1, "requirements/missing-user-story", "Requirement block is missing **User Story:**")
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


def section_fences(lines: list[str], visible: list[str | None], name: str) -> list[Fence]:
    bounds = section_bounds(visible, name)
    return fenced_blocks(lines, bounds[0] + 1, bounds[1]) if bounds else []


def section_has_not_applicable(visible: list[str | None], name: str) -> bool:
    bounds = section_bounds(visible, name)
    if bounds is None:
        return False
    start, end = bounds
    return any(
        line is not None
        and re.fullmatch(r"\*\*Not applicable:\*\*\s+(?!<)\S.*", line)
        for line in visible[start + 1 : end]
    )


def table_headers(visible: list[str | None], start: int, end: int) -> list[tuple[list[str], int]]:
    result: list[tuple[list[str], int]] = []
    for index in range(start, end - 1):
        line = visible[index]
        divider = visible[index + 1]
        if line is None or divider is None or not line.startswith("|") or not divider.startswith("|"):
            continue
        headers = [cell.strip() for cell in line.strip().strip("|").split("|")]
        divider_cells = [cell.strip() for cell in divider.strip().strip("|").split("|")]
        if len(headers) == len(divider_cells) and headers and all(TABLE_DIVIDER_CELL_RE.fullmatch(cell) for cell in divider_cells):
            result.append((headers, index + 1))
    return result


def section_has_table(visible: list[str | None], name: str, expected: tuple[str, ...]) -> bool:
    bounds = section_bounds(visible, name)
    if bounds is None:
        return False
    return any(tuple(headers) == expected for headers, _ in table_headers(visible, bounds[0] + 1, bounds[1]))


def has_nonempty_fence(fences: list[Fence], languages: set[str] | None = None) -> bool:
    return any(block.content.strip() and (languages is None or block.language in languages) for block in fences)


def has_native_contract(fences: list[Fence]) -> bool:
    return any(block.content.strip() and block.language not in NATIVE_LANGUAGES_EXCLUDED for block in fences)


def upstream_ids(path: Path) -> tuple[set[str], set[str], str | None]:
    requirements = path.parent / "requirements.md"
    if requirements.is_file():
        lines = visible_lines(requirements.read_text(encoding="utf-8").splitlines())
        valid: set[str] = set()
        required: set[str] = set()
        blocks: list[tuple[int, int, str]] = []
        requirement_starts = [
            (index, match.group("number"))
            for index, line in enumerate(lines)
            if line is not None and (match := REQUIREMENT_RE.fullmatch(line))
        ]
        for position, (start, number) in enumerate(requirement_starts):
            end = requirement_starts[position + 1][0] if position + 1 < len(requirement_starts) else len(lines)
            blocks.append((start, end, number))
        for start, end, number in blocks:
            valid.add(number)
            for line in lines[start + 1 : end]:
                if line is not None and (match := ACCEPTANCE_ITEM_RE.fullmatch(line)):
                    identifier = f"{number}.{match.group('number')}"
                    valid.add(identifier)
                    required.add(identifier)
        return valid, required, "Requirements"

    bugfix = path.parent / "bugfix.md"
    if bugfix.is_file():
        content = bugfix.read_text(encoding="utf-8")
        valid = {match.group("id") for match in BUGFIX_ID_RE.finditer(content)}
        required = {identifier for identifier in valid if identifier.startswith(("EB", "UB"))}
        return valid, required, "Bugfix"

    return set(), set(), None


def validate_design(path: Path, lines: list[str], visible: list[str | None]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    is_bugfix = (path.parent / "bugfix.md").is_file()

    architecture = section_bounds(visible, "Architecture")
    if architecture and not has_nonempty_fence(section_fences(lines, visible, "Architecture"), {"mermaid"}):
        diagnostics.append(Diagnostic(architecture[0] + 1, "design/missing-architecture-diagram", "Architecture must contain a nonempty Mermaid diagram."))

    if is_bugfix:
        hierarchy = section_bounds(visible, "Affected Hierarchy")
        if hierarchy and not has_nonempty_fence(section_fences(lines, visible, "Affected Hierarchy"), {"text"}):
            diagnostics.append(Diagnostic(hierarchy[0] + 1, "design/missing-affected-hierarchy", "Affected Hierarchy must contain a nonempty text tree."))
        root_cause = section_bounds(visible, "Root Cause and Fix")
        if root_cause and not has_nonempty_fence(section_fences(lines, visible, "Root Cause and Fix"), {"mermaid"}):
            diagnostics.append(Diagnostic(root_cause[0] + 1, "design/missing-root-cause-flow", "Root Cause and Fix must contain a nonempty Mermaid diagram."))
        changed = section_bounds(visible, "Changed Interfaces")
        if changed and not has_native_contract(section_fences(lines, visible, "Changed Interfaces")):
            diagnostics.append(Diagnostic(changed[0] + 1, "design/missing-native-contract", "Changed Interfaces must contain language-labeled native code or pseudocode."))
        models = section_bounds(visible, "Data Model Changes")
        if models and not has_native_contract(section_fences(lines, visible, "Data Model Changes")) and not section_has_not_applicable(visible, "Data Model Changes"):
            diagnostics.append(Diagnostic(models[0] + 1, "design/missing-data-model-contract", "Data Model Changes needs native code, pseudocode, or an evidence-based Not applicable reason."))
        required_tables = (
            ("Error Handling", ("Scenario", "System Response", "Caller or UI Recovery", "Validates"), "design/missing-error-table"),
            ("Regression Strategy", ("Boundary", "Test Evidence", "Validates"), "design/missing-regression-table"),
            ("Traceability", ("Source", "Design Elements", "Verification"), "design/missing-traceability-table"),
        )
    else:
        for section, code, message in (
            ("Repository Structure", "design/missing-repository-hierarchy", "Repository Structure must contain a nonempty text tree."),
            ("Component Hierarchy", "design/missing-component-hierarchy", "Component Hierarchy must contain a nonempty text tree."),
        ):
            bounds = section_bounds(visible, section)
            if bounds and not has_nonempty_fence(section_fences(lines, visible, section), {"text"}):
                diagnostics.append(Diagnostic(bounds[0] + 1, code, message))
        components = section_bounds(visible, "Components and Interfaces")
        if components and not has_native_contract(section_fences(lines, visible, "Components and Interfaces")):
            diagnostics.append(Diagnostic(components[0] + 1, "design/missing-native-contract", "Components and Interfaces must contain language-labeled native code or pseudocode."))
        models = section_bounds(visible, "Data Models")
        if models and not has_native_contract(section_fences(lines, visible, "Data Models")) and not section_has_not_applicable(visible, "Data Models"):
            diagnostics.append(Diagnostic(models[0] + 1, "design/missing-data-model-contract", "Data Models needs native code, pseudocode, or an evidence-based Not applicable reason."))
        operations = section_bounds(visible, "Operations")
        if operations and not section_has_table(visible, "Operations", ("Operation", "Input", "Output", "Errors", "Validates")) and not section_has_not_applicable(visible, "Operations"):
            diagnostics.append(Diagnostic(operations[0] + 1, "design/missing-operation-table", "Operations needs a typed inventory table or an evidence-based Not applicable reason."))
        flows = section_bounds(visible, "Flows and Strategies")
        if flows:
            subsections = subsection_bounds(visible, flows[0], flows[1])
            missing_flow = not subsections or any(
                not has_nonempty_fence(fenced_blocks(lines, start + 1, end), {"mermaid"})
                for start, end in subsections
            )
            if missing_flow:
                diagnostics.append(Diagnostic(flows[0] + 1, "design/missing-flow-diagram", "Every Flows and Strategies subsection must contain a nonempty Mermaid diagram."))
        required_tables = (
            ("Error Handling", ("Scenario", "System Response", "Caller or UI Recovery", "Validates"), "design/missing-error-table"),
            ("Testing Strategy", ("Behavior", "Level", "Evidence", "Validates"), "design/missing-testing-table"),
            ("Traceability", ("Source", "Design Elements", "Verification"), "design/missing-traceability-table"),
        )

    for section, expected, code in required_tables:
        bounds = section_bounds(visible, section)
        if bounds and not section_has_table(visible, section, expected):
            diagnostics.append(Diagnostic(bounds[0] + 1, code, f"{section} is missing its required table contract."))

    valid_ids, required_ids, _ = upstream_ids(path)
    traceability = section_bounds(visible, "Traceability")
    if traceability and valid_ids:
        start, end = traceability
        trace_text = "\n".join(line for line in visible[start + 1 : end] if line is not None)
        referenced = (
            set(re.findall(r"(?<![\d.])\d+\.\d+(?![\d.])", trace_text))
            if not is_bugfix
            else set(re.findall(r"\b[CEU]B\d+\b", trace_text))
        )
        unknown = referenced - valid_ids
        missing = required_ids - referenced
        if unknown:
            diagnostics.append(Diagnostic(start + 1, "design/invalid-traceability", f"Traceability references unknown identifiers: {', '.join(sorted(unknown))}."))
        if missing:
            diagnostics.append(Diagnostic(start + 1, "design/missing-upstream-coverage", f"Traceability is missing required identifiers: {', '.join(sorted(missing))}."))

    return diagnostics


def parse_trace(lines: list[str | None], start: int, end: int) -> tuple[str | None, tuple[str, ...], int | None]:
    for index in range(start, end):
        line = lines[index]
        if line is not None and (match := TRACE_RE.fullmatch(line)):
            identifiers = tuple(part.strip().strip("<>") for part in match.group("ids").split(",") if part.strip())
            return match.group("kind"), identifiers, index + 1
    return None, (), None


def task_labels(lines: list[str | None], start: int, end: int) -> list[str]:
    return [
        match.group("label")
        for line in lines[start:end]
        if line is not None and (match := TASK_LABEL_RE.fullmatch(line))
    ]


def classify_task(node: TaskNode) -> str:
    if node.title.startswith("Checkpoint"):
        return "checkpoint" if node.labels == ["Check", "Expected"] else "invalid-checkpoint"
    if "[TDD Exception]" in node.title:
        return "exception" if node.labels == ["Reason", "Approval", "Check"] else "invalid-exception"
    if node.labels == ["RED", "Verify RED"]:
        return "test"
    if node.labels == ["GREEN", "Verify GREEN", "REFACTOR"]:
        return "implementation"
    return "invalid"


def parse_tasks(visible: list[str | None], start: int, end: int) -> tuple[list[TaskNode], list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    parent_starts = [
        (index, match)
        for index in range(start + 1, end)
        if visible[index] is not None and (match := PARENT_TASK_RE.fullmatch(visible[index]))
    ]
    if not parent_starts:
        return [], [Diagnostic(start + 1, "tasks/missing-task-checkbox", "Tasks is missing a numbered top-level task checkbox.")]

    parents: list[TaskNode] = []
    expected_parent = 1
    for position, (parent_start, match) in enumerate(parent_starts):
        parent_end = parent_starts[position + 1][0] if position + 1 < len(parent_starts) else end
        parent_id = match.group("id")
        if int(parent_id) != expected_parent:
            diagnostics.append(Diagnostic(parent_start + 1, "tasks/invalid-parent-sequence", f"Expected parent task {expected_parent}, found {parent_id}."))
        expected_parent += 1
        parent = TaskNode(
            id=parent_id,
            title=match.group("title"),
            line=parent_start + 1,
            checked=match.group("checked").lower() == "x",
            optional=bool(match.group("optional")),
            parent_id=None,
        )
        child_starts = [
            (index, child_match)
            for index in range(parent_start + 1, parent_end)
            if visible[index] is not None and (child_match := CHILD_TASK_RE.fullmatch(visible[index]))
        ]

        if child_starts:
            parent.kind = "group"
            expected_child = 1
            for child_position, (child_start, child_match) in enumerate(child_starts):
                child_end = child_starts[child_position + 1][0] if child_position + 1 < len(child_starts) else parent_end
                child_id = child_match.group("id")
                expected_id = f"{parent_id}.{expected_child}"
                if child_id != expected_id:
                    diagnostics.append(Diagnostic(child_start + 1, "tasks/invalid-subtask-sequence", f"Expected subtask {expected_id}, found {child_id}."))
                expected_child += 1
                labels = task_labels(visible, child_start + 1, child_end)
                trace_kind, trace_ids, _ = parse_trace(visible, child_start + 1, child_end)
                child = TaskNode(
                    id=child_id,
                    title=child_match.group("title"),
                    line=child_start + 1,
                    checked=child_match.group("checked").lower() == "x",
                    optional=bool(child_match.group("optional")),
                    parent_id=parent_id,
                    labels=labels,
                    trace_kind=trace_kind,
                    trace_ids=trace_ids,
                )
                child.kind = classify_task(child)
                allowed_lines = 0
                for line in visible[child_start + 1 : child_end]:
                    if line is None or not re.match(r"^\s+-\s+", line):
                        continue
                    if TASK_LABEL_RE.fullmatch(line) or TRACE_RE.fullmatch(line):
                        continue
                    allowed_lines += 1
                if allowed_lines:
                    diagnostics.append(Diagnostic(child.line, "tasks/unexpected-subtask-entry", "Executable subtasks may contain only their accepted labeled entries and traceability line."))
                if child.kind == "invalid-checkpoint":
                    diagnostics.append(Diagnostic(child.line, "tasks/missing-checkpoint-verification", "Checkpoint must include Check and Expected entries in order."))
                elif child.kind == "invalid-exception":
                    diagnostics.append(Diagnostic(child.line, "tasks/incomplete-tdd-exception", "TDD exception must include Reason, Approval, and Check entries in order."))
                elif child.kind == "invalid":
                    diagnostics.append(Diagnostic(child.line, "tasks/invalid-subtask-form", "Subtask must be a RED test, GREEN implementation, checkpoint, or approved TDD exception form."))
                if child.trace_kind is None:
                    diagnostics.append(Diagnostic(child.line, "tasks/missing-traceability", "Executable subtask is missing a Requirements or Bugfix traceability line."))
                parent.children.append(child)

            for index, child in enumerate(parent.children):
                if child.kind == "test":
                    if index + 1 >= len(parent.children) or parent.children[index + 1].kind != "implementation":
                        diagnostics.append(Diagnostic(child.line, "tasks/orphan-test", "RED subtask must be followed by one implementation subtask."))
                    else:
                        implementation = parent.children[index + 1]
                        if child.trace_kind != implementation.trace_kind or child.trace_ids != implementation.trace_ids:
                            diagnostics.append(Diagnostic(implementation.line, "tasks/pair-traceability-mismatch", "Paired RED and GREEN subtasks must use identical traceability."))
                        if child.optional != implementation.optional:
                            diagnostics.append(Diagnostic(implementation.line, "tasks/pair-optionality-mismatch", "Paired RED and GREEN subtasks must both be required or both optional."))
                elif child.kind == "implementation" and (index == 0 or parent.children[index - 1].kind != "test"):
                    diagnostics.append(Diagnostic(child.line, "tasks/orphan-implementation", "Implementation subtask must immediately follow one RED subtask."))

            required_children = [child for child in parent.children if not child.optional]
            if parent.checked and any(not child.checked for child in required_children):
                diagnostics.append(Diagnostic(parent.line, "tasks/inconsistent-parent-state", "Checked parent has an incomplete required child."))
            if required_children and not parent.checked and all(child.checked for child in required_children):
                diagnostics.append(Diagnostic(parent.line, "tasks/inconsistent-parent-state", "Parent must be checked when every required child is complete."))
        else:
            parent.labels = task_labels(visible, parent_start + 1, parent_end)
            parent.trace_kind, parent.trace_ids, _ = parse_trace(visible, parent_start + 1, parent_end)
            parent.kind = classify_task(parent)
            if parent.kind in {"test", "implementation"} or any(
                label in {"RED", "Verify RED", "GREEN", "Verify GREEN", "REFACTOR"}
                for label in parent.labels
            ):
                diagnostics.append(Diagnostic(parent.line, "tasks/legacy-flat-task", "Behavior work must use hierarchical paired subtasks; flat TDD tasks are not supported."))
            elif parent.kind == "invalid-checkpoint":
                diagnostics.append(Diagnostic(parent.line, "tasks/missing-checkpoint-verification", "Checkpoint must include Check and Expected entries in order."))
            elif parent.kind == "invalid-exception":
                diagnostics.append(Diagnostic(parent.line, "tasks/incomplete-tdd-exception", "TDD exception must include Reason, Approval, and Check entries in order."))
            elif parent.kind == "invalid":
                diagnostics.append(Diagnostic(parent.line, "tasks/empty-parent", "Capability parent must contain executable subtasks or use a checkpoint/exception form."))
            if parent.kind in {"checkpoint", "exception"} and parent.trace_kind is None:
                diagnostics.append(Diagnostic(parent.line, "tasks/missing-traceability", "Executable task is missing a Requirements or Bugfix traceability line."))
        parents.append(parent)
    return parents, diagnostics


def executable_tasks(parents: list[TaskNode]) -> list[TaskNode]:
    result: list[TaskNode] = []
    for parent in parents:
        if parent.kind == "group":
            result.extend(parent.children)
        elif parent.kind in {"checkpoint", "exception"}:
            result.append(parent)
    return result


def parse_graph(lines: list[str], visible: list[str | None]) -> tuple[dict[str, GraphTask], list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    bounds = section_bounds(visible, "Task Dependency Graph")
    if bounds is None:
        return {}, diagnostics
    start, end = bounds
    blocks = [block for block in fenced_blocks(lines, start + 1, end) if block.language == "json"]
    if not blocks:
        return {}, [Diagnostic(start + 1, "tasks/missing-dag-json", "Task Dependency Graph is missing its JSON execution graph.")]
    block = blocks[0]
    try:
        value = json.loads(block.content)
    except json.JSONDecodeError:
        return {}, [Diagnostic(block.line, "tasks/invalid-dag-json", "Task Dependency Graph JSON is invalid.")]
    if not isinstance(value, dict) or not isinstance(value.get("waves"), list) or not value["waves"]:
        return {}, [Diagnostic(block.line, "tasks/invalid-dag-waves", "Task Dependency Graph must define nonempty waves.")]

    graph: dict[str, GraphTask] = {}
    wave_numbers: list[int] = []
    for wave_value in value["waves"]:
        if not isinstance(wave_value, dict) or type(wave_value.get("wave")) is not int or wave_value["wave"] <= 0:
            diagnostics.append(Diagnostic(block.line, "tasks/invalid-dag-waves", "Each wave needs a positive integer wave number."))
            continue
        wave = wave_value["wave"]
        wave_numbers.append(wave)
        task_values = wave_value.get("tasks")
        if not isinstance(task_values, list) or not task_values:
            diagnostics.append(Diagnostic(block.line, "tasks/invalid-dag-waves", "Each wave needs a nonempty tasks array."))
            continue
        for task_value in task_values:
            if not isinstance(task_value, dict):
                diagnostics.append(Diagnostic(block.line, "tasks/invalid-dag-task", "Graph tasks must be objects with id and dependsOn fields."))
                continue
            task_id = task_value.get("id")
            depends_on = task_value.get("dependsOn")
            if not isinstance(task_id, str) or not TASK_ID_RE.fullmatch(task_id) or not isinstance(depends_on, list) or not all(isinstance(item, str) and TASK_ID_RE.fullmatch(item) for item in depends_on):
                diagnostics.append(Diagnostic(block.line, "tasks/invalid-dag-task", "Graph task id must be a string identifier and dependsOn must contain string identifiers."))
                continue
            if task_id in graph:
                diagnostics.append(Diagnostic(block.line, "tasks/duplicate-dag-task", f"Graph task {task_id} appears more than once."))
                continue
            graph[task_id] = GraphTask(task_id, tuple(depends_on), wave, block.line)

    if wave_numbers != list(range(1, len(wave_numbers) + 1)):
        diagnostics.append(Diagnostic(block.line, "tasks/invalid-dag-waves", "Wave numbers must be unique and sequential starting at 1."))

    for task in graph.values():
        for dependency in task.depends_on:
            if dependency not in graph:
                diagnostics.append(Diagnostic(block.line, "tasks/unknown-dependency", f"Task {task.id} depends on unknown task {dependency}."))
            elif graph[dependency].wave >= task.wave:
                diagnostics.append(Diagnostic(block.line, "tasks/dependency-not-earlier", f"Task {task.id} dependency {dependency} must appear in an earlier wave."))

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(task_id: str) -> bool:
        if task_id in visiting:
            return True
        if task_id in visited or task_id not in graph:
            return False
        visiting.add(task_id)
        cycle = any(visit(dependency) for dependency in graph[task_id].depends_on)
        visiting.remove(task_id)
        visited.add(task_id)
        return cycle

    if any(visit(task_id) for task_id in graph):
        diagnostics.append(Diagnostic(block.line, "tasks/dependency-cycle", "Task dependency graph contains a cycle."))
    return graph, diagnostics


def validate_task_traceability(path: Path, tasks: list[TaskNode]) -> list[Diagnostic]:
    valid_ids, required_ids, expected_kind = upstream_ids(path)
    if not valid_ids or expected_kind is None:
        return []
    diagnostics: list[Diagnostic] = []
    covered: set[str] = set()
    for task in tasks:
        if task.trace_kind is None or any("<" in identifier for identifier in task.trace_ids):
            continue
        referenced = set(task.trace_ids)
        if task.trace_kind != expected_kind or referenced - valid_ids:
            diagnostics.append(
                Diagnostic(
                    task.line,
                    "tasks/invalid-traceability",
                    f"Task {task.id} traceability must use existing {expected_kind} identifiers.",
                )
            )
        if not task.optional and task.kind in {"implementation", "checkpoint", "exception"}:
            covered.update(referenced & valid_ids)
    missing = required_ids - covered
    if missing:
        diagnostics.append(Diagnostic(1, "tasks/missing-upstream-coverage", f"Required tasks do not cover: {', '.join(sorted(missing))}."))
    return diagnostics


def validate_tasks(path: Path, lines: list[str], visible: list[str | None]) -> list[Diagnostic]:
    bounds = section_bounds(visible, "Tasks")
    if bounds is None:
        return []
    parents, diagnostics = parse_tasks(visible, bounds[0], bounds[1])
    executable = executable_tasks(parents)
    graph, graph_diagnostics = parse_graph(lines, visible)
    diagnostics.extend(graph_diagnostics)

    executable_ids = {task.id for task in executable}
    if graph and set(graph) != executable_ids:
        missing = sorted(executable_ids - set(graph))
        extra = sorted(set(graph) - executable_ids)
        detail = []
        if missing:
            detail.append(f"missing {', '.join(missing)}")
        if extra:
            detail.append(f"unknown {', '.join(extra)}")
        diagnostics.append(Diagnostic(1, "tasks/graph-task-mismatch", f"Graph and executable checklist differ: {'; '.join(detail)}."))

    task_by_id = {task.id: task for task in executable}
    for parent in parents:
        if parent.kind != "group":
            continue
        for index, child in enumerate(parent.children[:-1]):
            if child.kind != "test" or parent.children[index + 1].kind != "implementation":
                continue
            implementation = parent.children[index + 1]
            if implementation.id in graph and child.id not in graph[implementation.id].depends_on:
                diagnostics.append(Diagnostic(implementation.line, "tasks/missing-pair-dependency", f"Implementation {implementation.id} must depend directly on RED task {child.id}."))

    diagnostics.extend(validate_task_traceability(path, list(task_by_id.values())))
    return diagnostics


def validate(path: Path) -> list[Diagnostic]:
    lines = path.read_text(encoding="utf-8").splitlines()
    visible = visible_lines(lines)
    diagnostics = required_section_diagnostics(path, visible)
    if path.name == "requirements.md":
        diagnostics.extend(validate_requirements(visible))
    elif path.name == "design.md":
        diagnostics.extend(validate_design(path, lines, visible))
    elif path.name == "tasks.md":
        diagnostics.extend(validate_tasks(path, lines, visible))
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
