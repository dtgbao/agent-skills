"""Validate tasks.md leaves and the Task Dependency Graph JSON (sdd shared/artifacts/tasks.md rules)."""

import json
import re
import sys
from pathlib import Path

TASKS = Path(sys.argv[1])
text = TASKS.read_text()

# Graph JSON: last ```json block.
blocks = re.findall(r"```json\n(.*?)```", text, re.S)
results = []


def check(name, ok, detail=""):
    results.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))


# 1. Graph JSON parses
try:
    graph = json.loads(blocks[-1])
    check("graph JSON parses", True)
except Exception as e:  # noqa: BLE001
    check("graph JSON parses", False, str(e))
    print("RESULT: FAIL")
    sys.exit(1)

# Leaves: '  - [ ]' or '  - [ ]*' with N.M id. Groups: '- [ ] N.'
leaf_re = re.compile(r"^  - \[[ x\-]\]\*? (\d+\.\d+) ")
group_re = re.compile(r"^- \[[ x\-]\] (\d+)\. ")
leaves = {}
current = None
for line in text.splitlines():
    m = leaf_re.match(line)
    if m:
        current = m.group(1)
        leaves[current] = {"lines": [line], "optional": "]*" in line.split(current)[0]}
        continue
    if group_re.match(line) or line.startswith("## "):
        current = None
        continue
    if current and line.startswith("    "):
        leaves[current]["lines"].append(line)
    elif current and line.strip() == "":
        pass

# Requirement citations per leaf
req_re = re.compile(r"_Requirements: ([0-9., ]+)_")
cited = set()
leaf_reqs = {}
for lid, info in leaves.items():
    body = "\n".join(info["lines"])
    m = req_re.search(body)
    reqs = [r.strip() for r in m.group(1).split(",")] if m else []
    leaf_reqs[lid] = reqs
    cited.update(reqs)

# Files named per leaf: backticked tokens ending in .py/.toml/.md
file_re = re.compile(r"`([\w/\.\-]+\.(?:py|toml|md|json))`")
leaf_files = {}
for lid, info in leaves.items():
    body = "\n".join(info["lines"])
    leaf_files[lid] = set(file_re.findall(body))

# 2. Each leaf in exactly one wave; graph ids are leaves only
wave_of = {}
dup = []
for w in graph["waves"]:
    for t in w["tasks"]:
        if t in wave_of:
            dup.append(t)
        wave_of[t] = w["id"]
check("every leaf in exactly one wave", not dup and set(wave_of) == set(leaves),
      f"dup={dup} missing={sorted(set(leaves) - set(wave_of))} extra={sorted(set(wave_of) - set(leaves))}")

# 3. Wave ids start at 0, contiguous
ids = [w["id"] for w in graph["waves"]]
check("wave ids start at 0 and are contiguous", ids == list(range(len(ids))), str(ids))

# 4. Same-wave leaves touch disjoint files
clashes = []
for w in graph["waves"]:
    seen = {}
    for t in w["tasks"]:
        for f in leaf_files.get(t, set()):
            if f in seen:
                clashes.append((w["id"], f, seen[f], t))
            seen[f] = t
check("same-wave leaves touch disjoint files", not clashes, str(clashes))

# 5. Every leaf names its files
nofile = [l for l in leaves if not leaf_files[l]]
check("every leaf names its files", not nofile, str(nofile))

# 6. Every criterion cited by >=1 leaf (criteria from requirements.md)
req_md = (TASKS.parent / "requirements.md").read_text()
criteria = set(re.findall(r"^(\d+\.\d+)\. WHEN|^(\d+\.\d+)\. IF|^(\d+\.\d+)\. THE", req_md, re.M))
criteria = {c for tup in criteria for c in tup if c}
uncited = sorted(criteria - cited, key=lambda s: tuple(map(int, s.split("."))))
check("every criterion cited by >=1 leaf", not uncited,
      f"criteria={len(criteria)} uncited={uncited}")

# 7. Property leaves carry Property and Validates lines
props = [l for l, info in leaves.items() if "**Property" in "\n".join(info["lines"])]
bad_props = [l for l in props if "**Validates: Requirements" not in "\n".join(leaves[l]["lines"])]
check("property leaves carry Validates line", not bad_props, f"props={props} bad={bad_props}")

# 8. Checkpoints not in graph
cp_in_graph = [t for t in wave_of if "Checkpoint" in t]
check("checkpoints not in graph", not cp_in_graph)

# 9. Info: wave table
print("\nWave table:")
for w in graph["waves"]:
    print(f"  wave {w['id']}: {', '.join(w['tasks'])}")

failed = [n for n, ok in results if not ok]
print("\nRESULT:", "PASS" if not failed else f"FAIL ({len(failed)} checks)")
