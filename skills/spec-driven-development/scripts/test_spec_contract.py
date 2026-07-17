from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_spec.py")


class SpecContractTest(unittest.TestCase):
    def run_validator(self, path: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(path)],
            capture_output=True,
            text=True,
            check=False,
        )

    def write(self, root: Path, name: str, content: str) -> Path:
        path = root / name
        path.write_text(content, encoding="utf-8")
        return path

    def assert_valid(self, path: Path) -> None:
        result = self.run_validator(path)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")

    def feature_design(self) -> str:
        return """# Design Document: Example

## Overview

Build the approved booking capability in the existing application.

## Key Design Decisions

- Keep availability checks and booking insertion in one transaction.

## Architecture

```mermaid
flowchart LR
    Browser --> BookingService --> Database
```

## Repository Structure

```text
src/
└── booking/
    ├── service.ts
    └── service.test.ts
```

## Component Hierarchy

```text
BookingPage
└── BookingForm
    └── DateRangeField
```

## Components and Interfaces

### Booking service

```typescript
interface BookingService {
  create(input: CreateBookingInput): Promise<BookingReceipt>;
}
```

## Data Models

```typescript
type Booking = {
  id: string;
  checkIn: string;
  checkOut: string;
};
```

## Operations

### Mutations

| Operation | Input | Output | Errors | Validates |
| --- | --- | --- | --- | --- |
| `bookings.create` | `CreateBookingInput` | `BookingReceipt` | `DATES_UNAVAILABLE` | 1.1 |

## Flows and Strategies

### Conflict-safe booking

```mermaid
sequenceDiagram
    Browser->>BookingService: create(input)
    BookingService->>Database: check and insert transactionally
    Database-->>BookingService: receipt or conflict
```

```pseudocode
if overlaps(existing, requested): reject
insert booking
```

## Error Handling

| Scenario | System Response | Caller or UI Recovery | Validates |
| --- | --- | --- | --- |
| Dates overlap | Return `DATES_UNAVAILABLE` without a write | Ask for new dates | 1.1 |

## Testing Strategy

| Behavior | Level | Evidence | Validates |
| --- | --- | --- | --- |
| Racing requests have one winner | Integration | Two concurrent callers | 1.1 |

## Traceability

| Source | Design Elements | Verification |
| --- | --- | --- |
| 1.1 | Booking mutation and conflict flow | Integration race test |
"""

    def bugfix_design(self) -> str:
        return """# Design Document: Example Fix

## Overview

Correct duplicate booking creation without changing adjacent bookings.

## Key Design Decisions

- Move the overlap check into the shared transactional mutation.

## Architecture

```mermaid
flowchart LR
    Caller --> BookingMutation --> Database
```

## Affected Hierarchy

```text
bookingRoute
└── createBooking
    └── bookingRepository
```

## Root Cause and Fix

```mermaid
flowchart LR
    Read[Separate availability read] --> Race[Concurrent insert race]
    Race --> Fix[Transactional check and insert]
```

## Changed Interfaces

```typescript
declare function createBooking(input: BookingInput): Promise<BookingResult>;
```

## Data Model Changes

**Not applicable:** The fix changes transaction ownership but not persisted fields.

## Error Handling

| Scenario | System Response | Caller or UI Recovery | Validates |
| --- | --- | --- | --- |
| Conflicting booking | Return `DATES_UNAVAILABLE` | Preserve entered dates | EB1, UB1 |

## Regression Strategy

| Boundary | Test Evidence | Validates |
| --- | --- | --- |
| Concurrent conflict | Reproduce with two callers | EB1 |
| Adjacent bookings | Preserve successful insertion | UB1 |

## Traceability

| Source | Design Elements | Verification |
| --- | --- | --- |
| EB1, UB1 | Transactional mutation | Regression test |
"""

    def requirements(self) -> str:
        return """# Requirements Document: Example

## Introduction

Provide conflict-safe booking.

## Glossary

- **Booking:** A confirmed stay.

## Requirements

### Requirement 1: Conflict-safe booking

**User Story:** As a guest, I want conflicting requests rejected, so that my booking is trustworthy.

#### Acceptance Criteria

1. WHEN two requests overlap, THE System SHALL confirm at most one booking.
"""

    def bugfix(self) -> str:
        return """# Bugfix Analysis: Example

## Issue Summary

Concurrent callers can create duplicates.

## Reproduction and Evidence

1. Submit two overlapping bookings.

- **Observed result:** Both succeed.
- **Frequency:** Always under the synchronized test.

## Current Behavior

1. **CB1** — WHEN requests race, THEN THE System creates duplicate bookings.

## Expected Behavior

1. **EB1** — WHEN requests race, THE System SHALL confirm at most one booking.

## Unchanged Behavior

1. **UB1** — WHEN bookings are adjacent, THE System SHALL CONTINUE TO accept both.

## Fix Constraints and Regression Boundaries

- **In scope:** Booking mutation transaction ownership.
- **Out of scope:** Search behavior.
- **Constraint:** Preserve adjacent intervals.
"""

    def tasks_document(
        self,
        *,
        requirement: str = "1.1",
        implementation_depends_on: list[str] | None = None,
        include_test_in_graph: bool = True,
        parent_checked: bool = False,
        child_checked: bool = False,
    ) -> str:
        checked_parent = "x" if parent_checked else " "
        checked_child = "x" if child_checked else " "
        dependencies = ["1.1"] if implementation_depends_on is None else implementation_depends_on
        waves: list[dict[str, object]] = []
        if include_test_in_graph:
            waves.append({"wave": 1, "tasks": [{"id": "1.1", "dependsOn": []}]})
        waves.extend(
            [
                {"wave": 2, "tasks": [{"id": "1.2", "dependsOn": dependencies}]},
                {"wave": 3, "tasks": [{"id": "2", "dependsOn": ["1.2"]}]},
            ]
        )
        graph = json.dumps({"waves": waves}, indent=2)
        trace_kind = "Bugfix" if requirement.startswith(("EB", "UB", "CB")) else "Requirements"
        return f"""# Implementation Plan: Example

## Overview

Implement and verify conflict-safe booking in dependency order.

## Tasks

- [{checked_parent}] 1. Deliver conflict-safe booking
  - [{checked_child}] 1.1 Prove overlapping requests cannot both succeed
    - **RED:** Add a focused concurrent booking test asserting one confirmation and one conflict.
    - **Verify RED:** Run `pytest tests/test_booking.py -v`; expect both requests to succeed before the fix.
    - _{trace_kind}: {requirement}_
  - [{checked_child}] 1.2 Implement transactional conflict detection
    - **GREEN:** Move overlap detection and insertion into the shared booking transaction defined in `design.md`.
    - **Verify GREEN:** Run `pytest tests/test_booking.py -v`; expect one confirmation and one conflict.
    - **REFACTOR:** Keep one overlap predicate and rerun `pytest tests/test_booking.py -v`.
    - _{trace_kind}: {requirement}_

- [ ] 2. Checkpoint — booking behavior is integrated
  - **Check:** Run `pytest -q`.
  - **Expected:** The complete suite passes without warnings.
  - _{trace_kind}: {requirement}_

## Task Dependency Graph

```json
{graph}
```

## Notes

- Parent tasks contain architecture-free execution leaves.
"""

    def exception_document(self, *, include_approval: bool = True) -> str:
        approval = "  - **Approval:** The user approved configuration-only generation.\n" if include_approval else ""
        return f"""# Implementation Plan: Example

## Overview

Generate configuration with explicit verification.

## Tasks

- [ ] 1. [TDD Exception] Generate checked-in configuration
  - **Reason:** The output is generated from the approved schema.
{approval}  - **Check:** Run `python3 scripts/generate.py --check`; expect no diff.
  - _Requirements: 1.1_

## Task Dependency Graph

```json
{{"waves": [{{"wave": 1, "tasks": [{{"id": "1", "dependsOn": []}}]}}]}}
```

## Notes

- The exception is limited to generated output.
"""

    def test_valid_feature_and_bugfix_designs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "requirements.md", self.requirements())
            self.assert_valid(self.write(root, "design.md", self.feature_design()))

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "bugfix.md", self.bugfix())
            self.assert_valid(self.write(root, "design.md", self.bugfix_design()))

    def test_feature_design_requires_hierarchies_native_contracts_and_flow_diagrams(self) -> None:
        cases = {
            "missing-repository": (
                self.feature_design().replace("## Repository Structure", "## Repository Map"),
                "design/missing-repository-structure",
            ),
            "missing-component": (
                self.feature_design().replace("## Component Hierarchy", "## Components Tree"),
                "design/missing-component-hierarchy",
            ),
            "generic-contract": (
                self.feature_design().replace("```typescript\ninterface BookingService", "```text\ninterface BookingService", 1),
                "design/missing-native-contract",
            ),
            "missing-flow": (
                self.feature_design().replace("```mermaid\nsequenceDiagram", "```text\nsequenceDiagram"),
                "design/missing-flow-diagram",
            ),
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "requirements.md", self.requirements())
            for label, (content, code) in cases.items():
                with self.subTest(label=label):
                    result = self.run_validator(self.write(root, "design.md", content))
                    self.assertEqual(result.returncode, 1)
                    self.assertIn(f"[{code}]", result.stderr)

    def test_design_tables_are_contracts_not_decorative_pipes(self) -> None:
        content = self.feature_design().replace(
            "| Scenario | System Response | Caller or UI Recovery | Validates |",
            "| Problem | Response | Recovery | Source |",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "requirements.md", self.requirements())
            result = self.run_validator(self.write(root, "design.md", content))

        self.assertEqual(result.returncode, 1)
        self.assertIn("[design/missing-error-table]", result.stderr)

    def test_bugfix_design_uses_focused_hierarchy_and_root_cause_flow(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "bugfix.md", self.bugfix())
            cases = {
                "hierarchy": (
                    self.bugfix_design().replace("## Affected Hierarchy", "## Affected Files"),
                    "design/missing-affected-hierarchy",
                ),
                "flow": (
                    self.bugfix_design().replace("```mermaid\nflowchart LR\n    Read", "```text\nflowchart LR\n    Read"),
                    "design/missing-root-cause-flow",
                ),
            }
            for label, (content, code) in cases.items():
                with self.subTest(label=label):
                    result = self.run_validator(self.write(root, "design.md", content))
                    self.assertEqual(result.returncode, 1)
                    self.assertIn(f"[{code}]", result.stderr)

    def test_valid_hierarchical_tasks_and_bugfix_traceability(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "requirements.md", self.requirements())
            self.assert_valid(self.write(root, "tasks.md", self.tasks_document()))

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "bugfix.md", self.bugfix())
            self.assert_valid(self.write(root, "tasks.md", self.tasks_document(requirement="EB1, UB1")))

    def test_legacy_flat_tasks_are_rejected(self) -> None:
        content = """# Implementation Plan: Legacy

## Overview

Legacy flat task.

## Tasks

- [ ] 1. Add behavior
  - **RED:** Add a failing test.
  - **Verify RED:** Run `pytest`; expect failure.
  - **GREEN:** Implement behavior.
  - **Verify GREEN:** Run `pytest`; expect success.
  - **REFACTOR:** Remove duplication and rerun `pytest`.

## Task Dependency Graph

```json
{"waves": [{"wave": 1, "tasks": [1]}]}
```

## Notes

Legacy format.
"""
        with tempfile.TemporaryDirectory() as directory:
            path = self.write(Path(directory), "tasks.md", content)
            result = self.run_validator(path)

        self.assertEqual(result.returncode, 1)
        self.assertIn("[tasks/legacy-flat-task]", result.stderr)

    def test_task_pairs_and_graph_must_agree(self) -> None:
        cases = {
            "missing-test-id": (self.tasks_document(include_test_in_graph=False), "tasks/graph-task-mismatch"),
            "missing-pair-dependency": (
                self.tasks_document(implementation_depends_on=[]),
                "tasks/missing-pair-dependency",
            ),
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "requirements.md", self.requirements())
            for label, (content, code) in cases.items():
                with self.subTest(label=label):
                    result = self.run_validator(self.write(root, "tasks.md", content))
                    self.assertEqual(result.returncode, 1)
                    self.assertIn(f"[{code}]", result.stderr)

    def test_orphaned_and_oversized_subtasks_are_rejected(self) -> None:
        orphan = self.tasks_document().replace(
            "  - [ ] 1.2 Implement transactional conflict detection\n"
            "    - **GREEN:** Move overlap detection and insertion into the shared booking transaction defined in `design.md`.\n"
            "    - **Verify GREEN:** Run `pytest tests/test_booking.py -v`; expect one confirmation and one conflict.\n"
            "    - **REFACTOR:** Keep one overlap predicate and rerun `pytest tests/test_booking.py -v`.\n"
            "    - _Requirements: 1.1_\n",
            "",
        )
        oversized = self.tasks_document().replace(
            "    - _Requirements: 1.1_",
            "    - Add another peer implementation instruction.\n    - _Requirements: 1.1_",
            1,
        )
        cases = {
            "orphan": (orphan, "tasks/orphan-test"),
            "oversized": (oversized, "tasks/unexpected-subtask-entry"),
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "requirements.md", self.requirements())
            for label, (content, code) in cases.items():
                with self.subTest(label=label):
                    result = self.run_validator(self.write(root, "tasks.md", content))
                    self.assertEqual(result.returncode, 1)
                    self.assertIn(f"[{code}]", result.stderr)

    def test_graph_rejects_invalid_ids_cycles_and_nonsequential_waves(self) -> None:
        template = self.tasks_document()
        graph_start = template.index("```json") + len("```json")
        graph_end = template.index("```", graph_start)

        def with_graph(value: object) -> str:
            return template[:graph_start] + "\n" + json.dumps(value) + "\n" + template[graph_end:]

        cases = {
            "invalid-id": (
                with_graph({"waves": [{"wave": 1, "tasks": [{"id": 1, "dependsOn": []}]}]}),
                "tasks/invalid-dag-task",
            ),
            "cycle": (
                with_graph(
                    {
                        "waves": [
                            {"wave": 1, "tasks": [{"id": "1.1", "dependsOn": ["1.2"]}]},
                            {"wave": 2, "tasks": [{"id": "1.2", "dependsOn": ["1.1"]}]},
                            {"wave": 3, "tasks": [{"id": "2", "dependsOn": ["1.2"]}]},
                        ]
                    }
                ),
                "tasks/dependency-cycle",
            ),
            "wave-gap": (
                with_graph(
                    {
                        "waves": [
                            {"wave": 1, "tasks": [{"id": "1.1", "dependsOn": []}]},
                            {"wave": 3, "tasks": [{"id": "1.2", "dependsOn": ["1.1"]}]},
                            {"wave": 4, "tasks": [{"id": "2", "dependsOn": ["1.2"]}]},
                        ]
                    }
                ),
                "tasks/invalid-dag-waves",
            ),
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "requirements.md", self.requirements())
            for label, (content, code) in cases.items():
                with self.subTest(label=label):
                    result = self.run_validator(self.write(root, "tasks.md", content))
                    self.assertEqual(result.returncode, 1)
                    self.assertIn(f"[{code}]", result.stderr)

    def test_checkpoint_and_exception_forms_are_exact(self) -> None:
        incomplete_checkpoint = self.tasks_document().replace(
            "  - **Expected:** The complete suite passes without warnings.\n",
            "",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "requirements.md", self.requirements())
            self.assert_valid(self.write(root, "tasks.md", self.exception_document()))

            result = self.run_validator(self.write(root, "tasks.md", self.exception_document(include_approval=False)))
            self.assertEqual(result.returncode, 1)
            self.assertIn("[tasks/incomplete-tdd-exception]", result.stderr)

            result = self.run_validator(self.write(root, "tasks.md", incomplete_checkpoint))
            self.assertEqual(result.returncode, 1)
            self.assertIn("[tasks/missing-checkpoint-verification]", result.stderr)

    def test_task_traceability_and_parent_state_are_enforced(self) -> None:
        cases = {
            "unknown-requirement": (self.tasks_document(requirement="9.9"), "tasks/invalid-traceability"),
            "checked-parent": (
                self.tasks_document(parent_checked=True, child_checked=False),
                "tasks/inconsistent-parent-state",
            ),
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "requirements.md", self.requirements())
            for label, (content, code) in cases.items():
                with self.subTest(label=label):
                    result = self.run_validator(self.write(root, "tasks.md", content))
                    self.assertEqual(result.returncode, 1)
                    self.assertIn(f"[{code}]", result.stderr)

    def test_required_upstream_coverage_is_complete(self) -> None:
        requirements = self.requirements().replace(
            "1. WHEN two requests overlap, THE System SHALL confirm at most one booking.",
            "1. WHEN two requests overlap, THE System SHALL confirm at most one booking.\n"
            "2. WHEN bookings are adjacent, THE System SHALL accept both bookings.",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "requirements.md", requirements)
            result = self.run_validator(self.write(root, "tasks.md", self.tasks_document()))

        self.assertEqual(result.returncode, 1)
        self.assertIn("[tasks/missing-upstream-coverage]", result.stderr)


if __name__ == "__main__":
    unittest.main()
