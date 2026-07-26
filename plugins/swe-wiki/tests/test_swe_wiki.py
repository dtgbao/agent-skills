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

        self.cli("init", "--root", root, environment=environment)
        self.cli("init", "--root", root, environment=environment)
        self.cli(
            "ingest",
            "https://example.com/cache",
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
        self.assertIn("wiki/sources/", query.stdout)
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
        self.assertIn("# SWE Wiki Index", remote_index)

    def test_sync_commits_pushes_pulls_and_does_not_commit_noop(self):
        first_environment = self.machine_environment("first")
        second_environment = self.machine_environment("second")
        remote = self.bare_remote()
        first_root = self.base / "first-wiki"
        second_root = self.base / "second-wiki"
        self.setup_wiki(first_root, remote, first_environment)
        self.setup_wiki(second_root, remote, second_environment)

        page = first_root / "wiki" / "practices" / "sync-test.md"
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
                second_root / "wiki" / "practices" / "sync-test.md"
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

        first_page = first_root / "wiki" / "practices" / "shared.md"
        first_page.write_text("baseline\n", encoding="utf-8")
        self.cli("sync", environment=first_environment)
        self.cli("sync", environment=second_environment)

        first_page.write_text("remote change\n", encoding="utf-8")
        self.cli("sync", environment=first_environment)
        second_page = second_root / "wiki" / "practices" / "shared.md"
        second_page.write_text("local change\n", encoding="utf-8")

        result = self.cli("sync", environment=second_environment, check=False)

        self.assertEqual(1, result.returncode)
        self.assertIn(
            "Conflicting files: wiki/practices/shared.md.",
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
