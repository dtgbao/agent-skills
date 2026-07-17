from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).parents[1]
REPOSITORY_ROOT = SKILL_ROOT.parents[1]
EXAMPLE = REPOSITORY_ROOT / "examples" / "codex-roamly-guest-booking-mvp-improved"
VALIDATOR = SKILL_ROOT / "scripts" / "validate_spec.py"


class ImprovedBenchmarkTest(unittest.TestCase):
    def test_improved_example_meets_the_enforced_contract(self) -> None:
        paths = [EXAMPLE / name for name in ("requirements.md", "design.md", "tasks.md")]
        for path in paths:
            with self.subTest(path=path.name):
                self.assertTrue(path.is_file(), f"missing benchmark artifact: {path}")
                result = subprocess.run(
                    [sys.executable, str(VALIDATOR), str(path)],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)

        design = (EXAMPLE / "design.md").read_text(encoding="utf-8")
        for heading in (
            "## Key Design Decisions",
            "## Repository Structure",
            "## Component Hierarchy",
            "## Operations",
            "## Flows and Strategies",
            "## Error Handling",
            "## Testing Strategy",
            "## Traceability",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, design)
        self.assertGreaterEqual(len(re.findall(r"^```mermaid$", design, flags=re.MULTILINE)), 2)
        self.assertGreaterEqual(
            len(re.findall(r"^```(?:typescript|tsx|javascript|sql|python|pseudocode)$", design, flags=re.MULTILINE)),
            3,
        )
        self.assertIn("defineSchema", design)
        self.assertIn("defineTable", design)
        self.assertIn("### Queries", design)
        self.assertIn("### Mutations", design)
        self.assertIn("| Scenario | System Response | Caller or UI Recovery | Validates |", design)

        tasks = (EXAMPLE / "tasks.md").read_text(encoding="utf-8")
        parent_count = len(re.findall(r"^- \[[ xX]\](?:\\?\*)? \d+\. ", tasks, flags=re.MULTILINE))
        child_count = len(re.findall(r"^  - \[[ xX]\](?:\\?\*)? \d+\.\d+ ", tasks, flags=re.MULTILINE))
        red_count = len(re.findall(r"^    - \*\*RED:\*\*", tasks, flags=re.MULTILINE))
        green_count = len(re.findall(r"^    - \*\*GREEN:\*\*", tasks, flags=re.MULTILINE))
        self.assertGreater(parent_count, 0)
        self.assertGreater(child_count, parent_count)
        self.assertGreater(red_count, 0)
        self.assertEqual(red_count, green_count)
        self.assertIn('"dependsOn"', tasks)
        self.assertNotIn("| Task | Depends On |", tasks)


if __name__ == "__main__":
    unittest.main()
