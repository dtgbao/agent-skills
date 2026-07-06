#!/usr/bin/env python3
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

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

LOG_RE = re.compile(r"^## \[\d{4}-\d{2}-\d{2}(?: \d{2}:\d{2})?\] (bootstrap|ingest|query|lint) \| .+")


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


def wiki(root):
    return root / "wiki"


def rel(path, root):
    return path.resolve().relative_to(root.resolve()).as_posix()


def ensure_dirs(root):
    (root / "raw").mkdir(parents=True, exist_ok=True)
    wiki(root).mkdir(parents=True, exist_ok=True)
    for directory in KINDS:
        (wiki(root) / directory).mkdir(parents=True, exist_ok=True)


def write_once(path, text):
    if not path.exists():
        path.write_text(text, encoding="utf-8")


def page_files(root):
    base = wiki(root)
    if not base.exists():
        return []
    return sorted(
        p for p in base.rglob("*.md")
        if p.name not in {"index.md", "log.md"} and "_templates" not in p.parts
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
    return f"- [{title}]({rel(path, wiki(root))}) - {summary} | tags: {tags} | updated: {updated} | sources: {source_count(meta)}"


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
    for kind in ["source", "concept", "decision", "blueprint", "practice", "convention", "system", "question"]:
        lines += [f"## {kind.title()}s", ""]
        lines += sorted(sections.get(kind, [])) or ["_None yet._"]
        lines.append("")
    (wiki(root) / "index.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def cmd_init(args):
    root = root_path(args.root)
    ensure_dirs(root)
    write_once(root / "AGENTS.md", """# SWE Wiki Schema

Use `$swe-wiki` to ingest sources, query accumulated knowledge, and lint this wiki.

- Keep `raw/` immutable.
- Maintain `wiki/index.md` on every ingest or durable query.
- Keep `wiki/log.md` append-only with headings like `## [YYYY-MM-DD HH:MM] ingest | Title`.
- Put durable software engineering knowledge in the page kind that owns it.
""")
    write_once(wiki(root) / "log.md", "# SWE Wiki Log\n\n")
    rebuild_index(root)
    append_log(root, "bootstrap", "SWE wiki initialized", changed=["AGENTS.md", "wiki/index.md", "wiki/log.md"])
    print(f"initialized {root}")


def cmd_ingest(args):
    root = root_path(args.root)
    ensure_dirs(root)
    title = args.title or title_from_path(Path(args.source))
    path = wiki(root) / "sources" / f"{today()}-{slug(title)}.md"
    write_once(path, f"""---
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
""")
    rebuild_index(root)
    print(rel(path, root))


def cmd_query(args):
    root = root_path(args.root)
    terms = [t.lower() for t in re.findall(r"[a-zA-Z0-9_/-]+", args.query) if len(t) > 1]
    hits = []
    for path in [wiki(root) / "index.md", *page_files(root)]:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        haystack = f"{path.name}\n{text}".lower()
        score = sum(haystack.count(term) for term in terms)
        if score:
            snippet = next((line.strip() for line in text.splitlines() if any(t in line.lower() for t in terms)), "")
            hits.append((score, path, snippet[:220]))
    for score, path, snippet in sorted(hits, reverse=True)[:args.limit]:
        print(f"{score:>3} {rel(path, root)}")
        if snippet:
            print(f"    {snippet}")


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
    with path.open("a", encoding="utf-8") as f:
        f.write("\n" + "\n".join(lines) + "\n")


def cmd_log(args):
    root = root_path(args.root)
    append_log(root, args.kind, args.title, args.changed, args.notes, args.followups)
    print(f"logged {args.kind} | {args.title}")


def cmd_lint(args):
    root = root_path(args.root)
    errors = []
    warnings = []

    for required in ["raw", "wiki", "wiki/index.md", "wiki/log.md", *[f"wiki/{d}" for d in KINDS]]:
        if not (root / required).exists():
            errors.append(f"missing {required}")

    listed = index_links(root)
    for path in page_files(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        meta = frontmatter(text)
        page_rel = rel(path, wiki(root))
        if page_rel not in listed:
            errors.append(f"not listed in index: wiki/{page_rel}")
        for key in ["title", "kind", "status", "tags", "sources", "updated", "confidence"]:
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
        headings = [line for line in log.read_text(encoding="utf-8").splitlines() if line.startswith("## ")]
        for heading in headings:
            if not LOG_RE.match(heading):
                errors.append(f"bad log heading: {heading}")
        if not headings:
            warnings.append("log has no entries")

    inbound = {rel(p, wiki(root)): 0 for p in page_files(root)}
    for path in page_files(root):
        for target in markdown_links(path.read_text(encoding="utf-8", errors="ignore")):
            norm = rel((path.parent / target).resolve(), wiki(root)) if (path.parent / target).exists() else target
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


def main(argv=None):
    parser = argparse.ArgumentParser(description="Operate a markdown SWE wiki.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init")
    p.add_argument("root")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("ingest")
    p.add_argument("root")
    p.add_argument("source")
    p.add_argument("--title")
    p.set_defaults(func=cmd_ingest)

    p = sub.add_parser("query")
    p.add_argument("root")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=cmd_query)

    p = sub.add_parser("log")
    p.add_argument("root")
    p.add_argument("kind", choices=["bootstrap", "ingest", "query", "lint"])
    p.add_argument("title")
    p.add_argument("--changed", action="append")
    p.add_argument("--notes")
    p.add_argument("--followups")
    p.set_defaults(func=cmd_log)

    p = sub.add_parser("lint")
    p.add_argument("root")
    p.set_defaults(func=cmd_lint)

    args = parser.parse_args(argv)
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
