from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_spec.py")
TEMPLATES = Path(__file__).parents[1] / "assets" / "templates"
SKILL = Path(__file__).parents[1] / "SKILL.md"


class ValidateSpecTest(unittest.TestCase):
    def run_validator(self, path: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(path)],
            capture_output=True,
            text=True,
            check=False,
        )

    def write(self, root: Path, name: str, content: str | None = None) -> Path:
        path = root / name
        path.write_text(
            content if content is not None else (TEMPLATES / name).read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        return path

    def assert_valid(self, path: Path) -> None:
        result = self.run_validator(path)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")

    def test_templates_are_structurally_valid(self) -> None:
        for name in ("requirements.md", "bugfix.md", "tasks.md"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                self.assert_valid(self.write(Path(directory), name))

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            design = (TEMPLATES / "design.md").read_text(encoding="utf-8")
            self.assert_valid(self.write(root, "design.md", design))
            start = design.index("## Correctness Properties")
            end = design.index("## Error Handling")
            self.assert_valid(self.write(root, "design.md", design[:start] + design[end:]))

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "bugfix.md")
            bugfix_design = (TEMPLATES / "design-bugfix.md").read_text(encoding="utf-8")
            self.assert_valid(self.write(root, "design.md", bugfix_design))

    def test_missing_required_sections_are_aggregated_and_fenced_headings_do_not_count(self) -> None:
        content = """# Requirements Document: Example

```markdown
## Introduction
## Glossary
```

## Requirements

### Requirement 1: Valid

**User Story:** As a user, I want a result, so that I benefit.

#### Acceptance Criteria
"""
        with tempfile.TemporaryDirectory() as directory:
            path = self.write(Path(directory), "requirements.md", content)
            result = self.run_validator(path)

        self.assertEqual(result.returncode, 1)
        self.assertIn("[requirements/missing-introduction]", result.stderr)
        self.assertIn("[requirements/missing-glossary]", result.stderr)

    def test_required_section_codes_cover_feature_bugfix_design_and_bugfix_analysis(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            content = (TEMPLATES / "design.md").read_text(encoding="utf-8").replace(
                "## Component Hierarchy", "## Runtime Components"
            )
            result = self.run_validator(self.write(root, "design.md", content))
            self.assertEqual(result.returncode, 1)
            self.assertIn("[design/missing-component-hierarchy]", result.stderr)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "bugfix.md")
            content = (TEMPLATES / "design-bugfix.md").read_text(encoding="utf-8").replace(
                "## Affected Hierarchy", "## Affected Files"
            )
            result = self.run_validator(self.write(root, "design.md", content))
            self.assertEqual(result.returncode, 1)
            self.assertIn("[design/missing-affected-hierarchy]", result.stderr)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            content = (TEMPLATES / "bugfix.md").read_text(encoding="utf-8").replace(
                "## Expected Behavior", "## Expected Result"
            )
            result = self.run_validator(self.write(root, "bugfix.md", content))
            self.assertEqual(result.returncode, 1)
            self.assertIn("[bugfix/missing-expected-behavior]", result.stderr)

    def test_every_requirement_block_needs_story_and_acceptance_heading(self) -> None:
        content = """# Requirements Document: Example

## Introduction

Text.

## Glossary

- **Term**: Definition.

## Requirements

### Requirement 1: Complete

**User Story:** As a user, I want a result, so that I benefit.

#### Acceptance Criteria

1. WHEN used, THE System SHALL respond.

### Requirement 2: Missing story

#### Acceptance Criteria

1. WHEN used, THE System SHALL respond.

### Requirement 3: Missing criteria

**User Story:** As a user, I want another result, so that I benefit.
"""
        with tempfile.TemporaryDirectory() as directory:
            path = self.write(Path(directory), "requirements.md", content)
            result = self.run_validator(path)

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr.count("requirements/missing-user-story"), 1)
        self.assertEqual(result.stderr.count("requirements/missing-acceptance-criteria"), 1)

    def test_requirements_need_at_least_one_requirement_block(self) -> None:
        content = """# Requirements Document: Example

## Introduction

Text.

## Glossary

- **Term**: Definition.

## Requirements

No requirement blocks.
"""
        with tempfile.TemporaryDirectory() as directory:
            path = self.write(Path(directory), "requirements.md", content)
            result = self.run_validator(path)

        self.assertEqual(result.returncode, 1)
        self.assertIn("[requirements/missing-requirement-block]", result.stderr)

    def test_tasks_require_checklist_and_single_json_graph(self) -> None:
        content = """# Implementation Plan: Example

## Overview

Text.

## Tasks

No checkboxes.

## Task Dependency Graph

## Notes

Text.
"""
        with tempfile.TemporaryDirectory() as directory:
            path = self.write(Path(directory), "tasks.md", content)
            result = self.run_validator(path)

        self.assertEqual(result.returncode, 1)
        self.assertIn("[tasks/missing-task-checkbox]", result.stderr)
        self.assertIn("[tasks/missing-dag-json]", result.stderr)
        self.assertNotIn("missing-dependency-tree", result.stderr)
        self.assertNotIn("missing-dependency-table", result.stderr)

    def test_missing_task_dependency_graph_uses_stable_code(self) -> None:
        content = (TEMPLATES / "tasks.md").read_text(encoding="utf-8").replace(
            "## Task Dependency Graph", "## Dependency Plan"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = self.write(Path(directory), "tasks.md", content)
            result = self.run_validator(path)

        self.assertEqual(result.returncode, 1)
        self.assertIn("[tasks/missing-dependency-graph]", result.stderr)

    def test_bad_inputs_exit_two(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            missing = self.run_validator(root / "requirements.md")
            unsupported = self.run_validator(self.write(root, "notes.md", "# Notes\n"))

        self.assertEqual(missing.returncode, 2)
        self.assertIn("error: cannot read document", missing.stderr)
        self.assertEqual(unsupported.returncode, 2)
        self.assertIn("error: unsupported document", unsupported.stderr)

    def test_skill_makes_per_artifact_validation_a_phase_gate(self) -> None:
        content = SKILL.read_text(encoding="utf-8")
        self.assertIn("## Validate Each Artifact", content)
        self.assertIn(
            "python <skill-directory>/scripts/validate_spec.py docs/specs/<slug>/<artifact>",
            content,
        )
        for order in (
            "`requirements.md` → `design.md` → `tasks.md`",
            "`design.md` → `requirements.md` → synchronized `design.md` → `tasks.md`",
            "`bugfix.md` → `design.md` → `tasks.md`",
        ):
            self.assertIn(order, content)
        self.assertIn("Request approval only after validation passes", content)

    def test_skill_routes_before_discovery_and_scaffolding(self) -> None:
        content = SKILL.read_text(encoding="utf-8")
        choice = content.index("## Choose the Workflow First")
        discovery = content.index("## Complete Discovery Before Files")
        scaffold = content.index("## Start or Resume a Spec")
        self.assertLess(choice, discovery)
        self.assertLess(discovery, scaffold)
        self.assertIn("Requirements-First", content)
        self.assertIn("Design-First", content)
        self.assertIn("Quick Plan", content)
        self.assertIn("recommend one with a one-sentence reason", content)
        self.assertIn("wait for the user's choice", content)
        self.assertIn("create only the current artifact", content)


if __name__ == "__main__":
    unittest.main()
