"""Grade swe-wiki eval runs.

Usage: python3 evals/grade.py <iteration-dir>

Each run directory is <iteration-dir>/eval-<name>/<config>/run-<n>/ and holds
outputs/response.md plus the wiki-root/ the agent worked on.
"""

import filecmp
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

EVALS = Path(__file__).resolve().parent
NEW_SCRIPT = EVALS.parent / "scripts" / "swe_wiki.py"
FIX = EVALS / "files"
IT = Path(sys.argv[1])
PH = "_Fill during ingestion._"


def read(p):
    return p.read_text(encoding="utf-8", errors="ignore") if p.exists() else ""


def lint_errors(root):
    with tempfile.TemporaryDirectory() as home:
        r = subprocess.run(
            [sys.executable, str(NEW_SCRIPT), "lint", "--root", str(root)],
            capture_output=True,
            text=True,
            check=False,
            env={"HOME": home, "PATH": "/usr/bin:/bin"},
        )
    return [l for l in (r.stdout + r.stderr).splitlines() if l.startswith("ERROR")]


def tree_diff(a, b):
    out = []

    def walk(c):
        out.extend(f"changed {Path(c.left).name}/{n}" for n in c.diff_files)
        out.extend(f"only-in-run {n}" for n in c.right_only)
        out.extend(f"removed {n}" for n in c.left_only)
        for s in c.subdirs.values():
            walk(s)

    walk(filecmp.dircmp(a, b))
    return out


def fm(text, key):
    m = re.search(rf"^{key}:\s*(.*)$", text, re.MULTILINE)
    return m.group(1).strip().strip('"') if m else ""


def check(text, passed, evidence):
    return {"text": text, "passed": bool(passed), "evidence": evidence}


def grade_url(run, root, resp):
    raw = list((root / "raw" / "backend" / "caching").glob("*"))
    srcs = (
        [
            p
            for p in (root / "wiki" / "backend" / "caching" / "sources").glob("*.md")
            if p.name != "index.md"
        ]
        if (root / "wiki/backend/caching/sources").exists()
        else []
    )
    src = srcs[0] if srcs else None
    st = read(src) if src else ""
    log = read(root / "wiki" / "log.md")
    related = [
        p.name
        for p in (root / "wiki/backend/caching").glob("*.md")
        if p.name != "index.md" and src and src.name in read(p)
    ]
    urls = set(re.findall(r"https?://[^\s)>\]]+", st)) - {
        "https://martinfowler.com/bliki/TwoHardThings.html"
    }
    errs = lint_errors(root)
    return [
        check(
            "Raw layer holds an immutable local copy of the URL page under raw/backend/caching/",
            raw,
            f"raw files: {[p.name for p in raw]}",
        ),
        check(
            "Source page exists and has no `_Fill during ingestion._` placeholders",
            src and PH not in st,
            f"source={src.name if src else None}, placeholders={st.count(PH)}",
        ),
        check(
            "Source page has a non-empty `summary` frontmatter field",
            fm(st, "summary"),
            f"summary={fm(st, 'summary')[:80]!r}",
        ),
        check(
            "An existing durable page in backend/caching links to the new source page",
            related,
            f"pages linking source: {related}",
        ),
        check(
            "Source page cites at least one related external URL besides the source",
            urls,
            f"other urls: {sorted(urls)[:5]}",
        ),
        check(
            "wiki/log.md has an `ingest` entry",
            " ingest | " in log,
            "found" if " ingest | " in log else "missing",
        ),
        check(
            "Strict (new) mechanical lint reports no errors",
            not errs,
            "; ".join(errs[:4]) or "no errors",
        ),
    ]


def grade_local(run, root, resp):
    diff = tree_diff(FIX / "base-wiki", root)
    low = resp.lower()
    domains = re.findall(r"`([a-z0-9-]+(?:/[a-z0-9-]+)+)`", resp)
    return [
        check(
            "Wiki and raw trees are unchanged before approval",
            not diff,
            "; ".join(diff[:5]) or "no changes",
        ),
        check(
            "Response recommends a primary domain in kebab-case path form",
            domains,
            f"domains: {sorted(set(domains))[:5]}",
        ),
        check(
            "Response gives key takeaways from the notes",
            "takeaway" in low,
            "keyword 'takeaway' " + ("found" if "takeaway" in low else "missing"),
        ),
        check(
            "Response names related existing wiki pages (cache invalidation)",
            "cache-invalidation" in low or "cache invalidation" in low,
            "",
        ),
        check(
            "Response asks the user what to emphasize",
            "emphas" in low,
            "keyword 'emphas' " + ("found" if "emphas" in low else "missing"),
        ),
        check(
            "Response explicitly waits for approval before writing",
            any(k in low for k in ["approv", "confirm"]),
            "",
        ),
    ]


def grade_lint(run, root, resp):
    log = read(root / "wiki" / "log.md")
    entry = log.split(" lint | ")[-1] if " lint | " in log else ""
    cdn = read(root / "wiki/backend/caching/cdn-caching.md")
    low = resp.lower()
    errs = lint_errors(root)
    return [
        check("wiki/log.md has a `lint` entry", entry, ""),
        check(
            "The lint log entry records Follow-ups",
            "Follow-ups" in entry,
            entry[:200].replace("\n", " | "),
        ),
        check(
            "cdn-caching placeholder is fixed in the page or flagged to the user",
            PH not in cdn or ("cdn-caching" in low and "placeholder" in low),
            f"placeholder in page: {PH in cdn}",
        ),
        check(
            "Response names the TTL contradiction (60 s vs 300 s)",
            "60" in resp and "300" in resp,
            "",
        ),
        check(
            "Response suggests new questions or sources to fill gaps",
            "gap" in low or "next source" in low or "new source" in low,
            "keyword check; verify manually",
        ),
        check(
            "Strict (new) mechanical lint reports no errors after repair",
            not errs,
            "; ".join(errs[:4]) or "no errors",
        ),
    ]


def grade_query(run, root, resp):
    pages = [
        p for p in (root / "wiki").rglob("*.md") if fm(read(p), "kind") == "question"
    ]
    q = pages[0] if pages else None
    qt = read(q) if q else ""
    items = (
        re.findall(r"^- \[[ x]\]", qt.split("## Decision Checklist")[-1], re.MULTILINE)
        if "## Decision Checklist" in qt
        else []
    )
    idx = read(q.parent / "index.md") if q else ""
    log = read(root / "wiki" / "log.md")
    return [
        check(
            "A `kind: question` page is filed in the wiki",
            q,
            str(q.relative_to(root)) if q else "none",
        ),
        check(
            "Question page carries the local-convention tag `team-platform`",
            "team-platform" in fm(qt, "tags"),
            f"tags={fm(qt, 'tags')}",
        ),
        check(
            "Question page ends with a `## Decision Checklist` of 3-5 checkbox items",
            3 <= len(items) <= 5,
            f"items={len(items)}",
        ),
        check(
            "Response cites both cache-invalidation and write-through-cache pages",
            "cache-invalidation" in resp and "write-through-cache" in resp,
            "",
        ),
        check("Question page is listed in its local index", q and q.name in idx, ""),
        check("wiki/log.md has a `query` entry", " query | " in log, ""),
    ]


GRADERS = {
    "ingest-url-preapproved": grade_url,
    "ingest-local-needs-approval": grade_local,
    "lint-repair-with-gaps": grade_lint,
    "query-files-answer-with-local-convention": grade_query,
}

for ev in sorted(IT.glob("eval-*")):
    name = ev.name[5:]
    meta = json.loads(read(ev / "eval_metadata.json"))
    for run in sorted(ev.glob("*/run-*")):
        resp = read(run / "outputs" / "response.md")
        if not resp:
            print("skip (no response yet)", run.relative_to(IT))
            continue
        exps = GRADERS[name](run, run / "wiki-root", resp)
        passed = sum(e["passed"] for e in exps)
        g = {
            "expectations": exps,
            "summary": {
                "passed": passed,
                "failed": len(exps) - passed,
                "total": len(exps),
                "pass_rate": round(passed / len(exps), 2),
            },
        }
        t = run / "timing.json"
        if t.exists():
            g["timing"] = json.loads(read(t))
        (run / "grading.json").write_text(json.dumps(g, indent=2))
        meta["assertions"] = [e["text"] for e in exps]
        print(f"{passed}/{len(exps)}", run.relative_to(IT))
    (ev / "eval_metadata.json").write_text(json.dumps(meta, indent=2))
