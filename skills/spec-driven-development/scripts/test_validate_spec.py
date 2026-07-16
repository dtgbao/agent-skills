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

    def test_templates_are_valid_and_correctness_properties_is_optional(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("requirements.md", "bugfix.md", "tasks.md"):
                self.assert_valid(self.write(root, name))

            design = (TEMPLATES / "design.md").read_text(encoding="utf-8")
            start = design.index("## Correctness Properties")
            end = design.index("## Error Handling")
            self.assert_valid(self.write(root, "design.md", design[:start] + design[end:]))

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
        self.assertIn("[requirements/missing-introduction] Missing required section: ## Introduction", result.stderr)
        self.assertIn("[requirements/missing-glossary] Missing required section: ## Glossary", result.stderr)

    def test_required_section_codes_cover_design_and_bugfix(self) -> None:
        cases = (
            ("design.md", "## Architecture", "## architecture", "design/missing-architecture"),
            ("bugfix.md", "## Expected Behavior", "## Expected Result", "bugfix/missing-expected-behavior"),
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, heading, replacement, code in cases:
                with self.subTest(name=name):
                    content = (TEMPLATES / name).read_text(encoding="utf-8").replace(heading, replacement)
                    result = self.run_validator(self.write(root, name, content))
                    self.assertEqual(result.returncode, 1)
                    self.assertIn(f"[{code}] Missing required section: {heading}", result.stderr)

    def test_every_requirement_block_needs_its_own_story_and_acceptance_heading(self) -> None:
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

### Requirement 4: Missing both

```markdown
**User Story:** Fake.
#### Acceptance Criteria
```
"""
        with tempfile.TemporaryDirectory() as directory:
            path = self.write(Path(directory), "requirements.md", content)
            result = self.run_validator(path)

        self.assertEqual(result.returncode, 1)
        lines = content.splitlines()
        story_line = lines.index("### Requirement 2: Missing story") + 1
        criteria_line = lines.index("### Requirement 3: Missing criteria") + 1
        both_line = lines.index("### Requirement 4: Missing both") + 1
        self.assertIn(f"{path}:{story_line}:1: error [requirements/missing-user-story]", result.stderr)
        self.assertIn(f"{path}:{criteria_line}:1: error [requirements/missing-acceptance-criteria]", result.stderr)
        self.assertIn(f"{path}:{both_line}:1: error [requirements/missing-user-story]", result.stderr)
        self.assertIn(f"{path}:{both_line}:1: error [requirements/missing-acceptance-criteria]", result.stderr)
        self.assertEqual(result.stderr.count("requirements/missing-user-story"), 2)
        self.assertEqual(result.stderr.count("requirements/missing-acceptance-criteria"), 2)
        self.assertIn("Requirement block is missing **User Story:**", result.stderr)
        self.assertIn("Requirement block is missing #### Acceptance Criteria", result.stderr)

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
        self.assertIn(f"{path}:11:1: error [requirements/missing-requirement-block]", result.stderr)

    def test_task_graph_structures_and_checklist_are_required(self) -> None:
        content = """# Implementation Plan: Example

## Overview

Text.

## Task Dependency Graph

## Tasks

No checkboxes.

## Notes

Text.
"""
        with tempfile.TemporaryDirectory() as directory:
            path = self.write(Path(directory), "tasks.md", content)
            result = self.run_validator(path)

        self.assertEqual(result.returncode, 1)
        for code in (
            "tasks/missing-dag-json",
            "tasks/missing-dependency-tree",
            "tasks/missing-dependency-table",
            "tasks/missing-task-checkbox",
        ):
            self.assertIn(f"[{code}]", result.stderr)

    def test_task_waves_reject_invalid_json_and_invalid_identifiers(self) -> None:
        template = (TEMPLATES / "tasks.md").read_text(encoding="utf-8")
        json_start = template.index("```json") + len("```json")
        json_end = template.index("```", json_start)

        def with_json(value: str) -> str:
            return template[:json_start] + "\n" + value + "\n" + template[json_end:]

        cases = {
            "invalid-json": (with_json("{"), "tasks/invalid-dag-json"),
            "empty-waves": (with_json('{"waves": []}'), "tasks/invalid-dag-waves"),
            "duplicate-task": (
                with_json('{"waves": [{"wave": 1, "tasks": [1]}, {"wave": 2, "tasks": [1]}]}'),
                "tasks/invalid-dag-waves",
            ),
            "nonpositive-task": (with_json('{"waves": [{"wave": 1, "tasks": [0]}]}'), "tasks/invalid-dag-waves"),
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for label, (content, code) in cases.items():
                with self.subTest(label=label):
                    path = self.write(root, "tasks.md", content)
                    result = self.run_validator(path)
                    self.assertEqual(result.returncode, 1)
                    self.assertIn(f"[{code}]", result.stderr)

    def test_task_dependency_table_needs_a_mapping_row(self) -> None:
        template = (TEMPLATES / "tasks.md").read_text(encoding="utf-8")
        start = template.index("| 1    | —")
        end = template.index("\n\n---", start)
        content = template[:start] + template[end:]
        with tempfile.TemporaryDirectory() as directory:
            path = self.write(Path(directory), "tasks.md", content)
            result = self.run_validator(path)

        self.assertEqual(result.returncode, 1)
        self.assertIn("[tasks/missing-dependency-table]", result.stderr)

    def test_missing_task_dependency_graph_uses_kiro_compatible_code(self) -> None:
        content = (TEMPLATES / "tasks.md").read_text(encoding="utf-8").replace(
            "## Task Dependency Graph", "## Dependency Plan"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = self.write(Path(directory), "tasks.md", content)
            result = self.run_validator(path)

        self.assertEqual(result.returncode, 1)
        self.assertIn("[tasks/missing-dependency-graph] Missing required section: ## Task Dependency Graph", result.stderr)

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

    def test_skill_requires_workflow_choice_before_scaffolding(self) -> None:
        content = SKILL.read_text(encoding="utf-8")
        choice = content.index("## Choose Workflow Before Creating Files")
        scaffold = content.index("## Start or Resume a Spec")
        self.assertLess(choice, scaffold)
        self.assertIn("Requirements-First, Design-First, and Quick Plan", content)
        self.assertIn("State the recommendation and one-sentence reason", content)
        self.assertIn("Wait for the user's choice before calling the initializer", content)
        self.assertIn("--artifact <artifact>", content)
        self.assertIn("create only the artifact for the current phase", content)


if __name__ == "__main__":
    unittest.main()
