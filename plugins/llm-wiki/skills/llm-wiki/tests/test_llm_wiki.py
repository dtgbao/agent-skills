"""Tests for scripts/llm_wiki.py.

Run: python3 -m unittest discover -s tests -v

Each test uses a temporary HOME, a temporary wiki root and local bare Git
remotes. No test makes a network call; URL sources use file:// URLs.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "llm_wiki.py"
HEADING_RE = re.compile(
    r"^## \[\d{4}-\d{2}-\d{2} \d{2}:\d{2}\] (bootstrap|ingest|query|lint|schema) \| .+$"
)


class WikiTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.root = self.tmp / "wiki-root"
        self.env = {
            "HOME": str(self.home),
            "PATH": os.environ.get("PATH", ""),
            "GIT_AUTHOR_NAME": "Test",
            "GIT_AUTHOR_EMAIL": "test@example.invalid",
            "GIT_COMMITTER_NAME": "Test",
            "GIT_COMMITTER_EMAIL": "test@example.invalid",
            "GIT_CONFIG_NOSYSTEM": "1",
        }

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def run_cli(
        self, *args: str, root: Path | None = None, ok: bool = True, stdin: str = ""
    ) -> dict:
        cmd = [
            sys.executable,
            str(SCRIPT),
            *args,
            "--json",
            "--root",
            str(root or self.root),
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, env=self.env, input=stdin, check=False
        )
        if ok and result.returncode != 0:
            self.fail(
                f"{args} failed ({result.returncode}): {result.stdout}{result.stderr}"
            )
        if not ok and result.returncode == 0:
            self.fail(f"{args} should fail: {result.stdout}")
        data = json.loads(result.stdout)
        data["_exit"] = result.returncode
        return data

    def git(self, cwd: Path, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            env=self.env,
            check=True,
        )
        return result.stdout.strip()

    def init(self, *extra: str) -> dict:
        return self.run_cli("init", *extra)

    def log_text(self) -> str:
        return (self.root / "wiki" / "log.md").read_text()

    def write_page(self, rel: str, **fields: str) -> Path:
        body = fields.pop("body", "Body text.\n")
        meta = {
            "title": "Page",
            "kind": "concept",
            "domain": str(Path(rel).parent),
            "summary": "A short summary.",
            "created": "2026-01-01",
            "updated": "2026-01-02",
        }
        meta.update(fields)
        front = "\n".join(f"{k}: {v}" for k, v in meta.items())
        path = self.root / "wiki" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\n{front}\n---\n\n{body}")
        return path

    def codes(self, report: dict, bucket: str) -> list[str]:
        return [item["code"] for item in report[bucket]]


class InitAndIndexTests(WikiTestCase):
    def test_init_creates_layout_and_logs_bootstrap(self) -> None:
        data = self.init("--domain", "aws/iam")
        for rel in (
            "AGENTS.md",
            "wiki/log.md",
            "wiki/index.md",
            "wiki/aws/iam/index.md",
        ):
            self.assertTrue((self.root / rel).is_file(), rel)
        self.assertTrue((self.root / "raw/aws/iam").is_dir())
        self.assertRegex(data["log_heading"], HEADING_RE)
        self.assertIn("bootstrap", data["log_heading"])

    def test_init_never_overwrites_schema_and_logs_each_run(self) -> None:
        self.init()
        schema = self.root / "AGENTS.md"
        schema.write_text("custom schema\n")
        data = self.init()
        self.assertEqual(schema.read_text(), "custom schema\n")
        self.assertIn("AGENTS.md", data["skipped"])
        self.assertEqual(self.log_text().count("] bootstrap |"), 2)

    def test_index_writes_no_log_entry(self) -> None:
        self.init()
        before = self.log_text()
        self.write_page("ml/attention.md", title="Attention")
        data = self.run_cli("index")
        self.assertIn("wiki/ml/index.md", data["written"])
        self.assertEqual(self.log_text(), before)

    def test_index_uses_summary_field_never_body(self) -> None:
        self.init()
        body = (
            "```python\nprint('code fence')\n```\n\nTODO(llm-wiki): body placeholder\n"
        )
        self.write_page(
            "ml/attention.md",
            title="Attention",
            summary="Weights tokens by relevance.",
            body=body,
        )
        self.write_page(
            "ml/no-summary.md",
            title="No summary",
            summary='""',
            body="First body line.\n",
        )
        self.run_cli("index")
        index = (self.root / "wiki/ml/index.md").read_text()
        self.assertIn(
            "| [Attention](attention.md) | Weights tokens by relevance. |", index
        )
        self.assertIn("_summary pending_", index)
        self.assertNotIn("code fence", index)
        self.assertNotIn("First body line", index)
        self.assertNotIn("TODO(llm-wiki)", index)

    def test_index_row_has_tags_updated_and_source_count(self) -> None:
        self.init()
        self.write_page(
            "ml/attention.md",
            title="Attention",
            tags="[nlp, transformers]",
            sources="[raw/ml/a.md, raw/ml/b.md]",
            updated="2026-03-04",
        )
        self.run_cli("index")
        index = (self.root / "wiki/ml/index.md").read_text()
        self.assertIn("## Concepts", index)
        self.assertIn("| nlp, transformers | 2026-03-04 | 2 |", index)
        root_index = (self.root / "wiki/index.md").read_text()
        self.assertIn("| [ml](ml/index.md) | 1 | 2026-03-04 |", root_index)

    def test_index_groups_by_kind_including_preset_kinds(self) -> None:
        self.init("--preset", "engineering")
        self.write_page("ops/restart.md", title="Restart", kind="runbook")
        self.write_page("ops/db.md", title="DB", kind="entity")
        self.run_cli("index")
        index = (self.root / "wiki/ops/index.md").read_text()
        self.assertLess(index.index("## Entities"), index.index("## Runbooks"))
        report = self.run_cli("lint")
        self.assertEqual(report["errors"], [])


class IngestTests(WikiTestCase):
    def test_local_file_is_copied_never_moved(self) -> None:
        self.init()
        original = self.tmp / "notes.md"
        original.write_text("# Meeting\nWe chose Postgres.\n")
        data = self.run_cli(
            "ingest", str(original), "--domain", "team/db", "--title", "DB meeting"
        )
        self.assertTrue(original.is_file())
        self.assertEqual(data["raw"], ["raw/team/db/db-meeting.md"])
        self.assertEqual((self.root / data["raw"][0]).read_text(), original.read_text())
        page = (self.root / data["page"]).read_text()
        self.assertIn("kind: source", page)
        self.assertIn("domain: team/db", page)
        self.assertIn("sources: [raw/team/db/db-meeting.md]", page)
        self.assertGreater(data["placeholders"], 0)
        self.assertEqual(self.log_text().count("] ingest |"), 0)

    def test_collision_with_different_content_is_refused(self) -> None:
        self.init()
        first = self.tmp / "a" / "notes.md"
        second = self.tmp / "b" / "notes.md"
        first.parent.mkdir()
        second.parent.mkdir()
        first.write_text("one\n")
        second.write_text("two\n")
        self.run_cli("ingest", str(first), "--domain", "x")
        (self.root / "wiki/x/notes.md").unlink()
        data = self.run_cli("ingest", str(second), "--domain", "x", ok=False)
        self.assertEqual(data["error"]["code"], "name-collision")
        self.assertEqual((self.root / "raw/x/notes.md").read_text(), "one\n")

    def test_identical_content_is_reused(self) -> None:
        self.init()
        src = self.tmp / "notes.md"
        src.write_text("same\n")
        self.run_cli("ingest", str(src), "--domain", "x")
        (self.root / "wiki/x/notes.md").unlink()
        data = self.run_cli("ingest", str(src), "--domain", "x")
        self.assertEqual(data["reused"], ["raw/x/notes.md"])

    def test_existing_page_is_never_overwritten(self) -> None:
        self.init()
        src = self.tmp / "notes.md"
        src.write_text("same\n")
        self.run_cli("ingest", str(src), "--domain", "x")
        data = self.run_cli("ingest", str(src), "--domain", "x", ok=False)
        self.assertEqual(data["error"]["code"], "page-exists")

    def test_file_already_in_raw_is_used_in_place(self) -> None:
        self.init()
        raw_file = self.root / "raw/x/dropped.md"
        raw_file.parent.mkdir(parents=True, exist_ok=True)
        raw_file.write_text("dropped by user\n")
        data = self.run_cli("ingest", str(raw_file), "--domain", "x")
        self.assertEqual(data["raw"], [])
        self.assertEqual(data["sources"], ["raw/x/dropped.md"])

    def test_snapshot_saves_original_and_extracted_text(self) -> None:
        self.init()
        html = self.tmp / "post.html"
        html.write_text(
            "<html><head><title>Rate Limits Explained</title><script>x()</script></head>"
            "<body><h1>Limits</h1><p>Token bucket refills.</p></body></html>"
        )
        data = self.run_cli(
            "ingest", html.as_uri(), "--domain", "api/limits", "--snapshot"
        )
        self.assertEqual(data["title"], "Rate Limits Explained")
        self.assertEqual(
            data["raw"],
            [
                "raw/api/limits/rate-limits-explained.html",
                "raw/api/limits/rate-limits-explained.md",
            ],
        )
        self.assertEqual((self.root / data["raw"][0]).read_bytes(), html.read_bytes())
        extracted = (self.root / data["raw"][1]).read_text()
        self.assertIn("# Limits", extracted)
        self.assertNotIn("x()", extracted)
        page = (self.root / data["page"]).read_text()
        self.assertIn("source_url:", page)
        self.assertIn("retrieved:", page)

    def test_url_without_snapshot_records_url_only(self) -> None:
        self.init()
        data = self.run_cli(
            "ingest", "https://example.com/post", "--domain", "web", "--title", "Post"
        )
        self.assertEqual(data["raw"], [])
        self.assertEqual(data["sources"], ["https://example.com/post"])

    def test_snapshot_needs_url(self) -> None:
        self.init()
        src = self.tmp / "notes.md"
        src.write_text("x\n")
        data = self.run_cli("ingest", str(src), "--domain", "x", "--snapshot", ok=False)
        self.assertEqual(data["error"]["code"], "snapshot-needs-url")

    def test_asset_is_copied_into_raw_assets(self) -> None:
        self.init()
        src = self.tmp / "talk.md"
        src.write_text("talk\n")
        img = self.tmp / "Diagram 1.PNG"
        img.write_bytes(b"\x89PNG fake")
        data = self.run_cli("ingest", str(src), "--domain", "x", "--asset", str(img))
        self.assertEqual(data["assets"], ["raw/x/assets/talk/diagram-1.png"])
        self.assertTrue(img.is_file())
        self.assertIn(
            "![diagram-1](../../raw/x/assets/talk/diagram-1.png)",
            (self.root / data["page"]).read_text(),
        )

    def test_invalid_domain_is_refused(self) -> None:
        self.init()
        src = self.tmp / "n.md"
        src.write_text("x\n")
        data = self.run_cli("ingest", str(src), "--domain", "AWS/IAM", ok=False)
        self.assertEqual(data["error"]["code"], "domain-invalid")


class LintTests(WikiTestCase):
    def ingest_and_finish(self) -> str:
        src = self.tmp / "notes.md"
        src.write_text("notes\n")
        data = self.run_cli("ingest", str(src), "--domain", "x", "--title", "Notes")
        page = self.root / data["page"]
        text = page.read_text().replace(
            "TODO(llm-wiki): one plain sentence, 160 characters or fewer.", "Notes."
        )
        text = re.sub(r"(?m)^.*TODO\(llm-wiki\).*\n", "", text)
        page.write_text(text + "\nSee [concept](concept.md).\n")
        self.write_page(
            "x/concept.md", title="Concept", body="From [notes](notes.md).\n"
        )
        self.run_cli("index")
        return data["page"]

    def test_placeholder_fails_lint(self) -> None:
        self.init()
        src = self.tmp / "notes.md"
        src.write_text("notes\n")
        self.run_cli("ingest", str(src), "--domain", "x")
        report = self.run_cli("lint", ok=False)
        self.assertEqual(report["_exit"], 1)
        self.assertIn("placeholder", self.codes(report, "errors"))

    def test_placeholder_in_code_is_ignored(self) -> None:
        self.init()
        self.write_page(
            "x/a.md",
            body="Write `TODO(llm-wiki)` markers.\n\n```\nTODO(llm-wiki): x\n```\n",
        )
        self.run_cli("index")
        report = self.run_cli("lint")
        self.assertNotIn("placeholder", self.codes(report, "errors"))

    def test_missing_ingest_log_entry_warns_then_clears(self) -> None:
        self.init()
        page = self.ingest_and_finish()
        report = self.run_cli("lint")
        self.assertIn("ingest-log-missing", self.codes(report, "warnings"))
        self.run_cli("log", "ingest", "Notes", "--page", page)
        report = self.run_cli("lint", "--strict")
        self.assertEqual(report["warnings"], [])
        self.assertEqual(report["errors"], [])

    def test_links_outside_wiki_are_skipped(self) -> None:
        self.init()
        self.write_page(
            "x/a.md",
            body="[raw](../../raw/x/missing.md) [schema](../../AGENTS.md) [b](b.md) [ext](https://e.com)\n",
        )
        report = self.run_cli("lint", ok=False)
        broken = [e for e in report["errors"] if e["code"] == "link-broken"]
        self.assertEqual(
            [e["message"] for e in broken], ["Link target 'b.md' does not exist."]
        )

    def test_orphan_warning_ignores_index_links(self) -> None:
        self.init()
        self.write_page("x/a.md", title="A")
        self.write_page("x/hub.md", title="Hub", kind="overview")
        self.run_cli("index")
        report = self.run_cli("lint")
        orphans = [w["path"] for w in report["warnings"] if w["code"] == "orphan"]
        self.assertEqual(orphans, ["wiki/x/a.md"])

    def test_summary_rules(self) -> None:
        self.init()
        self.write_page("x/long.md", summary="y" * 161)
        self.write_page("x/none.md", summary='""')
        report = self.run_cli("lint", ok=False)
        errors = report["errors"]
        self.assertIn(
            ("summary-too-long", "wiki/x/long.md"),
            [(e["code"], e["path"]) for e in errors],
        )
        self.assertIn(
            ("field-missing", "wiki/x/none.md"),
            [(e["code"], e["path"]) for e in errors],
        )

    def test_kind_and_domain_checks(self) -> None:
        self.init()
        self.write_page("x/a.md", kind="runbook")
        self.write_page("x/b.md", domain="y")
        self.write_page("root-page.md", domain="x")
        codes = self.codes(self.run_cli("lint", ok=False), "errors")
        for code in ("kind-unknown", "domain-mismatch", "page-outside-domain"):
            self.assertIn(code, codes)

    def test_missing_raw_source_is_an_error(self) -> None:
        self.init()
        self.write_page("x/a.md", sources="[raw/x/gone.md]")
        self.assertIn(
            "source-missing", self.codes(self.run_cli("lint", ok=False), "errors")
        )

    def test_raw_file_without_reference_warns(self) -> None:
        self.init()
        stray = self.root / "raw/x/stray.pdf"
        stray.parent.mkdir(parents=True, exist_ok=True)
        stray.write_bytes(b"%PDF")
        report = self.run_cli("lint")
        self.assertIn("raw-unreferenced", self.codes(report, "warnings"))

    def test_malformed_log_heading_fails(self) -> None:
        self.init()
        with (self.root / "wiki/log.md").open("a") as fh:
            fh.write("\n## 2026-01-01 ingest Bad heading\n")
        self.assertIn(
            "log-heading-invalid", self.codes(self.run_cli("lint", ok=False), "errors")
        )

    def test_hand_edited_index_is_stale(self) -> None:
        self.init()
        (self.root / "wiki/index.md").write_text("# hand edit\n")
        self.assertIn("index-stale", self.codes(self.run_cli("lint"), "warnings"))


class LogAndSearchTests(WikiTestCase):
    def test_log_format_follow_ups_and_demotion(self) -> None:
        self.init()
        data = self.run_cli(
            "log",
            "lint",
            "Health check",
            "--body",
            "## Findings\n- two orphans",
            "--follow-up",
            "Question: who owns X?",
            "--follow-up",
            "Source: the 2025 report",
            "--at",
            "2026-02-03 04:05",
        )
        self.assertEqual(data["heading"], "## [2026-02-03 04:05] lint | Health check")
        text = self.log_text()
        self.assertIn("### Findings", text)
        self.assertIn(
            "### Follow-ups\n\n- Question: who owns X?\n- Source: the 2025 report", text
        )
        for line in text.splitlines():
            if line.startswith("## "):
                self.assertRegex(line, HEADING_RE)

    def test_log_is_append_only(self) -> None:
        self.init()
        before = self.log_text()
        self.run_cli("log", "query", "Q1")
        self.assertTrue(self.log_text().startswith(before.rstrip("\n")))

    def test_log_rejects_unknown_op(self) -> None:
        self.init()
        cmd = [
            sys.executable,
            str(SCRIPT),
            "log",
            "sync",
            "x",
            "--root",
            str(self.root),
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, env=self.env, check=False
        )
        self.assertNotEqual(result.returncode, 0)

    def test_log_body_from_stdin(self) -> None:
        self.init()
        self.run_cli("log", "query", "Q", "--body", "-", stdin="answer text\n")
        self.assertIn("answer text", self.log_text())

    def test_search_boosts_title_and_summary(self) -> None:
        self.init()
        self.write_page(
            "x/body.md",
            title="Other",
            summary="Unrelated.",
            body="kafka " * 3 + "filler " * 50,
        )
        self.write_page(
            "x/title.md",
            title="Kafka",
            summary="Kafka partitions.",
            body="filler " * 50,
        )
        data = self.run_cli("search", "kafka")
        self.assertEqual(
            [r["path"] for r in data["results"]], ["wiki/x/title.md", "wiki/x/body.md"]
        )
        self.assertEqual(
            set(data["results"][0]),
            {"path", "title", "kind", "domain", "summary", "score", "snippet"},
        )

    def test_search_filters(self) -> None:
        self.init()
        self.write_page("a/one.md", title="Kafka one")
        self.write_page("b/two.md", title="Kafka two", kind="entity")
        self.assertEqual(
            len(self.run_cli("search", "kafka", "--domain", "a")["results"]), 1
        )
        self.assertEqual(
            len(self.run_cli("search", "kafka", "--kind", "entity")["results"]), 1
        )

    def test_status_reports_counts(self) -> None:
        self.init()
        self.write_page("a/one.md")
        data = self.run_cli("status")
        self.assertEqual(data["counts"], {"a": {"concept": 1}})
        self.assertTrue(data["initialized"])
        self.assertEqual(len(data["recent_log"]), 1)


class GitTests(WikiTestCase):
    def bare(self, name: str = "remote.git") -> Path:
        path = self.tmp / name
        subprocess.run(
            ["git", "init", "--bare", "--quiet", str(path)], check=True, env=self.env
        )
        self.git(path, "symbolic-ref", "HEAD", "refs/heads/main")
        return path

    def test_setup_rejects_credentials_in_url(self) -> None:
        for url in (
            "https://user:token@github.com/me/wiki.git",
            "https://ghp_abc123@github.com/me/wiki.git",
            "https://github.com/me/wiki.git?access_token=x",
        ):
            data = self.run_cli("setup", "--remote", url, ok=False)
            self.assertEqual(data["error"]["code"], "credentials-in-url", url)
        self.assertFalse((self.home / ".config/llm-wiki/config.json").exists())

    def test_setup_initializes_repo_and_writes_config(self) -> None:
        remote = self.bare()
        data = self.run_cli("setup", "--remote", str(remote))
        self.assertTrue(data["git_initialized"])
        self.assertFalse(data["cloned"])
        self.assertTrue(any("private" in w for w in data["warnings"]))
        config = json.loads((self.home / ".config/llm-wiki/config.json").read_text())
        self.assertEqual(config["root"], str(self.root))
        self.assertEqual(
            self.git(self.root, "remote", "get-url", "origin"), str(remote)
        )

    def test_setup_unreachable_remote_fails(self) -> None:
        data = self.run_cli("setup", "--remote", str(self.tmp / "nope.git"), ok=False)
        self.assertEqual(data["error"]["code"], "remote-unreachable")

    def test_default_root_comes_from_config(self) -> None:
        remote = self.bare()
        self.run_cli("setup", "--remote", str(remote))
        cmd = [sys.executable, str(SCRIPT), "status", "--json"]
        result = subprocess.run(
            cmd, capture_output=True, text=True, env=self.env, check=True
        )
        self.assertEqual(json.loads(result.stdout)["root"], str(self.root))

    def test_sync_pushes_and_setup_clones(self) -> None:
        remote = self.bare()
        self.run_cli("setup", "--remote", str(remote))
        self.init()
        log_before = self.log_text()
        data = self.run_cli("sync", "-m", "first")
        self.assertTrue(data["committed"] and data["pushed"])
        self.assertEqual(self.log_text(), log_before)
        self.assertEqual(self.git(remote, "rev-parse", "main"), data["commit"])
        other = self.tmp / "clone"
        cloned = self.run_cli("setup", "--remote", str(remote), root=other)
        self.assertTrue(cloned["cloned"])
        self.assertTrue(cloned["wiki_exists"])

    def test_sync_conflict_aborts_rebase_and_keeps_local_commit(self) -> None:
        remote = self.bare()
        self.run_cli("setup", "--remote", str(remote))
        self.init()
        self.run_cli("sync", "-m", "base")
        other = self.tmp / "clone"
        self.run_cli("setup", "--remote", str(remote), root=other)
        (other / "AGENTS.md").write_text("remote edit\n")
        self.run_cli("sync", "-m", "remote", root=other)
        remote_head = self.git(remote, "rev-parse", "main")
        (self.root / "AGENTS.md").write_text("local edit\n")
        data = self.run_cli("sync", "-m", "local", ok=False)
        self.assertEqual(data["_exit"], 2)
        self.assertEqual(data["error"]["code"], "rebase-conflict")
        self.assertEqual(data["conflicts"], ["AGENTS.md"])
        self.assertFalse((self.root / ".git/rebase-merge").exists())
        self.assertFalse((self.root / ".git/rebase-apply").exists())
        self.assertEqual(self.git(self.root, "rev-parse", "HEAD"), data["commit"])
        self.assertEqual(self.git(self.root, "log", "-1", "--format=%s"), "local")
        self.assertEqual((self.root / "AGENTS.md").read_text(), "local edit\n")
        self.assertEqual(self.git(remote, "rev-parse", "main"), remote_head)

    def test_sync_rebases_non_conflicting_changes(self) -> None:
        remote = self.bare()
        self.run_cli("setup", "--remote", str(remote))
        self.init()
        self.run_cli("sync")
        other = self.tmp / "clone"
        self.run_cli("setup", "--remote", str(remote), root=other)
        (other / "remote.txt").write_text("r\n")
        self.run_cli("sync", root=other)
        (self.root / "local.txt").write_text("l\n")
        data = self.run_cli("sync")
        self.assertTrue(data["pulled"] and data["pushed"])
        self.assertTrue((self.root / "remote.txt").is_file())

    def test_sync_never_force_pushes(self) -> None:
        source = SCRIPT.read_text()
        self.assertNotIn("--force", source)
        self.assertNotIn('"-f"', source)


class JsonContractTests(WikiTestCase):
    def test_every_command_supports_json(self) -> None:
        help_text = subprocess.run(
            [sys.executable, str(SCRIPT), "--help"],
            capture_output=True,
            text=True,
            env=self.env,
            check=True,
        ).stdout
        commands = re.search(r"\{([a-z,]+)\}", help_text)
        assert commands is not None
        for command in commands.group(1).split(","):
            result = subprocess.run(
                [sys.executable, str(SCRIPT), command, "--help"],
                capture_output=True,
                text=True,
                env=self.env,
                check=True,
            )
            self.assertIn("--json", result.stdout, command)

    def test_errors_are_json(self) -> None:
        data = self.run_cli("lint", ok=False)
        self.assertEqual(data["error"]["code"], "not-initialized")
        self.assertFalse(data["ok"])


class SlugAndFlagTests(WikiTestCase):
    def test_descriptive_url_path_wins_over_long_title(self) -> None:
        self.init()
        html = self.tmp / "permission-boundaries-explained.html"
        html.write_text(
            "<html><head><title>Permission Boundaries Explained: What They Cap and What They Do Not</title></head></html>"
        )
        data = self.run_cli(
            "ingest", html.as_uri(), "--domain", "aws/iam", "--snapshot"
        )
        self.assertEqual(
            data["page"], "wiki/aws/iam/permission-boundaries-explained.md"
        )

    def test_long_slugs_are_cut_at_a_word_boundary(self) -> None:
        self.init()
        src = self.tmp / "n.md"
        src.write_text("x\n")
        title = "A very long meeting title about the quarterly payments architecture review and more"
        data = self.run_cli("ingest", str(src), "--domain", "x", "--title", title)
        slug = data["page"].removeprefix("wiki/x/").removesuffix(".md")
        self.assertLessEqual(len(slug), 60)
        self.assertTrue(title.lower().replace(" ", "-").startswith(slug))

    def test_global_flags_work_before_the_command(self) -> None:
        self.init()
        cmd = [
            sys.executable,
            str(SCRIPT),
            "--root",
            str(self.root),
            "--json",
            "status",
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, env=self.env, check=True
        )
        self.assertEqual(json.loads(result.stdout)["root"], str(self.root))


if __name__ == "__main__":
    unittest.main()
