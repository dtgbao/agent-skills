from __future__ import annotations

import re
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).parents[1]
SKILL = SKILL_ROOT / "SKILL.md"
REFERENCES = SKILL_ROOT / "references"
COPIED_REFERENCES = (
    REFERENCES / "brainstorming.md",
    REFERENCES / "design-and-task-planning.md",
    REFERENCES / "test-driven-development.md",
)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+\.md(?:#[^)]*)?)\)")


class SkillReferencesTest(unittest.TestCase):
    def test_feature_brainstorming_precedes_workflow_choice_and_bugfixes_stay_evidence_first(self) -> None:
        content = SKILL.read_text(encoding="utf-8")
        brainstorming = content.index("## Brainstorm Feature Ideas Before Choosing a Workflow")
        workflow_choice = content.index("## Choose Workflow Before Creating Files")

        self.assertLess(brainstorming, workflow_choice)
        self.assertIn("For a defect, begin with the Bugfix workflow choice and evidence flow", content)

    def test_skill_directly_routes_every_reference(self) -> None:
        content = SKILL.read_text(encoding="utf-8")
        for link in (
            "[brainstorming](references/brainstorming.md)",
            "[design and task planning](references/design-and-task-planning.md)",
            "[test-driven development](references/test-driven-development.md)",
            "[testing anti-patterns](references/testing-anti-patterns.md)",
        ):
            with self.subTest(link=link):
                self.assertIn(link, content)

    def test_copied_references_are_plain_reference_documents(self) -> None:
        for path in COPIED_REFERENCES:
            with self.subTest(path=path.name):
                self.assertFalse(path.read_text(encoding="utf-8").startswith("---"))

    def test_long_references_have_contents_indexes(self) -> None:
        for path in REFERENCES.glob("*.md"):
            content = path.read_text(encoding="utf-8")
            if len(content.splitlines()) > 100:
                with self.subTest(path=path.name):
                    self.assertIn("## Contents", content)

    def test_superpowers_footprints_are_removed(self) -> None:
        forbidden = (
            "superpowers",
            "writing-plans",
            "subagent-driven-development",
            "executing-plans",
            "frontend-design",
            "mcp-builder",
            "elements-of-style",
            "visual-companion.md",
        )
        paths = (SKILL, *REFERENCES.glob("*.md"))
        for path in paths:
            content = path.read_text(encoding="utf-8").lower()
            for footprint in forbidden:
                with self.subTest(path=path.name, footprint=footprint):
                    self.assertNotIn(footprint, content)

    def test_local_markdown_links_resolve(self) -> None:
        paths = (SKILL, *REFERENCES.glob("*.md"))
        for path in paths:
            content = path.read_text(encoding="utf-8")
            for target in MARKDOWN_LINK_RE.findall(content):
                local_path = target.split("#", 1)[0]
                if "://" in local_path:
                    continue
                with self.subTest(path=path.name, target=target):
                    self.assertTrue((path.parent / local_path).resolve().is_file())


if __name__ == "__main__":
    unittest.main()
