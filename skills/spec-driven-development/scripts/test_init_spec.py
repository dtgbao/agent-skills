from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("init_spec.py")


class InitSpecTest(unittest.TestCase):
    def run_script(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_feature_artifacts_are_created_one_phase_at_a_time(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = self.run_script(root, "dogfinder", "--title", "DogFinder")
            target = root / "docs/specs/dogfinder"

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual({path.name for path in target.iterdir()}, {"requirements.md"})
            requirements = (target / "requirements.md").read_text(encoding="utf-8")
            self.assertIn("DogFinder", requirements)
            self.assertNotIn("{{SPEC_TITLE}}", requirements)
            self.assertIn("## Requirements", requirements)

            design_result = self.run_script(root, "dogfinder", "--title", "DogFinder", "--artifact", "design")
            self.assertEqual(design_result.returncode, 0, design_result.stderr)
            self.assertEqual({path.name for path in target.iterdir()}, {"requirements.md", "design.md"})
            self.assertIn("## Architecture", (target / "design.md").read_text(encoding="utf-8"))

            tasks_result = self.run_script(root, "dogfinder", "--title", "DogFinder", "--artifact", "tasks")
            self.assertEqual(tasks_result.returncode, 0, tasks_result.stderr)
            self.assertEqual(
                {path.name for path in target.iterdir()},
                {"requirements.md", "design.md", "tasks.md"},
            )
            tasks = (target / "tasks.md").read_text(encoding="utf-8")
            self.assertIn("## Task Dependency Graph", tasks)
            self.assertIn('"waves"', tasks)
            self.assertIn("1 (foundation)", tasks)
            self.assertIn("| Task | Depends On |", tasks)

            before = {path.name: path.read_bytes() for path in target.iterdir()}
            second = self.run_script(root, "dogfinder", "--title", "Changed", "--artifact", "design")
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual(before, {path.name: path.read_bytes() for path in target.iterdir()})

    def test_bugfix_starts_with_only_bugfix_analysis(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = self.run_script(root, "duplicate-email", "--kind", "bugfix")
            target = root / "docs/specs/duplicate-email"

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual({path.name for path in target.iterdir()}, {"bugfix.md"})
            bugfix = (target / "bugfix.md").read_text(encoding="utf-8")
            self.assertIn("## Current Behavior", bugfix)
            self.assertIn("## Expected Behavior", bugfix)
            self.assertIn("## Unchanged Behavior", bugfix)

            design = self.run_script(root, "duplicate-email", "--artifact", "design")
            self.assertEqual(design.returncode, 0, design.stderr)
            self.assertEqual({path.name for path in target.iterdir()}, {"bugfix.md", "design.md"})


if __name__ == "__main__":
    unittest.main()
