"""Validate tasks.md '## Task Dependency Graph' against the wave rules in shared/artifacts/tasks.md.

Usage: python3 -I validate_tasks.py <spec_dir>
Reads <spec_dir>/tasks.md and <spec_dir>/requirements.md.
"""

import json
import pathlib
import re
import sys

spec = pathlib.Path(sys.argv[1])
tasks_text = (spec / "tasks.md").read_text()
req_text = (spec / "requirements.md").read_text()
errors = []

# 1. Parse leaves (indent 2, '- [ ]' or '- [ ]*') and their bodies (indent 4+).
leaves = {}
group = None
cur = None
for line in tasks_text.splitlines():
    m = re.match(r"^- \[[ x\-]\] (\d+)\. ", line)
    if m:
        group, cur = m.group(1), None
        continue
    m = re.match(r"^  - \[[ x\-]\](\*?) (\d+\.\d+) ", line)
    if m:
        cur = m.group(2)
        leaves[cur] = {"optional": bool(m.group(1)), "group": group, "text": line}
        continue
    if cur and line.startswith("    "):
        leaves[cur]["text"] += "\n" + line
    elif re.match(r"^(## |- \[|  - \[)", line):
        cur = None

# 2. Parse graph JSON.
m = re.search(r"## Task Dependency Graph.*?```json\n(.*?)```", tasks_text, re.S)
if not m:
    errors.append("no json block under '## Task Dependency Graph'")
    graph = {"waves": []}
else:
    try:
        graph = json.loads(m.group(1))
        print("JSON parses: OK")
    except json.JSONDecodeError as e:
        errors.append(f"JSON does not parse: {e}")
        graph = {"waves": []}

# 3. Each leaf in exactly one wave; no unknown ids.
where = {}
for w in graph["waves"]:
    for t in w["tasks"]:
        where.setdefault(t, []).append(w["id"])
for lid in leaves:
    n = len(where.get(lid, []))
    if n != 1:
        errors.append(f"leaf {lid} appears in {n} waves (want 1)")
for t in where:
    if t not in leaves:
        errors.append(f"graph names unknown leaf {t}")
print(f"Leaves: {len(leaves)} · Waves: {len(graph['waves'])}")
print("Each leaf in exactly one wave: " + ("OK" if not any("appears" in e for e in errors) else "FAIL"))

# 4. Same-wave leaves touch disjoint files. Files = backticked *.py / *.toml paths.
def files_of(lid):
    return set(re.findall(r"`([\w./-]+\.(?:py|toml))`", leaves[lid]["text"]))

for lid in leaves:
    if not files_of(lid):
        errors.append(f"leaf {lid} names no files")
wave_ok = True
for w in graph["waves"]:
    ids = [t for t in w["tasks"] if t in leaves]
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            shared = files_of(a) & files_of(b)
            if shared:
                wave_ok = False
                errors.append(f"wave {w['id']}: {a} and {b} share {sorted(shared)}")
print("Same-wave leaves disjoint: " + ("OK" if wave_ok else "FAIL"))

# 5. Optional test leaf sits in a later wave than every non-optional leaf of its group.
test_ok = True
for lid, info in leaves.items():
    if not info["optional"] or lid not in where:
        continue
    code = [where[c][0] for c, i in leaves.items()
            if i["group"] == info["group"] and not i["optional"] and c in where]
    if code and where[lid][0] <= max(code):
        test_ok = False
        errors.append(f"test leaf {lid} (wave {where[lid][0]}) is not after its code leaves {code}")
print("Test leaves after code leaves: " + ("OK" if test_ok else "FAIL"))

# 6. Every criterion cited by at least one leaf (criteria numbered in requirements.md).
criteria = set()
for m in re.finditer(r"^(\d+)\. (?:WHEN|IF|THE|WHILE)", req_text, re.M):
    criteria.add(f"1.{m.group(1)}")
cited = set()
for info in leaves.values():
    for seg in re.findall(r"Requirements:? ([^\n]*)", info["text"]):
        cited.update(re.findall(r"\b\d+\.\d+\b", seg))
missing = sorted(criteria - cited)
print(f"Criteria {len(criteria)} · cited {len(criteria & cited)} · uncited {missing or 'none'}")
if missing:
    errors.append(f"uncited criteria: {missing}")

print()
print("RESULT: " + ("PASS" if not errors else "FAIL"))
for e in errors:
    print("  - " + e)
