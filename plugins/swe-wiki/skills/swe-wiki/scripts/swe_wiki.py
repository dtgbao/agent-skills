#!/usr/bin/env python3
import argparse
import datetime as dt
import filecmp
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

CONFIG_VERSION = 1
LEGACY_KIND_DIRS = {
    "sources": "source",
    "concepts": "concept",
    "decisions": "decision",
    "blueprints": "blueprint",
    "practices": "practice",
    "conventions": "convention",
    "systems": "system",
    "questions": "question",
}
KINDS = tuple(LEGACY_KIND_DIRS.values())
ACRONYMS = {"ai", "api", "aws", "cli", "ec2", "iam", "sdk", "swe", "vpc"}
DOMAIN_SEGMENT_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*$")
LOG_RE = re.compile(
    r"^## \[\d{4}-\d{2}-\d{2}(?: \d{2}:\d{2})?\] "
    r"(bootstrap|ingest|query|lint|migrate) \| .+"
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
    for directory in [root / "raw", wiki(root)]:
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


def index_files(root):
    base = wiki(root)
    if not base.exists():
        return []
    return sorted(base.rglob("index.md"))


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


def frontmatter_sources(text):
    value = frontmatter(text).get("sources", "[]")
    try:
        sources = json.loads(value)
    except json.JSONDecodeError:
        return []
    return sources if isinstance(sources, list) else []


def markdown_links(text):
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+\.md)(?:#[^)]+)?\)", text):
        target = match.group(1)
        if not re.match(r"[a-z]+://", target):
            yield target


def index_links(path):
    if not path.exists():
        return set()
    return set(markdown_links(path.read_text(encoding="utf-8")))


def source_count(meta):
    value = meta.get("sources", "")
    if value in {"", "[]"}:
        return 0
    return max(1, value.count(",") + 1)


def markdown_rel(path, start):
    return Path(os.path.relpath(path, start=start)).as_posix()


def index_row(index_dir, path):
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
        f"- [{title}]({markdown_rel(path, index_dir)}) - {summary} "
        f"| tags: {tags} | updated: {updated} | sources: {source_count(meta)}"
    )


def knowledge_dirs(root, pages=None):
    base = wiki(root)
    directories = {base}
    for page in pages if pages is not None else page_files(root):
        directory = page.parent
        while directory != base:
            directories.add(directory)
            directory = directory.parent
    return directories


def directory_counts(root, directory):
    pages = [path for path in page_files(root) if directory in path.parents]
    source_pages = [
        path
        for path in pages
        if frontmatter(path.read_text(encoding="utf-8")).get("kind") == "source"
    ]
    return len(pages), len(source_pages)


def directory_title(directory, base):
    if directory == base:
        return "SWE Wiki"
    return " ".join(
        part.upper() if part in ACRONYMS else part.capitalize()
        for part in directory.name.split("-")
    )


def rebuild_indexes(root):
    base = wiki(root)
    pages = page_files(root)
    directories = knowledge_dirs(root, pages)
    changed = []

    for directory in sorted(directories, key=lambda path: (len(path.parts), str(path))):
        children = sorted(
            child
            for child in directories
            if child.parent == directory
        )
        local_pages = sorted(path for path in pages if path.parent == directory)
        title = directory_title(directory, base)
        lines = [
            f"# {title}",
            "",
            "<!-- Generated by swe-wiki. -->",
            "",
        ]

        if children:
            lines += ["## Domains" if directory == base else "## Subdomains", ""]
            for child in children:
                count, source_count_value = directory_counts(root, child)
                child_title = directory_title(child, base)
                lines.append(
                    f"- [{child_title}]({child.name}/index.md) - "
                    f"{count} pages, {source_count_value} sources"
                )
            lines.append("")

        if local_pages:
            lines += ["## Local Pages", ""]
            sections = {kind: [] for kind in KINDS}
            for path in local_pages:
                meta = frontmatter(path.read_text(encoding="utf-8"))
                sections.setdefault(meta.get("kind", "concept"), []).append(
                    index_row(directory, path)
                )
            for kind in KINDS:
                rows = sorted(sections.get(kind, []))
                if rows:
                    lines += [f"### {kind.title()}s", "", *rows, ""]

        if not children and not local_pages:
            lines += ["_No knowledge yet._", ""]

        content = "\n".join(lines).rstrip() + "\n"
        index = directory / "index.md"
        if write_if_changed(index, content):
            changed.append(index)
    return changed


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
- File knowledge under one primary domain such as `wiki/aws/iam/`.
- Keep page kind in frontmatter instead of using kind-based directories.
- Maintain an `index.md` in every directory under `wiki/`.
- Keep `wiki/log.md` append-only with headings like `## [YYYY-MM-DD HH:MM] ingest | Title`.
- Use tags and cross-links for secondary domains instead of duplicating pages.
""",
    ):
        changed.append("AGENTS.md")
    if write_once(wiki(root) / "log.md", "# SWE Wiki Log\n\n"):
        changed.append("wiki/log.md")
    if not domain_layout_errors(root):
        changed.extend(rel(path, root) for path in rebuild_indexes(root))
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
    return paths


def require_initialized(root):
    if not all(path.exists() for path in required_wiki_paths(root)):
        raise SweWikiError(
            f"{root} is not initialized; run `setup` or `init --root {root}` first"
        )


def validate_domain(value):
    if not isinstance(value, str) or not value.strip():
        raise SweWikiError("a domain is required, for example `aws/iam`")
    value = value.strip().strip("/")
    segments = value.split("/")
    if any(
        segment == "sources" or not DOMAIN_SEGMENT_RE.fullmatch(segment)
        for segment in segments
    ):
        raise SweWikiError(
            f"invalid domain `{value}`; use lowercase kebab-case segments and "
            "reserve `sources` for provenance pages"
        )
    return "/".join(segments)


def expected_domain(root, path, kind=None):
    parts = path.resolve().relative_to(wiki(root).resolve()).parts
    kind = kind or frontmatter(path.read_text(encoding="utf-8")).get("kind")
    if kind == "source":
        if len(parts) < 3 or parts[-2] != "sources":
            return None
        domain_parts = parts[:-2]
    else:
        if len(parts) < 2 or parts[-2] == "sources":
            return None
        domain_parts = parts[:-1]
    try:
        return validate_domain("/".join(domain_parts))
    except SweWikiError:
        return None


def domain_layout_errors(root):
    errors = []
    for path in page_files(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        meta = frontmatter(text)
        page_rel = rel(path, wiki(root))
        domain = meta.get("domain")
        if not domain:
            errors.append(f"missing frontmatter `domain`: wiki/{page_rel}")
            continue
        try:
            domain = validate_domain(domain)
        except SweWikiError:
            errors.append(f"bad domain `{domain}`: wiki/{page_rel}")
            continue
        expected = expected_domain(root, path, meta.get("kind"))
        if expected != domain:
            errors.append(
                f"domain/path mismatch `{domain}`: wiki/{page_rel} "
                f"(expected {expected or 'a domain-first path'})"
            )
    return errors


def require_domain_layout(root):
    errors = domain_layout_errors(root)
    if errors:
        raise SweWikiError(
            "wiki uses the legacy or an invalid layout; preview and apply `migrate` "
            f"before ingesting ({errors[0]})"
        )


def is_web_url(value):
    return urlsplit(value).scheme.lower() in {"http", "https"}


def copy_raw_file(root, domain, value):
    source = root_path(value)
    if not source.exists() or not source.is_file():
        raise SweWikiError(f"local source file does not exist: {source}")
    target = root / "raw" / Path(domain) / source.name
    target.parent.mkdir(parents=True, exist_ok=True)
    if source == target.resolve():
        return target
    if target.exists():
        if filecmp.cmp(source, target, shallow=False):
            return target
        raise SweWikiError(
            f"raw file collision at {target}; rename the input or choose another domain"
        )
    shutil.copy2(source, target)
    return target


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
    errors = domain_layout_errors(root)
    if errors:
        print("legacy layout detected; preview and apply `migrate` before ingesting")


def cmd_ingest(args):
    root = resolve_root(args.root)
    require_initialized(root)
    require_domain_layout(root)
    domain = validate_domain(args.domain)
    title = args.title or title_from_path(Path(args.source))
    path = wiki(root) / Path(domain) / "sources" / f"{today()}-{slug(title)}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    source_values = []
    provenance = []
    for value in [args.source, *args.asset]:
        if is_web_url(value):
            source_values.append(value)
            provenance.append(f"- Source: {value}")
            continue
        copied = copy_raw_file(root, domain, value)
        reference = markdown_rel(copied, path.parent)
        source_values.append(reference)
        provenance.append(f"- Source: [{copied.name}]({reference})")

    write_once(
        path,
        f"""---
title: {json.dumps(title)}
kind: source
domain: {domain}
status: draft
tags: [swe]
sources: {json.dumps(source_values)}
updated: {today()}
confidence: medium
---

# {title}

## Provenance

{chr(10).join(provenance)}
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
    rebuild_indexes(root)
    print(rel(path, root))


def load_migration_manifest(path):
    try:
        payload = json.loads(root_path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SweWikiError(f"cannot read migration manifest {path}: {error}") from error
    assignments = payload.get("assignments") if isinstance(payload, dict) else None
    if not isinstance(assignments, list) or not assignments:
        raise SweWikiError("migration manifest requires a non-empty `assignments` list")
    return assignments


def contained_path(root, value):
    path = Path(value)
    if path.is_absolute():
        raise SweWikiError(f"migration path must be relative: {value}")
    resolved = (root / path).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as error:
        raise SweWikiError(f"migration path escapes the wiki root: {value}") from error
    return resolved


def migration_target(root, source, domain):
    relative = source.relative_to(root)
    if relative.parts[0] == "raw":
        return root / "raw" / Path(domain) / source.name
    if relative.parts[0] != "wiki" or source.suffix != ".md":
        raise SweWikiError(f"migration supports only raw files and wiki pages: {relative}")
    if source.name in {"index.md", "log.md"}:
        raise SweWikiError(f"generated indexes and the log cannot be assigned: {relative}")
    kind = frontmatter(source.read_text(encoding="utf-8")).get("kind")
    parent = wiki(root) / Path(domain)
    if kind == "source":
        parent /= "sources"
    return parent / source.name


def build_migration_plan(root, manifest):
    moves = []
    assigned = set()
    targets = {}
    for assignment in manifest:
        if not isinstance(assignment, dict):
            raise SweWikiError("each migration assignment must be an object")
        domain = validate_domain(assignment.get("domain"))
        paths = assignment.get("paths")
        if not isinstance(paths, list) or not paths:
            raise SweWikiError(f"migration assignment `{domain}` requires paths")
        for value in paths:
            if not isinstance(value, str):
                raise SweWikiError(f"migration paths for `{domain}` must be strings")
            source = contained_path(root, value)
            if not source.exists() or not source.is_file():
                raise SweWikiError(f"migration source does not exist: {value}")
            if source in assigned:
                raise SweWikiError(f"migration source is assigned twice: {value}")
            assigned.add(source)
            target = migration_target(root, source, domain).resolve()
            if target in targets and targets[target] != source:
                raise SweWikiError(
                    f"migration target collision: {rel(target, root)} receives "
                    f"{rel(targets[target], root)} and {value}"
                )
            if target.exists() and target != source:
                raise SweWikiError(f"migration target already exists: {rel(target, root)}")
            targets[target] = source
            moves.append((source, target, domain))

    for page in page_files(root):
        meta = frontmatter(page.read_text(encoding="utf-8", errors="ignore"))
        valid = meta.get("domain") and expected_domain(root, page, meta.get("kind")) == meta.get("domain")
        if not valid and page.resolve() not in assigned:
            raise SweWikiError(
                f"legacy page is missing from the migration manifest: {rel(page, root)}"
            )
    for raw_file in sorted((root / "raw").glob("*")):
        if raw_file.is_file() and raw_file.resolve() not in assigned:
            raise SweWikiError(
                f"flat raw file is missing from the migration manifest: {rel(raw_file, root)}"
            )
    return moves


def predicted_index_paths(root, moves):
    destinations = {source: target for source, target, _ in moves}
    pages = [destinations.get(path.resolve(), path.resolve()) for path in page_files(root)]
    return sorted(directory / "index.md" for directory in knowledge_dirs(root, pages))


def split_fragment(value):
    if "#" not in value:
        return value, ""
    path, fragment = value.split("#", 1)
    return path, f"#{fragment}"


def remap_reference(value, old_page, new_page, destinations):
    path_value, fragment = split_fragment(value)
    if (
        not path_value
        or path_value.startswith(("/", "#", "<"))
        or urlsplit(path_value).scheme
    ):
        return value
    old_target = (old_page.parent / path_value).resolve()
    new_target = destinations.get(old_target, old_target)
    return markdown_rel(new_target, new_page.parent) + fragment


def set_domain_frontmatter(text, domain):
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return text
    try:
        end = lines.index("---", 1)
    except ValueError:
        return text
    for index in range(1, end):
        if lines[index].startswith("domain:"):
            lines[index] = f"domain: {domain}"
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    insert_at = next(
        (index + 1 for index in range(1, end) if lines[index].startswith("kind:")),
        end,
    )
    lines.insert(insert_at, f"domain: {domain}")
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def rewrite_page_references(text, old_page, new_page, destinations):
    def replace_link(match):
        target = match.group(2)
        return f"{match.group(1)}{remap_reference(target, old_page, new_page, destinations)}{match.group(3)}"

    text = re.sub(r"(!?\[[^\]]*\]\()([^)]+)(\))", replace_link, text)
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith("sources:"):
            continue
        raw_value = line.split(":", 1)[1].strip()
        try:
            values = json.loads(raw_value)
        except json.JSONDecodeError:
            continue
        if isinstance(values, list):
            values = [
                remap_reference(value, old_page, new_page, destinations)
                if isinstance(value, str)
                else value
                for value in values
            ]
            lines[index] = f"sources: {json.dumps(values)}"
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def remove_empty_legacy_directories(root):
    for name in LEGACY_KIND_DIRS:
        base = wiki(root) / name
        if not base.exists():
            continue
        for directory in sorted(
            [path for path in base.rglob("*") if path.is_dir()] + [base],
            key=lambda path: len(path.parts),
            reverse=True,
        ):
            index = directory / "index.md"
            if index.exists() and "<!-- Generated by swe-wiki. -->" in index.read_text(
                encoding="utf-8", errors="ignore"
            ):
                index.unlink()
            try:
                directory.rmdir()
            except OSError:
                pass


def require_clean_worktree(root):
    if not (root / ".git").exists():
        return
    result = run_git(["status", "--porcelain"], cwd=root)
    if result.stdout.strip():
        raise SweWikiError("migration apply requires a clean Git worktree")


def apply_migration(root, moves):
    require_clean_worktree(root)
    destinations = {source.resolve(): target.resolve() for source, target, _ in moves}
    domains = {source.resolve(): domain for source, _, domain in moves}
    original_pages = {path.resolve(): path.read_text(encoding="utf-8") for path in page_files(root)}
    rewritten_pages = {}
    for old_page, text in original_pages.items():
        new_page = destinations.get(old_page, old_page)
        if old_page in domains:
            text = set_domain_frontmatter(text, domains[old_page])
        rewritten_pages[(old_page, new_page)] = rewrite_page_references(
            text, old_page, new_page, destinations
        )

    for source, target, _ in moves:
        if source.parts[: len((root / "raw").parts)] != (root / "raw").parts:
            continue
        if source != target:
            target.parent.mkdir(parents=True, exist_ok=True)
            source.replace(target)

    for (old_page, new_page), text in rewritten_pages.items():
        new_page.parent.mkdir(parents=True, exist_ok=True)
        new_page.write_text(text, encoding="utf-8")
        if old_page != new_page and old_page.exists():
            old_page.unlink()

    remove_empty_legacy_directories(root)
    indexes = rebuild_indexes(root)
    changed = [rel(target, root) for _, target, _ in moves]
    changed.extend(rel(path, root) for path in indexes)
    append_log(
        root,
        "migrate",
        "Domain-first wiki layout",
        changed=sorted(set(changed)),
        notes="Moved knowledge and raw sources into approved primary domains.",
    )


def cmd_migrate(args):
    root = resolve_root(args.root)
    require_initialized(root)
    manifest = load_migration_manifest(args.manifest)
    moves = build_migration_plan(root, manifest)
    indexes = predicted_index_paths(root, moves)
    if args.apply:
        apply_migration(root, moves)
    action = "Migration plan" if not args.apply else "Applied migration"
    print(action)
    for source, target, _ in moves:
        verb = "UPDATE" if source == target else "MOVE"
        print(f"{verb} {rel(source, root)} -> {rel(target, root)}")
    for path in indexes:
        print(f"INDEX {rel(path, root)}")


def cmd_query(args):
    root = resolve_root(args.root)
    require_initialized(root)
    terms = [
        term.lower()
        for term in re.findall(r"[a-zA-Z0-9_/-]+", args.query)
        if len(term) > 1
    ]
    hits = []
    root_index = wiki(root) / "index.md"
    nested_indexes = [path for path in index_files(root) if path != root_index]
    for path in [root_index, *nested_indexes, *page_files(root)]:
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

    required = [".gitignore", "raw", "wiki", "wiki/index.md", "wiki/log.md"]
    for item in required:
        if not (root / item).exists():
            errors.append(f"missing {item}")

    pages = page_files(root)
    errors.extend(domain_layout_errors(root))
    for directory in knowledge_dirs(root, pages):
        if not (directory / "index.md").exists():
            errors.append(f"missing local index: {rel(directory / 'index.md', root)}")

    for path in page_files(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        meta = frontmatter(text)
        page_rel = rel(path, wiki(root))
        local_index = path.parent / "index.md"
        listed_targets = {
            (local_index.parent / target).resolve()
            for target in index_links(local_index)
        }
        if path.resolve() not in listed_targets:
            errors.append(f"not listed in local index: wiki/{page_rel}")
        for key in [
            "title",
            "kind",
            "domain",
            "status",
            "tags",
            "sources",
            "updated",
            "confidence",
        ]:
            if key not in meta:
                errors.append(f"missing frontmatter `{key}`: wiki/{page_rel}")
        if meta.get("kind") not in set(KINDS):
            errors.append(f"bad kind `{meta.get('kind')}`: wiki/{page_rel}")
        for target in markdown_links(text):
            target_path = (path.parent / target).resolve()
            if not target_path.exists():
                errors.append(f"broken link in wiki/{page_rel}: {target}")

        domain = meta.get("domain")
        if domain:
            try:
                raw_domain = (root / "raw" / Path(validate_domain(domain))).resolve()
            except SweWikiError:
                raw_domain = None
            if raw_domain:
                for source in frontmatter_sources(text):
                    if not isinstance(source, str) or urlsplit(source).scheme:
                        continue
                    source_path = (path.parent / split_fragment(source)[0]).resolve()
                    try:
                        source_path.relative_to((root / "raw").resolve())
                    except ValueError:
                        continue
                    try:
                        source_path.relative_to(raw_domain)
                    except ValueError:
                        errors.append(
                            f"raw source outside domain `{domain}` in wiki/{page_rel}: {source}"
                        )

    for index in index_files(root):
        for target in index_links(index):
            if not (index.parent / target).resolve().exists():
                errors.append(
                    f"index link missing target in {rel(index, root)}: {target}"
                )

    root_index = wiki(root) / "index.md"
    if root_index.exists():
        for target in index_links(root_index):
            target_path = (root_index.parent / target).resolve()
            if target_path.name != "index.md" or target_path.parent.parent != wiki(root).resolve():
                errors.append(f"root index must link only top-level domains: {target}")

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

    inbound = {rel(path, wiki(root)): 0 for path in pages}
    for path in pages:
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
        path = wiki(root) / page
        kind = frontmatter(path.read_text(encoding="utf-8", errors="ignore")).get("kind")
        if count == 0 and kind not in {"source", "question"}:
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
    command.add_argument("--domain", required=True)
    command.add_argument("--asset", action="append", default=[])
    command.add_argument("--title")
    add_root_argument(command)
    command.set_defaults(func=cmd_ingest)

    command = subparsers.add_parser("migrate")
    command.add_argument("manifest")
    command.add_argument("--apply", action="store_true")
    add_root_argument(command)
    command.set_defaults(func=cmd_migrate)

    command = subparsers.add_parser("query")
    command.add_argument("query")
    command.add_argument("--limit", type=int, default=10)
    add_root_argument(command)
    command.set_defaults(func=cmd_query)

    command = subparsers.add_parser("log")
    command.add_argument(
        "kind", choices=["bootstrap", "ingest", "query", "lint", "migrate"]
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
