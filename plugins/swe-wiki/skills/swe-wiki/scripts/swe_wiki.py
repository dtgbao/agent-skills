#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

CONFIG_VERSION = 1
KINDS = {
    "sources": "source",
    "concepts": "concept",
    "decisions": "decision",
    "blueprints": "blueprint",
    "practices": "practice",
    "conventions": "convention",
    "systems": "system",
    "questions": "question",
}
LOG_RE = re.compile(
    r"^## \[\d{4}-\d{2}-\d{2}(?: \d{2}:\d{2})?\] "
    r"(bootstrap|ingest|query|lint) \| .+"
)
GITIGNORE = """.DS_Store
__pycache__/
*.pyc
"""


class SweWikiError(RuntimeError):
    pass


def slug(text):
    text = re.sub(r"https?://", "", text.lower())
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:80] or "untitled"


def today():
    return dt.date.today().isoformat()


def now():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def root_path(value):
    return Path(value).expanduser().resolve()


def default_root():
    return Path.home() / ".swe-wiki"


def config_path():
    return Path.home() / ".config" / "swe-wiki" / "config.json"


def load_config():
    path = config_path()
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SweWikiError(f"cannot read config {path}: {error}") from error
    if (
        not isinstance(payload, dict)
        or payload.get("version") != CONFIG_VERSION
        or not isinstance(payload.get("root"), str)
        or not payload["root"].strip()
    ):
        raise SweWikiError(f"invalid config schema in {path}; run setup again")
    return payload


def save_config(root):
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"version": CONFIG_VERSION, "root": str(root)}
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)
    return path


def resolve_root(explicit=None):
    if explicit:
        return root_path(explicit)
    config = load_config()
    if config:
        return root_path(config["root"])
    return default_root().resolve()


def wiki(root):
    return root / "wiki"


def rel(path, root):
    return path.resolve().relative_to(root.resolve()).as_posix()


def ensure_dirs(root):
    created = []
    directories = [root / "raw", wiki(root)]
    directories.extend(wiki(root) / directory for directory in KINDS)
    for directory in directories:
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            created.append(f"{rel(directory, root)}/")
    return created


def write_once(path, text):
    if path.exists():
        return False
    path.write_text(text, encoding="utf-8")
    return True


def write_if_changed(path, text):
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def page_files(root):
    base = wiki(root)
    if not base.exists():
        return []
    return sorted(
        path
        for path in base.rglob("*.md")
        if path.name not in {"index.md", "log.md"} and "_templates" not in path.parts
    )


def title_from_path(path):
    return path.stem.replace("-", " ").title()


def frontmatter(text):
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    data = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
    return data


def markdown_links(text):
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+\.md)(?:#[^)]+)?\)", text):
        target = match.group(1)
        if not re.match(r"[a-z]+://", target):
            yield target


def index_links(root):
    path = wiki(root) / "index.md"
    if not path.exists():
        return set()
    return set(markdown_links(path.read_text(encoding="utf-8")))


def source_count(meta):
    value = meta.get("sources", "")
    if value in {"", "[]"}:
        return 0
    return max(1, value.count(",") + 1)


def index_row(root, path):
    text = path.read_text(encoding="utf-8")
    meta = frontmatter(text)
    title = meta.get("title") or title_from_path(path)
    tags = meta.get("tags", "[]").strip("[]") or "swe"
    updated = meta.get("updated") or today()
    summary = ""
    for line in text.splitlines():
        if line and not line.startswith(("#", "---")) and ":" not in line[:20]:
            summary = line.strip()
            break
    summary = summary or f"{title}."
    return (
        f"- [{title}]({rel(path, wiki(root))}) - {summary} "
        f"| tags: {tags} | updated: {updated} | sources: {source_count(meta)}"
    )


def rebuild_index(root):
    sections = {kind: [] for kind in KINDS.values()}
    for path in page_files(root):
        meta = frontmatter(path.read_text(encoding="utf-8"))
        kind = meta.get("kind") or KINDS.get(path.parent.name, "concept")
        sections.setdefault(kind, []).append(index_row(root, path))

    lines = [
        "# SWE Wiki Index",
        "",
        "Content catalog. Read this before querying pages.",
        "",
    ]
    for kind in [
        "source",
        "concept",
        "decision",
        "blueprint",
        "practice",
        "convention",
        "system",
        "question",
    ]:
        lines += [f"## {kind.title()}s", ""]
        lines += sorted(sections.get(kind, [])) or ["_None yet._"]
        lines.append("")
    content = "\n".join(lines).rstrip() + "\n"
    return write_if_changed(wiki(root) / "index.md", content)


def append_log(root, kind, title, changed=None, notes=None, followups=None):
    path = wiki(root) / "log.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"## [{now()}] {kind} | {title}"]
    if changed:
        lines.append(f"- Changed: {', '.join(changed)}")
    if notes:
        lines.append(f"- Notes: {notes}")
    if followups:
        lines.append(f"- Follow-ups: {followups}")
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n" + "\n".join(lines) + "\n")


def initialize_wiki(root):
    root.mkdir(parents=True, exist_ok=True)
    changed = ensure_dirs(root)
    if write_once(root / ".gitignore", GITIGNORE):
        changed.append(".gitignore")
    if write_once(
        root / "AGENTS.md",
        """# SWE Wiki Schema

Use `$swe-wiki` to ingest sources, query accumulated knowledge, lint this wiki, and sync it.

- Keep `raw/` immutable.
- Maintain `wiki/index.md` on every ingest or durable query.
- Keep `wiki/log.md` append-only with headings like `## [YYYY-MM-DD HH:MM] ingest | Title`.
- Put durable software engineering knowledge in the page kind that owns it.
""",
    ):
        changed.append("AGENTS.md")
    if write_once(wiki(root) / "log.md", "# SWE Wiki Log\n\n"):
        changed.append("wiki/log.md")
    if rebuild_index(root):
        changed.append("wiki/index.md")
    if changed:
        append_log(root, "bootstrap", "SWE wiki initialized", changed=changed)
    return changed


def required_wiki_paths(root):
    paths = [
        root / "raw",
        wiki(root),
        wiki(root) / "index.md",
        wiki(root) / "log.md",
    ]
    paths.extend(wiki(root) / directory for directory in KINDS)
    return paths


def require_initialized(root):
    if not all(path.exists() for path in required_wiki_paths(root)):
        raise SweWikiError(
            f"{root} is not initialized; run `setup` or `init --root {root}` first"
        )


def run_git(arguments, cwd=None, check=True):
    environment = None
    if not sys.stdin.isatty():
        environment = os.environ.copy()
        environment["GIT_TERMINAL_PROMPT"] = "0"
    try:
        result = subprocess.run(
            ["git", *arguments],
            cwd=cwd,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as error:
        raise SweWikiError("git is required but was not found on PATH") from error
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown git error"
        raise SweWikiError(f"git {' '.join(arguments)} failed: {detail}")
    return result


def validate_repository(repository):
    if not isinstance(repository, str):
        raise SweWikiError("a Git repository URL is required")
    repository = repository.strip()
    if not repository:
        raise SweWikiError("a Git repository URL is required")
    if any(character in repository for character in "\r\n\0"):
        raise SweWikiError("repository URL contains invalid characters")
    parsed = urlsplit(repository)
    if parsed.password is not None or (
        parsed.scheme.lower() in {"http", "https"} and parsed.username is not None
    ):
        raise SweWikiError(
            "repository URLs must not contain embedded credentials; "
            "use SSH or a credential manager"
        )
    return repository


def inspect_remote(repository):
    result = run_git(["ls-remote", repository], check=False)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown git error"
        raise SweWikiError(f"cannot reach Git repository {repository}: {detail}")
    return bool(result.stdout.strip())


def git_repository_root(root):
    result = run_git(["rev-parse", "--show-toplevel"], cwd=root)
    return root_path(result.stdout.strip())


def require_git_repository(root):
    if not (root / ".git").exists():
        raise SweWikiError(f"{root} is not a Git repository; run setup first")
    top_level = git_repository_root(root)
    if top_level != root.resolve():
        raise SweWikiError(f"{root} is not the Git repository root")
    result = run_git(["remote", "get-url", "origin"], cwd=root, check=False)
    if result.returncode != 0 or not result.stdout.strip():
        raise SweWikiError(f"{root} has no origin remote; run setup first")
    return validate_repository(result.stdout.strip())


def validate_existing_checkout(root, repository):
    origin = require_git_repository(root)
    if origin != repository:
        raise SweWikiError(
            f"{root} uses origin {origin}, which does not match {repository}; "
            "choose another directory or repository"
        )


def prepare_checkout(root, repository, remote_has_refs):
    if root.exists() and not root.is_dir():
        raise SweWikiError(f"{root} exists and is not a directory")
    if root.exists() and any(root.iterdir()):
        validate_existing_checkout(root, repository)
        return

    root.parent.mkdir(parents=True, exist_ok=True)
    if remote_has_refs:
        run_git(["clone", repository, str(root)])
        return

    root.mkdir(parents=True, exist_ok=True)
    run_git(["init", "-b", "main"], cwd=root)
    run_git(["remote", "add", "origin", repository], cwd=root)


def require_git_identity(root):
    missing = []
    for key in ["user.name", "user.email"]:
        result = run_git(["config", "--get", key], cwd=root, check=False)
        if result.returncode != 0 or not result.stdout.strip():
            missing.append(key)
    if missing:
        raise SweWikiError(
            "Git identity is not configured. Set it before syncing, for example: "
            '`git config --global user.name "Your Name"` and '
            '`git config --global user.email "you@example.com"`'
        )


def has_staged_changes(root):
    result = run_git(["diff", "--cached", "--quiet"], cwd=root, check=False)
    if result.returncode not in {0, 1}:
        detail = result.stderr.strip() or "cannot inspect staged changes"
        raise SweWikiError(detail)
    return result.returncode == 1


def current_branch(root):
    result = run_git(["branch", "--show-current"], cwd=root)
    branch = result.stdout.strip()
    if not branch:
        raise SweWikiError("cannot sync a detached HEAD; check out a branch first")
    return branch


def rebase_onto_remote(root, branch):
    remote_ref = f"refs/remotes/origin/{branch}"
    exists = run_git(
        ["show-ref", "--verify", "--quiet", remote_ref], cwd=root, check=False
    )
    if exists.returncode == 1:
        return
    if exists.returncode != 0:
        raise SweWikiError(f"cannot inspect remote branch origin/{branch}")

    result = run_git(["rebase", f"origin/{branch}"], cwd=root, check=False)
    if result.returncode == 0:
        return

    conflicts = run_git(
        ["diff", "--name-only", "--diff-filter=U"], cwd=root, check=False
    ).stdout.splitlines()
    run_git(["rebase", "--abort"], cwd=root, check=False)
    detail = result.stderr.strip() or result.stdout.strip() or "rebase failed"
    conflict_text = f" Conflicting files: {', '.join(conflicts)}." if conflicts else ""
    raise SweWikiError(
        "sync stopped because remote changes could not be rebased. "
        f"The local commit was preserved.{conflict_text} Git said: {detail}"
    )


def sync_repository(root, message=None):
    require_git_repository(root)
    run_git(["add", "--all"], cwd=root)
    committed = False
    if has_staged_changes(root):
        require_git_identity(root)
        run_git(
            ["commit", "-m", message or f"swe-wiki sync: {now()}"],
            cwd=root,
        )
        committed = True

    branch = current_branch(root)
    run_git(["fetch", "origin"], cwd=root)
    rebase_onto_remote(root, branch)
    result = run_git(
        ["push", "--set-upstream", "origin", branch], cwd=root, check=False
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "push failed"
        raise SweWikiError(
            f"push was rejected without force; rerun sync after reviewing: {detail}"
        )
    return committed, branch


def prompt_value(prompt, default=None):
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value or default


def setup_root(explicit):
    if explicit:
        return root_path(explicit)
    config = load_config()
    default = root_path(config["root"]) if config else default_root().resolve()
    if sys.stdin.isatty():
        return root_path(prompt_value("Wiki directory", str(default)))
    return default


def setup_repository(explicit):
    if explicit:
        return validate_repository(explicit)
    if not sys.stdin.isatty():
        raise SweWikiError("--repo is required when setup is non-interactive")
    return validate_repository(prompt_value("Git repository URL"))


def cmd_setup(args):
    root = setup_root(args.root)
    repository = setup_repository(args.repo)
    remote_has_refs = inspect_remote(repository)
    prepare_checkout(root, repository, remote_has_refs)
    initialize_wiki(root)
    committed, branch = sync_repository(root, message=f"swe-wiki setup: {now()}")
    path = save_config(root)
    action = "committed and synced" if committed else "synced"
    print(f"{action} {root} on {branch}")
    print(f"saved config {path}")
    print("Use a private remote when the wiki may contain proprietary information.")


def cmd_init(args):
    root = resolve_root(args.root)
    changed = initialize_wiki(root)
    state = "initialized" if changed else "already initialized"
    print(f"{state} {root}")


def cmd_ingest(args):
    root = resolve_root(args.root)
    require_initialized(root)
    title = args.title or title_from_path(Path(args.source))
    path = wiki(root) / "sources" / f"{today()}-{slug(title)}.md"
    write_once(
        path,
        f"""---
title: "{title}"
kind: source
status: draft
tags: [swe]
sources: ["{args.source}"]
updated: {today()}
confidence: medium
---

# {title}

## Provenance

- Source: {args.source}
- Ingested: {today()}

## Summary

_Fill during ingestion._

## SWE Extraction

- _Fill during ingestion._

## Impacted Pages

- _Fill during ingestion._

## Open Questions

- _Fill during ingestion._
""",
    )
    rebuild_index(root)
    print(rel(path, root))


def cmd_query(args):
    root = resolve_root(args.root)
    require_initialized(root)
    terms = [
        term.lower()
        for term in re.findall(r"[a-zA-Z0-9_/-]+", args.query)
        if len(term) > 1
    ]
    hits = []
    for path in [wiki(root) / "index.md", *page_files(root)]:
        text = path.read_text(encoding="utf-8", errors="ignore")
        haystack = f"{path.name}\n{text}".lower()
        score = sum(haystack.count(term) for term in terms)
        if score:
            snippet = next(
                (
                    line.strip()
                    for line in text.splitlines()
                    if any(term in line.lower() for term in terms)
                ),
                "",
            )
            hits.append((score, path, snippet[:220]))
    for score, path, snippet in sorted(hits, reverse=True)[: args.limit]:
        print(f"{score:>3} {rel(path, root)}")
        if snippet:
            print(f"    {snippet}")


def cmd_log(args):
    root = resolve_root(args.root)
    require_initialized(root)
    append_log(root, args.kind, args.title, args.changed, args.notes, args.followups)
    print(f"logged {args.kind} | {args.title}")


def cmd_lint(args):
    root = resolve_root(args.root)
    if not root.exists():
        raise SweWikiError(f"{root} does not exist; run setup first")
    errors = []
    warnings = []

    required = [
        ".gitignore",
        "raw",
        "wiki",
        "wiki/index.md",
        "wiki/log.md",
        *[f"wiki/{directory}" for directory in KINDS],
    ]
    for item in required:
        if not (root / item).exists():
            errors.append(f"missing {item}")

    listed = index_links(root)
    for path in page_files(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        meta = frontmatter(text)
        page_rel = rel(path, wiki(root))
        if page_rel not in listed:
            errors.append(f"not listed in index: wiki/{page_rel}")
        for key in [
            "title",
            "kind",
            "status",
            "tags",
            "sources",
            "updated",
            "confidence",
        ]:
            if key not in meta:
                errors.append(f"missing frontmatter `{key}`: wiki/{page_rel}")
        if meta.get("kind") not in set(KINDS.values()):
            errors.append(f"bad kind `{meta.get('kind')}`: wiki/{page_rel}")
        for target in markdown_links(text):
            target_path = (path.parent / target).resolve()
            if not target_path.exists():
                errors.append(f"broken link in wiki/{page_rel}: {target}")

    index = wiki(root) / "index.md"
    if index.exists():
        for target in listed:
            if not (wiki(root) / target).exists():
                errors.append(f"index links missing page: wiki/{target}")

    log = wiki(root) / "log.md"
    if log.exists():
        headings = [
            line
            for line in log.read_text(encoding="utf-8").splitlines()
            if line.startswith("## ")
        ]
        for heading in headings:
            if not LOG_RE.match(heading):
                errors.append(f"bad log heading: {heading}")
        if not headings:
            warnings.append("log has no entries")

    inbound = {rel(path, wiki(root)): 0 for path in page_files(root)}
    for path in page_files(root):
        for target in markdown_links(
            path.read_text(encoding="utf-8", errors="ignore")
        ):
            target_path = path.parent / target
            norm = (
                rel(target_path.resolve(), wiki(root))
                if target_path.exists()
                else target
            )
            if norm in inbound:
                inbound[norm] += 1
    for page, count in inbound.items():
        if count == 0 and not page.startswith(("sources/", "questions/")):
            warnings.append(f"orphan page: wiki/{page}")

    for item in errors:
        print(f"ERROR {item}")
    for item in warnings:
        print(f"WARN {item}")
    if errors:
        return 1
    print("OK")
    return 0


def cmd_sync(args):
    root = resolve_root(args.root)
    require_initialized(root)
    committed, branch = sync_repository(root)
    action = "committed and synced" if committed else "synced"
    print(f"{action} {root} on {branch}")


def add_root_argument(parser):
    parser.add_argument(
        "--root",
        help="Wiki root. Defaults to saved config, then ~/.swe-wiki.",
    )


def build_parser():
    parser = argparse.ArgumentParser(
        description="Operate and synchronize a markdown SWE wiki."
    )
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    command = subparsers.add_parser("setup")
    command.add_argument("--root", help="Wiki directory. Defaults to ~/.swe-wiki.")
    command.add_argument("--repo", help="Existing Git repository URL.")
    command.set_defaults(func=cmd_setup)

    command = subparsers.add_parser("init")
    add_root_argument(command)
    command.set_defaults(func=cmd_init)

    command = subparsers.add_parser("ingest")
    command.add_argument("source")
    command.add_argument("--title")
    add_root_argument(command)
    command.set_defaults(func=cmd_ingest)

    command = subparsers.add_parser("query")
    command.add_argument("query")
    command.add_argument("--limit", type=int, default=10)
    add_root_argument(command)
    command.set_defaults(func=cmd_query)

    command = subparsers.add_parser("log")
    command.add_argument(
        "kind", choices=["bootstrap", "ingest", "query", "lint"]
    )
    command.add_argument("title")
    command.add_argument("--changed", action="append")
    command.add_argument("--notes")
    command.add_argument("--followups")
    add_root_argument(command)
    command.set_defaults(func=cmd_log)

    command = subparsers.add_parser("lint")
    add_root_argument(command)
    command.set_defaults(func=cmd_lint)

    command = subparsers.add_parser("sync")
    add_root_argument(command)
    command.set_defaults(func=cmd_sync)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args) or 0
    except (SweWikiError, OSError) as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
