import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PLUGIN_ROOT / "skills" / "swe-wiki" / "scripts" / "swe_wiki.py"


class SweWikiCliTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary_directory.name)

    def tearDown(self):
        self.temporary_directory.cleanup()

    def machine_environment(self, name):
        home = self.base / f"{name}-home"
        home.mkdir()
        environment = os.environ.copy()
        environment["HOME"] = str(home)
        environment["GIT_CONFIG_NOSYSTEM"] = "1"
        self.git(
            "config",
            "--global",
            "user.name",
            f"{name} user",
            environment=environment,
        )
        self.git(
            "config",
            "--global",
            "user.email",
            f"{name}@example.com",
            environment=environment,
        )
        return environment

    def git(self, *arguments, cwd=None, environment=None, check=True):
        result = subprocess.run(
            ["git", *arguments],
            cwd=cwd,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        if check and result.returncode != 0:
            self.fail(
                f"git {' '.join(arguments)} failed\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )
        return result

    def cli(self, *arguments, environment, check=True):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, arguments)],
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        if check and result.returncode != 0:
            self.fail(
                f"swe_wiki.py {' '.join(map(str, arguments))} failed\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )
        return result

    def bare_remote(self, name="remote.git"):
        remote = self.base / name
        self.git("init", "--bare", "--initial-branch=main", str(remote))
        return remote

    def setup_wiki(self, root, remote, environment, check=True):
        return self.cli(
            "setup",
            "--root",
            root,
            "--repo",
            remote,
            environment=environment,
            check=check,
        )

    def seed_remote_with_readme(self, remote, environment):
        seed = self.base / "seed"
        self.git("init", "-b", "main", str(seed), environment=environment)
        (seed / "README.md").write_text("# Existing repository\n", encoding="utf-8")
        self.git("add", "README.md", cwd=seed, environment=environment)
        self.git(
            "commit",
            "-m",
            "seed repository",
            cwd=seed,
            environment=environment,
        )
        self.git(
            "remote",
            "add",
            "origin",
            str(remote),
            cwd=seed,
            environment=environment,
        )
        self.git(
            "push",
            "-u",
            "origin",
            "main",
            cwd=seed,
            environment=environment,
        )

    def test_setup_initializes_empty_remote_and_saves_config(self):
        environment = self.machine_environment("first")
        remote = self.bare_remote()
        root = self.base / "wiki"

        result = self.setup_wiki(root, remote, environment)

        self.assertIn("committed and synced", result.stdout)
        self.assertTrue((root / ".git").exists())
        self.assertTrue((root / "wiki" / "index.md").exists())
        self.assertTrue((root / "wiki" / "log.md").exists())
        config = json.loads(
            (
                Path(environment["HOME"])
                / ".config"
                / "swe-wiki"
                / "config.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual({"version": 1, "root": str(root.resolve())}, config)
        remote_subject = self.git(
            "--git-dir",
            str(remote),
            "log",
            "-1",
            "--format=%s",
        ).stdout.strip()
        self.assertTrue(remote_subject.startswith("swe-wiki setup:"))

    def test_local_workflows_use_new_root_interface_and_init_is_idempotent(self):
        environment = self.machine_environment("local")
        root = self.base / "local-wiki"
        source = self.base / "cache.txt"
        asset = self.base / "cache-diagram.png"
        source.write_text("Cache source\n", encoding="utf-8")
        asset.write_bytes(b"diagram")

        self.cli("init", "--root", root, environment=environment)
        self.cli("init", "--root", root, environment=environment)
        self.cli(
            "ingest",
            source,
            "--domain",
            "backend/caching",
            "--asset",
            asset,
            "--title",
            "Cache Strategies",
            "--root",
            root,
            environment=environment,
        )
        self.cli(
            "log",
            "ingest",
            "Cache Strategies",
            "--root",
            root,
            environment=environment,
        )
        query = self.cli(
            "query",
            "cache strategies",
            "--root",
            root,
            environment=environment,
        )
        lint = self.cli("lint", "--root", root, environment=environment)

        log = (root / "wiki" / "log.md").read_text(encoding="utf-8")
        self.assertEqual(1, log.count("bootstrap | SWE wiki initialized"))
        self.assertIn("wiki/backend/caching/sources/", query.stdout)
        self.assertTrue((root / "raw" / "backend" / "caching" / "cache.txt").exists())
        self.assertTrue(
            (root / "raw" / "backend" / "caching" / "cache-diagram.png").exists()
        )
        self.assertTrue((root / "wiki" / "backend" / "index.md").exists())
        self.assertTrue((root / "wiki" / "backend" / "caching" / "index.md").exists())
        self.assertTrue(
            (root / "wiki" / "backend" / "caching" / "sources" / "index.md").exists()
        )
        self.assertFalse((root / "wiki" / "concepts").exists())
        root_index = (root / "wiki" / "index.md").read_text(encoding="utf-8")
        self.assertIn("backend/index.md", root_index)
        self.assertNotIn("cache-strategies.md", root_index)
        self.assertEqual("OK\n", lint.stdout)

    def test_setup_clones_nonempty_remote_and_preserves_existing_files(self):
        seed_environment = self.machine_environment("seed")
        remote = self.bare_remote()
        self.seed_remote_with_readme(remote, seed_environment)
        environment = self.machine_environment("clone")
        root = self.base / "cloned-wiki"

        self.setup_wiki(root, remote, environment)

        self.assertEqual(
            "# Existing repository\n",
            (root / "README.md").read_text(encoding="utf-8"),
        )
        self.assertTrue((root / "wiki" / "index.md").exists())
        remote_index = self.git(
            "--git-dir",
            str(remote),
            "show",
            "main:wiki/index.md",
        ).stdout
        self.assertIn("# SWE Wiki", remote_index)

    def test_sync_commits_pushes_pulls_and_does_not_commit_noop(self):
        first_environment = self.machine_environment("first")
        second_environment = self.machine_environment("second")
        remote = self.bare_remote()
        first_root = self.base / "first-wiki"
        second_root = self.base / "second-wiki"
        self.setup_wiki(first_root, remote, first_environment)
        self.setup_wiki(second_root, remote, second_environment)

        page = first_root / "wiki" / "testing" / "sync-test.md"
        page.parent.mkdir(parents=True)
        page.write_text("# Synced from the first computer\n", encoding="utf-8")
        self.cli("sync", environment=first_environment)
        count_after_push = int(
            self.git(
                "--git-dir",
                str(remote),
                "rev-list",
                "--count",
                "main",
            ).stdout
        )

        self.cli("sync", environment=second_environment)
        self.assertEqual(
            "# Synced from the first computer\n",
            (
                second_root / "wiki" / "testing" / "sync-test.md"
            ).read_text(encoding="utf-8"),
        )
        self.cli("sync", environment=second_environment)
        count_after_noop = int(
            self.git(
                "--git-dir",
                str(remote),
                "rev-list",
                "--count",
                "main",
            ).stdout
        )
        self.assertEqual(count_after_push, count_after_noop)

    def test_sync_aborts_conflict_and_preserves_local_commit(self):
        first_environment = self.machine_environment("first")
        second_environment = self.machine_environment("second")
        remote = self.bare_remote()
        first_root = self.base / "first-wiki"
        second_root = self.base / "second-wiki"
        self.setup_wiki(first_root, remote, first_environment)
        self.setup_wiki(second_root, remote, second_environment)

        first_page = first_root / "wiki" / "testing" / "shared.md"
        first_page.parent.mkdir(parents=True)
        first_page.write_text("baseline\n", encoding="utf-8")
        self.cli("sync", environment=first_environment)
        self.cli("sync", environment=second_environment)

        first_page.write_text("remote change\n", encoding="utf-8")
        self.cli("sync", environment=first_environment)
        second_page = second_root / "wiki" / "testing" / "shared.md"
        second_page.write_text("local change\n", encoding="utf-8")

        result = self.cli("sync", environment=second_environment, check=False)

        self.assertEqual(1, result.returncode)
        self.assertIn(
            "Conflicting files: wiki/testing/shared.md.",
            result.stderr,
        )
        self.assertEqual("local change\n", second_page.read_text(encoding="utf-8"))
        self.assertEqual(
            "",
            self.git(
                "status",
                "--porcelain",
                cwd=second_root,
                environment=second_environment,
            ).stdout,
        )
        self.assertFalse((second_root / ".git" / "rebase-merge").exists())
        local_subject = self.git(
            "log",
            "-1",
            "--format=%s",
            cwd=second_root,
            environment=second_environment,
        ).stdout.strip()
        self.assertTrue(local_subject.startswith("swe-wiki sync:"))

    def test_ingest_validates_domains_and_refuses_raw_collisions(self):
        environment = self.machine_environment("domains")
        root = self.base / "wiki"
        first = self.base / "first" / "lesson.txt"
        second = self.base / "second" / "lesson.txt"
        first.parent.mkdir()
        second.parent.mkdir()
        first.write_text("first\n", encoding="utf-8")
        second.write_text("second\n", encoding="utf-8")
        self.cli("init", "--root", root, environment=environment)

        invalid = self.cli(
            "ingest",
            first,
            "--domain",
            "AWS/IAM",
            "--root",
            root,
            environment=environment,
            check=False,
        )
        self.assertEqual(1, invalid.returncode)
        self.assertIn("invalid domain", invalid.stderr)

        self.cli(
            "ingest",
            first,
            "--domain",
            "aws/iam",
            "--title",
            "First lesson",
            "--root",
            root,
            environment=environment,
        )
        collision = self.cli(
            "ingest",
            second,
            "--domain",
            "aws/iam",
            "--title",
            "Second lesson",
            "--root",
            root,
            environment=environment,
            check=False,
        )
        self.assertEqual(1, collision.returncode)
        self.assertIn("raw file collision", collision.stderr)
        self.assertEqual(
            "first\n",
            (root / "raw" / "aws" / "iam" / "lesson.txt").read_text(
                encoding="utf-8"
            ),
        )
        self.assertEqual(
            [],
            list((root / "wiki" / "aws" / "iam" / "sources").glob("*second-lesson.md")),
        )

    def test_migration_preview_is_read_only_and_apply_rewrites_links(self):
        environment = self.machine_environment("migration")
        root = self.base / "wiki"
        self.cli("init", "--root", root, environment=environment)
        raw = root / "raw" / "iam-lesson.txt"
        raw.write_text("IAM lesson\n", encoding="utf-8")
        sources = root / "wiki" / "sources"
        systems = root / "wiki" / "systems"
        sources.mkdir()
        systems.mkdir()
        source_page = sources / "iam-lesson.md"
        source_page.write_text(
            """---
title: "IAM lesson"
kind: source
status: draft
tags: [swe, aws, iam]
sources: ["../../raw/iam-lesson.txt"]
updated: 2026-08-05
confidence: medium
---

# IAM lesson

Lesson summary.

- [IAM system](../systems/iam.md)
- ![Raw transcript](../../raw/iam-lesson.txt)
""",
            encoding="utf-8",
        )
        system_page = systems / "iam.md"
        system_page.write_text(
            """---
title: "IAM"
kind: system
status: draft
tags: [swe, aws, iam]
sources: ["../sources/iam-lesson.md"]
updated: 2026-08-05
confidence: medium
---

# IAM

Identity and access management.

- [Source](../sources/iam-lesson.md)
""",
            encoding="utf-8",
        )
        manifest = self.base / "migration.json"
        manifest.write_text(
            json.dumps(
                {
                    "assignments": [
                        {
                            "domain": "aws/iam",
                            "paths": [
                                "raw/iam-lesson.txt",
                                "wiki/sources/iam-lesson.md",
                                "wiki/systems/iam.md",
                            ],
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        original_source = source_page.read_text(encoding="utf-8")

        preview = self.cli(
            "migrate",
            manifest,
            "--root",
            root,
            environment=environment,
        )
        self.assertIn("Migration plan", preview.stdout)
        self.assertIn("wiki/aws/iam/sources/iam-lesson.md", preview.stdout)
        self.assertEqual(original_source, source_page.read_text(encoding="utf-8"))
        self.assertFalse((root / "wiki" / "aws").exists())

        self.cli(
            "migrate",
            manifest,
            "--apply",
            "--root",
            root,
            environment=environment,
        )

        migrated_source = root / "wiki" / "aws" / "iam" / "sources" / "iam-lesson.md"
        migrated_system = root / "wiki" / "aws" / "iam" / "iam.md"
        migrated_raw = root / "raw" / "aws" / "iam" / "iam-lesson.txt"
        self.assertTrue(migrated_source.exists())
        self.assertTrue(migrated_system.exists())
        self.assertTrue(migrated_raw.exists())
        self.assertFalse(source_page.exists())
        self.assertFalse(system_page.exists())
        self.assertFalse(sources.exists())
        self.assertFalse(systems.exists())
        self.assertIn(
            "[AWS](aws/index.md)",
            (root / "wiki" / "index.md").read_text(encoding="utf-8"),
        )
        self.assertIn(
            "# IAM",
            (root / "wiki" / "aws" / "iam" / "index.md").read_text(
                encoding="utf-8"
            ),
        )
        source_text = migrated_source.read_text(encoding="utf-8")
        system_text = migrated_system.read_text(encoding="utf-8")
        self.assertIn("domain: aws/iam", source_text)
        self.assertIn("../../../../raw/aws/iam/iam-lesson.txt", source_text)
        self.assertIn("../iam.md", source_text)
        self.assertIn("sources: [\"sources/iam-lesson.md\"]", system_text)
        self.assertIn("(sources/iam-lesson.md)", system_text)
        self.assertIn(
            "migrate | Domain-first wiki layout",
            (root / "wiki" / "log.md").read_text(encoding="utf-8"),
        )
        lint = self.cli("lint", "--root", root, environment=environment)
        self.assertEqual("OK\n", lint.stdout)

    def test_migration_requires_complete_collision_free_manifest(self):
        environment = self.machine_environment("migration-errors")
        root = self.base / "wiki"
        self.cli("init", "--root", root, environment=environment)
        legacy = root / "wiki" / "systems"
        legacy.mkdir()
        page = legacy / "service.md"
        page.write_text(
            """---
title: "Service"
kind: system
status: draft
tags: [swe]
sources: []
updated: 2026-08-05
confidence: medium
---

# Service

Service summary.
""",
            encoding="utf-8",
        )
        incomplete = self.base / "incomplete.json"
        incomplete.write_text(
            json.dumps(
                {
                    "assignments": [
                        {"domain": "backend", "paths": ["wiki/log.md"]}
                    ]
                }
            ),
            encoding="utf-8",
        )
        result = self.cli(
            "migrate",
            incomplete,
            "--root",
            root,
            environment=environment,
            check=False,
        )
        self.assertEqual(1, result.returncode)
        self.assertTrue(page.exists())

        target = root / "wiki" / "backend" / "service.md"
        target.parent.mkdir(parents=True)
        target.write_text("occupied\n", encoding="utf-8")
        collision = self.base / "collision.json"
        collision.write_text(
            json.dumps(
                {
                    "assignments": [
                        {"domain": "backend", "paths": ["wiki/systems/service.md"]}
                    ]
                }
            ),
            encoding="utf-8",
        )
        result = self.cli(
            "migrate",
            collision,
            "--root",
            root,
            environment=environment,
            check=False,
        )
        self.assertEqual(1, result.returncode)
        self.assertIn("target already exists", result.stderr)
        self.assertTrue(page.exists())

    def test_migration_apply_refuses_dirty_git_worktree(self):
        environment = self.machine_environment("dirty-migration")
        root = self.base / "wiki"
        self.cli("init", "--root", root, environment=environment)
        legacy = root / "wiki" / "systems"
        legacy.mkdir()
        page = legacy / "service.md"
        page.write_text(
            """---
title: "Service"
kind: system
status: draft
tags: [swe]
sources: []
updated: 2026-08-05
confidence: medium
---

# Service

Service summary.
""",
            encoding="utf-8",
        )
        self.git("init", "-b", "main", str(root), environment=environment)
        self.git("add", "--all", cwd=root, environment=environment)
        self.git("commit", "-m", "legacy wiki", cwd=root, environment=environment)
        (root / "README.md").write_text("dirty\n", encoding="utf-8")
        manifest = self.base / "dirty-migration.json"
        manifest.write_text(
            json.dumps(
                {
                    "assignments": [
                        {"domain": "backend", "paths": ["wiki/systems/service.md"]}
                    ]
                }
            ),
            encoding="utf-8",
        )

        result = self.cli(
            "migrate",
            manifest,
            "--apply",
            "--root",
            root,
            environment=environment,
            check=False,
        )

        self.assertEqual(1, result.returncode)
        self.assertIn("clean Git worktree", result.stderr)
        self.assertTrue(page.exists())
        self.assertFalse((root / "wiki" / "backend").exists())

    def test_setup_refuses_ambiguous_directory(self):
        environment = self.machine_environment("ambiguous")
        remote = self.bare_remote()
        root = self.base / "occupied"
        root.mkdir()
        marker = root / "keep.txt"
        marker.write_text("keep\n", encoding="utf-8")

        result = self.setup_wiki(root, remote, environment, check=False)

        self.assertNotEqual(0, result.returncode)
        self.assertIn("is not a Git repository", result.stderr)
        self.assertEqual("keep\n", marker.read_text(encoding="utf-8"))
        self.assertFalse((root / ".git").exists())

    def test_setup_rejects_embedded_credentials_before_network_access(self):
        environment = self.machine_environment("credentials")
        root = self.base / "wiki"

        result = self.cli(
            "setup",
            "--root",
            root,
            "--repo",
            "https://user:secret@github.com/example/wiki.git",
            environment=environment,
            check=False,
        )

        self.assertEqual(1, result.returncode)
        self.assertIn("must not contain embedded credentials", result.stderr)
        self.assertFalse(root.exists())

    def test_commands_fail_clearly_before_setup(self):
        environment = self.machine_environment("unconfigured")

        result = self.cli(
            "query",
            "cache invalidation",
            environment=environment,
            check=False,
        )

        self.assertEqual(1, result.returncode)
        self.assertIn("run `setup`", result.stderr)


if __name__ == "__main__":
    unittest.main()
