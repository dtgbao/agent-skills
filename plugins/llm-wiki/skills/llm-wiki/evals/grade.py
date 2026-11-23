#!/usr/bin/env python3
"""Grade one llm-wiki eval run.

    python3 evals/grade.py --eval NAME --run-dir RUN_DIR

RUN_DIR must hold outputs/wiki-root (the wiki after the run) and, optionally,
outputs/response.md (the final message to the user). The script compares the wiki
with the fixture named in evals.json and writes RUN_DIR/grading.json.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

EVALS_DIR = Path(__file__).resolve().parent
SKILL_DIR = EVALS_DIR.parent
SPEC = importlib.util.spec_from_file_location(
    "llm_wiki", SKILL_DIR / "scripts" / "llm_wiki.py"
)
assert SPEC is not None and SPEC.loader is not None
lw = importlib.util.module_from_spec(SPEC)
sys.modules["llm_wiki"] = lw
SPEC.loader.exec_module(lw)

DOMAIN_IN_TICKS = re.compile(
    r"`[a-z0-9]+(?:-[a-z0-9]+)*(?:/[a-z0-9]+(?:-[a-z0-9]+)*)+`"
)
CONFLICT_RE = re.compile(r"contradict|conflict|supersed|disagree", re.IGNORECASE)
WEB_CITATION_RE = re.compile(
    r"\]\(https?://[^)\s]+\)[^\[\]]{0,80}?retrieved \d{4}-\d{2}-\d{2}", re.IGNORECASE
)
HEADING_RE = re.compile(r"^(#|\*\*[^*].*\*\*[:.]?\s*$)")


class Run:
    def __init__(self, run_dir: Path, fixture: Path) -> None:
        self.root = run_dir / "outputs" / "wiki-root"
        self.fixture = fixture
        response = run_dir / "outputs" / "response.md"
        self.response = (
            response.read_text(encoding="utf-8") if response.is_file() else ""
        )
        self.wiki = lw.Wiki(self.root)
        self.base = lw.Wiki(fixture)

    def files(self, root: Path) -> dict[str, bytes]:
        out: dict[str, bytes] = {}
        for path in root.rglob("*"):
            rel = path.relative_to(root)
            if path.is_file() and ".git" not in rel.parts and path.name != ".DS_Store":
                out[rel.as_posix()] = path.read_bytes()
        return out

    def new_pages(self) -> list[Any]:
        old = {p.rel for p in self.base.pages()}
        return [p for p in self.wiki.pages() if p.rel not in old]

    def new_log_entries(self) -> list[Any]:
        old = len(lw.read_log(self.base)[0])
        return lw.read_log(self.wiki)[0][old:]

    def lint(self) -> dict[str, Any]:
        return lw.lint_wiki(self.wiki)

    def log_prefix_kept(self) -> tuple[bool, str]:
        old = self.base.log.read_text(encoding="utf-8").rstrip("\n")
        new = (
            self.wiki.log.read_text(encoding="utf-8") if self.wiki.log.is_file() else ""
        )
        return new.startswith(
            old
        ), f"fixture log {len(old)} chars; new log {len(new)} chars"

    def raw_untouched(self) -> tuple[bool, str]:
        old = {
            k: v for k, v in self.files(self.fixture).items() if k.startswith("raw/")
        }
        new = self.files(self.root)
        changed = [k for k, v in old.items() if new.get(k) != v]
        return not changed, f"changed or removed raw files: {changed or 'none'}"


def entry_names(entry: Any, page_rel: str, title: str) -> bool:
    return (
        f"wiki/{page_rel}" in entry.body
        or page_rel in entry.body
        or entry.title == title
    )


def link_contexts(page: Any, target: Path) -> list[str]:
    """For each link from page to target: the nearest heading (or bold line) plus the paragraph."""
    lines = page.text.splitlines()
    contexts: list[str] = []
    for number, link in lw.page_links(page):
        if lw.resolve_link(page, link) != target:
            continue
        at = number - 1
        start = at
        while start > 0 and lines[start - 1].strip():
            start -= 1
        end = at
        while end + 1 < len(lines) and lines[end + 1].strip():
            end += 1
        heading = next(
            (lines[i] for i in range(start - 1, -1, -1) if HEADING_RE.match(lines[i])),
            "",
        )
        contexts.append("\n".join([heading, *lines[start : end + 1]]))
    return contexts


def flags_link(page: Any | None, target: Path, pattern: re.Pattern[str]) -> bool:
    return bool(page) and any(pattern.search(c) for c in link_contexts(page, target))


def linked_from(run: Run, page: Any) -> list[str]:
    return [
        other.rel
        for other in run.wiki.pages()
        if other.path != page.path
        and any(lw.resolve_link(other, t) == page.path for _, t in lw.page_links(other))
    ]


def page_at(run: Run, rel: str) -> Any | None:
    return next((p for p in run.wiki.pages() if p.rel == rel), None)


def lint_clean(run: Run) -> tuple[bool, str]:
    errors = run.lint()["errors"]
    return (
        not errors,
        f"{len(errors)} errors: {[e['code'] + ' ' + e['path'] for e in errors][:6]}",
    )


def log_entry(run: Run, op: str, page: Any | None) -> tuple[bool, str]:
    entries = [e for e in run.new_log_entries() if e.op == op]
    if page is None:
        return bool(entries), f"new {op} entries: {[e.title for e in entries]}"
    hits = [e for e in entries if entry_names(e, page.rel, page.title)]
    return bool(
        hits
    ), f"new {op} entries: {[e.title for e in entries]}; naming {page.rel}: {len(hits)}"


# ---------------------------------------------------------------- eval 1


def eval_url_snapshot(run: Run) -> dict[str, tuple[bool, str]]:
    source = (
        EVALS_DIR / "fixtures/sources/permission-boundaries-explained.html"
    ).read_bytes()
    old_files = run.files(run.fixture)
    snaps = [
        rel
        for rel, data in run.files(run.root).items()
        if rel.startswith("raw/") and rel not in old_files and data == source
    ]
    pages = [p for p in run.new_pages() if p.get("kind") == "source"]
    page = pages[0] if pages else None
    summary = page.get("summary") if page else ""
    results: dict[str, tuple[bool, str]] = {}
    results["snapshot"] = (bool(snaps), f"identical snapshots: {snaps or 'none'}")
    results["source-page-summary"] = (
        bool(page)
        and 0 < len(summary) <= lw.SUMMARY_MAX
        and lw.PLACEHOLDER not in summary,
        f"page={page.rel if page else None} summary={summary!r} ({len(summary)} chars)",
    )
    listed = page.get_list("sources") if page else []
    results["sources-field"] = (
        bool(snaps) and any(s in listed for s in snaps),
        f"sources={listed}",
    )
    index = run.root / "wiki/aws/iam/index.md"
    index_text = index.read_text(encoding="utf-8") if index.is_file() else ""
    results["index-uses-summary"] = (
        bool(page) and bool(summary) and lw.cell(summary) in index_text,
        f"summary in index: {bool(summary) and lw.cell(summary) in index_text}",
    )
    types = page_at(run, "aws/iam/policy-types.md")
    old_types = (run.fixture / "wiki/aws/iam/policy-types.md").read_text(
        encoding="utf-8"
    )
    changed = bool(types) and types.text != old_types
    flagged = bool(page) and flags_link(types, page.path, CONFLICT_RE)
    results["contradiction"] = (
        changed and flagged,
        f"changed={changed} conflict word next to a link to the source page={flagged}",
    )
    back = bool(types) and flags_link(page, types.path, CONFLICT_RE)
    results["contradiction-source-page"] = (
        back,
        f"conflict word next to a link to policy-types.md={back}",
    )
    results["ingest-log"] = (
        log_entry(run, "ingest", page) if page else (False, "no new source page")
    )
    results["log-append-only"] = run.log_prefix_kept()
    results["lint-clean"] = lint_clean(run)
    return results


# ---------------------------------------------------------------- eval 2


def takeaway_count(text: str) -> int:
    lines = text.splitlines()
    start = next(
        (
            i
            for i, line in enumerate(lines)
            if re.search(r"takeaway", line, re.IGNORECASE)
        ),
        -1,
    )
    if start < 0:
        return 0
    count = 0
    seen_item = False
    for line in lines[start + 1 :]:
        stripped = line.strip()
        if re.match(r"^(\d+[.)]|[-*•])\s+\S", stripped):
            count += 1
            seen_item = True
        elif seen_item and stripped and not line.startswith((" ", "\t")):
            break
    return count


def eval_approval_gate(run: Run) -> dict[str, tuple[bool, str]]:
    old = run.files(run.fixture)
    new = run.files(run.root)
    changed = sorted(k for k in set(old) | set(new) if old.get(k) != new.get(k))
    text = run.response
    n = takeaway_count(text)
    domains = DOMAIN_IN_TICKS.findall(text)
    return {
        "no-writes": (not changed, f"changed files: {changed[:8] or 'none'}"),
        "domain-path": (bool(domains), f"domain paths in backticks: {domains[:4]}"),
        "alternatives": (
            bool(re.search(r"alternativ", text, re.IGNORECASE)),
            "looked for 'alternative'",
        ),
        "takeaways": (3 <= n <= 5, f"{n} takeaway items"),
        "related-page": (
            bool(re.search(r"retry-policy|gateway retry policy", text, re.IGNORECASE)),
            "looked for retry-policy",
        ),
        "contradiction": (
            bool(re.search(r"contradict|conflict|supersed", text, re.IGNORECASE)),
            "looked for contradict/conflict/supersede",
        ),
        "emphasis": (
            bool(re.search(r"emphasi[sz]", text, re.IGNORECASE)),
            "looked for 'emphasize'",
        ),
    }


# ---------------------------------------------------------------- eval 3


def eval_local_convention(run: Run) -> dict[str, tuple[bool, str]]:
    pages = [p for p in run.new_pages() if p.get("kind") == "question"]
    page = pages[0] if pages else None
    results: dict[str, tuple[bool, str]] = {}
    results["question-page"] = (
        bool(page),
        f"new question pages: {[p.rel for p in pages]}",
    )
    name = Path(page.rel).name if page else ""
    results["q-prefix"] = (name.startswith("q-"), f"file name: {name or None}")
    confidence = False
    detail = "no page"
    if page:
        sections = re.split(r"(?m)^## ", page.body)
        last = sections[-1] if len(sections) > 1 else ""
        confidence = last.lower().startswith("confidence") and bool(
            re.search(r"\b(high|medium|low)\b", last, re.IGNORECASE)
        )
        detail = f"last H2 section starts: {last[:60]!r}"
    results["confidence"] = (confidence, detail)
    links = linked_from(run, page) if page else []
    results["linked"] = (bool(links), f"linked from: {links or 'none'}")
    results["query-log"] = (
        log_entry(run, "query", page) if page else (False, "no question page")
    )
    results["lint-clean"] = lint_clean(run)
    return results


# ---------------------------------------------------------------- eval 4


def eval_lint_follow_ups(run: Run) -> dict[str, tuple[bool, str]]:
    report = run.lint()
    entries = [e for e in run.new_log_entries() if e.op == "lint"]
    items: list[str] = []
    for entry in entries:
        match = re.search(r"(?ims)^###\s+follow-ups\s*$(.*?)(?=^###\s|\Z)", entry.body)
        if match:
            items += [
                m.strip() for m in re.findall(r"(?m)^\s*[-*]\s+(.+)$", match.group(1))
            ]
    questions = [
        i
        for i in items
        if re.match(r"^(question|q)\b", i, re.IGNORECASE) or i.rstrip().endswith("?")
    ]
    sources = [
        i
        for i in items
        if re.match(r"^source\b", i, re.IGNORECASE)
        or re.search(
            r"https?://|guide|documentation|docs\b|paper|article|report",
            i,
            re.IGNORECASE,
        )
    ]
    stale = [w for w in report["warnings"] if w["code"] == "index-stale"]
    org_index = run.root / "wiki/aws/organizations/index.md"
    hand_edit_gone = org_index.is_file() and "Hand note" not in org_index.read_text(
        encoding="utf-8"
    )
    missing = [
        w["path"] for w in report["warnings"] if w["code"] == "ingest-log-missing"
    ]
    return {
        "lint-clean": lint_clean(run),
        "raw-untouched": run.raw_untouched(),
        "log-append-only": run.log_prefix_kept(),
        "lint-log-follow-ups": (
            len(items) >= 2,
            f"{len(entries)} lint entries; {len(items)} follow-ups",
        ),
        "follow-up-kinds": (
            bool(questions) and bool(sources),
            f"questions={len(questions)} sources={len(sources)}",
        ),
        "indexes-current": (
            not stale and hand_edit_gone,
            f"stale={len(stale)} hand_edit_gone={hand_edit_gone}",
        ),
        "ingest-log-fixed": (not missing, f"ingest-log-missing: {missing or 'none'}"),
    }


# ---------------------------------------------------------------- eval 5


RUNBOOK_SECTIONS = ("when to use", "steps", "rollback")


def eval_schema(run: Run) -> dict[str, tuple[bool, str]]:
    schema = run.root / "AGENTS.md"
    text = schema.read_text(encoding="utf-8") if schema.is_file() else ""
    match = re.search(r"(?ims)^## Local conventions\s*$(.*?)(?=^## |\Z)", text)
    section = match.group(1) if match else ""
    bullet = re.search(
        r"(?im)^\s*[-*].*(\d{4}-\d{2}-\d{2}.*runbook|runbook.*\d{4}-\d{2}-\d{2})",
        section,
    )
    pages = [p for p in run.new_pages() if p.get("kind") == "runbook"]
    page = pages[0] if pages else None
    headings = (
        [h.strip().lower() for h in re.findall(r"(?m)^## (.+)$", page.body)]
        if page
        else []
    )
    missing = [s for s in RUNBOOK_SECTIONS if s not in headings]
    links = linked_from(run, page) if page else []
    stale = [w["path"] for w in run.lint()["warnings"] if w["code"] == "index-stale"]
    return {
        "kinds-marker": (
            "runbook" in run.wiki.extra_kinds(),
            f"extra kinds: {run.wiki.extra_kinds()}",
        ),
        "schema-bullet": (
            bool(bullet),
            f"Local conventions section: {section.strip()[:200]!r}",
        ),
        "schema-log": log_entry(run, "schema", None),
        "runbook-page": (
            bool(page) and not missing,
            f"runbook pages={[p.rel for p in pages]} missing sections={missing}",
        ),
        "linked": (bool(links), f"linked from: {links or 'none'}"),
        "indexes-current": (not stale, f"stale indexes: {stale or 'none'}"),
        "log-append-only": run.log_prefix_kept(),
        "raw-untouched": run.raw_untouched(),
        "lint-clean": lint_clean(run),
    }


# ---------------------------------------------------------------- eval 6


MANAGEMENT_RE = re.compile(r"management account", re.IGNORECASE)
REFUTED_RE = re.compile(
    r"contradict|conflict|incorrect|wrong|false|not true|inaccurate|"
    r"do(?:es)? not (?:apply|affect|restrict)|don't|doesn't|exempt|unaffected",
    re.IGNORECASE,
)


def eval_research(run: Run) -> dict[str, tuple[bool, str]]:
    source = (EVALS_DIR / "fixtures/sources/scp-rollout-notes.md").read_bytes()
    old_files = run.files(run.fixture)
    new_files = run.files(run.root)
    new_raw = [r for r in new_files if r.startswith("raw/") and r not in old_files]
    copies = [r for r in new_raw if new_files[r] == source]
    pages = [
        p
        for p in run.new_pages()
        if p.get("kind") == "source" and p.directory == "aws/organizations"
    ]
    page = pages[0] if pages else None
    summary = page.get("summary") if page else ""
    changed = [
        p
        for p in run.wiki.pages()
        if old_files.get(f"wiki/{p.rel}") != p.path.read_bytes()
    ]
    cited = [p.rel for p in changed if WEB_CITATION_RE.search(p.text)]
    flagged = False
    if page:
        paragraphs = re.split(r"\n\s*\n", page.body)
        flagged = any(
            MANAGEMENT_RE.search(par) and REFUTED_RE.search(par) for par in paragraphs
        )
    scp = page_at(run, "aws/organizations/scp.md")
    old_scp = (run.fixture / "wiki/aws/organizations/scp.md").read_text(
        encoding="utf-8"
    )
    scp_links = (
        bool(scp)
        and bool(page)
        and any(lw.resolve_link(scp, t) == page.path for _, t in lw.page_links(scp))
    )
    return {
        "source-page": (
            bool(page) and bool(summary) and lw.PLACEHOLDER not in summary,
            f"page={page.rel if page else None} summary={summary!r}",
        ),
        "raw-only-source": (
            len(new_raw) == 1 and len(copies) == 1,
            f"new raw files: {new_raw or 'none'}",
        ),
        "web-citation": (bool(cited), f"pages with dated web citations: {cited}"),
        "management-account": (
            flagged,
            "a source-page paragraph names the management account and refutes the claim",
        ),
        "scp-updated": (
            bool(scp) and scp.text != old_scp and scp_links,
            f"changed={bool(scp) and scp.text != old_scp} links to source={scp_links}",
        ),
        "ingest-log": (
            log_entry(run, "ingest", page) if page else (False, "no new source page")
        ),
        "log-append-only": run.log_prefix_kept(),
        "lint-clean": lint_clean(run),
    }


GRADERS: dict[str, Callable[[Run], dict[str, tuple[bool, str]]]] = {
    "url-snapshot-preapproved": eval_url_snapshot,
    "approval-gate": eval_approval_gate,
    "local-convention-query": eval_local_convention,
    "lint-follow-ups": eval_lint_follow_ups,
    "schema-co-evolution": eval_schema,
    "research-preapproved": eval_research,
}


def grade(eval_name: str, run_dir: Path) -> dict[str, Any]:
    spec = json.loads((EVALS_DIR / "evals.json").read_text(encoding="utf-8"))
    item = next(e for e in spec["evals"] if e["name"] == eval_name)
    run = Run(run_dir, EVALS_DIR / item["fixture"])
    if not run.root.is_dir():
        results = {
            a["id"]: (False, "outputs/wiki-root is missing") for a in item["assertions"]
        }
    else:
        results = GRADERS[eval_name](run)
    expectations = []
    for assertion in item["assertions"]:
        passed, evidence = results.get(assertion["id"], (False, "not graded"))
        expectations.append(
            {"text": assertion["text"], "passed": bool(passed), "evidence": evidence}
        )
    passed_count = sum(1 for e in expectations if e["passed"])
    total = len(expectations)
    return {
        "expectations": expectations,
        "summary": {
            "passed": passed_count,
            "failed": total - passed_count,
            "total": total,
            "pass_rate": round(passed_count / total, 2) if total else 0.0,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--eval", required=True, choices=sorted(GRADERS))
    parser.add_argument("--run-dir", required=True, type=Path)
    args = parser.parse_args()
    result = grade(args.eval, args.run_dir)
    (args.run_dir / "grading.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    summary = result["summary"]
    print(f"{args.eval}: {summary['passed']}/{summary['total']} passed")
    for item in result["expectations"]:
        print(
            f"  [{'x' if item['passed'] else ' '}] {item['text']} — {item['evidence']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
