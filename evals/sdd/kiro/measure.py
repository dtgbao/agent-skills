"""Measure spec artifacts (Kiro or sdd). Usage: python3 measure.py <label>=<spec-dir> ..."""
import json, re, sys
from pathlib import Path

def read(d, *names):
    for n in names:
        p = d / n
        if p.exists():
            return p.read_text()
    return ""

def req_stats(t):
    crit = re.findall(r"^\s*(?:\d+\.)+\d*\s+(.*)$", t.split("## Requirements", 1)[-1], re.M)
    crit = [c for c in crit if re.search(r"\bSHALL\b", c)]
    pat = {"WHEN": 0, "IF": 0, "WHILE": 0, "WHERE": 0, "UBIQ": 0}
    for c in crit:
        s = c.lstrip("*").strip()
        k = next((k for k in ("WHEN", "IF", "WHILE", "WHERE") if s.upper().startswith(k)), "UBIQ")
        pat[k] += 1
    multi = sum(1 for c in crit if len(re.findall(r"\bSHALL\b", c)) > 1 or re.search(r"\bSHALL\b[^.]*\band\b[^.]*\b(return|log|set|send|include|reject)", c))
    gl = len(re.findall(r"^- \*\*[^*]+\*\*:", t, re.M))
    nm = bool(re.search(r"^\s*\d+\.\d+\s", t, re.M))
    return dict(reqs=len(re.findall(r"^### Requirement \d+", t, re.M)), crit=len(crit),
                when=pat["WHEN"], if_=pat["IF"], while_=pat["WHILE"], where=pat["WHERE"], ubiq=pat["UBIQ"],
                unwanted_pct=round(100 * pat["IF"] / max(len(crit), 1)), multi=multi, glossary=gl,
                numbering="N.M" if nm else "N", words=len(t.split()), open_q="## Open Questions" in t)

def design_stats(t):
    fences = re.findall(r"^```(\w*)", t, re.M)
    return dict(words=len(t.split()), props=len(re.findall(r"^#{3,4} Property \d+", t, re.M)),
                validates=len(re.findall(r"\*\*Validates:", t)), mermaid=fences.count("mermaid"),
                diff=fences.count("diff"), code=sum(1 for f in fences[::2] if f not in ("mermaid", "diff", "")),
                req_refs=len(re.findall(r"_Requirements?:", t)), h2=len(re.findall(r"^## ", t, re.M)),
                file_tree=bool(re.search(r"^## File/Folder Structure", t, re.M)))

def task_stats(t):
    leaves = re.findall(r"^\s+- \[(.)\](\*?)\s*(\d+\.\d+)\s+(.*)$", t, re.M)
    body = re.split(r"^\s+- \[.\]\*?\s*\d+\.\d+\s", t, flags=re.M)[1:]
    files = sum(1 for b in body if re.search(r"`[^`\s]+\.(ts|tsx|py|js|json|md|toml)`|`[^`\s]*/[^`\s]+`|Files:", b.split("\n- [")[0]))
    checks = len(re.findall(r"^- \[.\]\s*\d+\.\s*.*Checkpoint", t, re.M | re.I))
    m = re.search(r"```json\s*(\{.*?\})\s*```", t, re.S)
    waves, width, deps = 0, 0, False
    if m:
        g = json.loads(m.group(1)); ws = g.get("waves", [])
        waves = len(ws); width = max((len(w["tasks"]) for w in ws), default=0)
        deps = "deps" in m.group(1)
    return dict(words=len(t.split()), groups=len(re.findall(r"^- \[.\]\s*\d+\.\s", t, re.M)), leaves=len(leaves),
                optional=sum(1 for l in leaves if l[1] == "*"), names_files=files, checkpoints=checks,
                prop_leaves=len(re.findall(r"\*\*Property \d+", t)), waves=waves, max_width=width, deps=deps)

rows = []
for arg in sys.argv[1:]:
    label, d = arg.split("=", 1); d = Path(d)
    req = read(d, "requirements.md", "bugfix.md")
    rows.append((label, req_stats(req) if req else {}, design_stats(read(d, "design.md")), task_stats(read(d, "tasks.md", "task.md"))))

def table(title, idx, keys):
    print(f"\n### {title}\n\n| Spec | " + " | ".join(keys) + " |\n|---|" + "---|" * len(keys))
    for r in rows:
        s = r[idx]; print(f"| {r[0]} | " + " | ".join(str(s.get(k, "–")) for k in keys) + " |")

table("requirements", 1, ["reqs", "crit", "when", "if_", "while_", "where", "ubiq", "unwanted_pct", "multi", "glossary", "numbering", "open_q", "words"])
table("design", 2, ["h2", "props", "validates", "mermaid", "diff", "code", "req_refs", "file_tree", "words"])
table("tasks", 3, ["groups", "leaves", "optional", "names_files", "prop_leaves", "checkpoints", "waves", "max_width", "deps", "words"])
