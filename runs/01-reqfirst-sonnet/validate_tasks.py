"""Validate tasks.md Task Dependency Graph. Usage: python validate_tasks.py <spec-dir>"""
import json, re, sys, pathlib

d = pathlib.Path(sys.argv[1])
text = (d / "tasks.md").read_text()
req = (d / "requirements.md").read_text()
ok = True
def check(name, cond, detail=""):
    global ok
    ok &= bool(cond)
    print(("PASS" if cond else "FAIL"), name, detail)

m = re.search(r"## Task Dependency Graph\s+```json\n(.*?)```", text, re.S)
check("graph is last section", m and text[m.end():].strip() == "")
graph = json.loads(m.group(1)); check("JSON parses", True)

# leaves: "  - [ ] N.M ..." or "  - [ ]* N.M ..."
leaves = {}
cur = None
for line in text.splitlines():
    lm = re.match(r"\s+- \[[ x-]\](\*?) (\d+\.\d+) (.*)", line)
    if lm:
        cur = lm.group(2)
        leaves[cur] = {"optional": bool(lm.group(1)), "title": lm.group(3), "files": [], "reqs": set()}
        continue
    if re.match(r"- \[", line): cur = None
    if cur:
        fm = re.search(r"Files?: (.*)", line)
        if fm: leaves[cur]["files"] = re.findall(r"`([^`]+)`", fm.group(1))
        rm = re.search(r"_Requirements: ([^_]+)_", line)
        if rm: leaves[cur]["reqs"] |= {x.strip() for x in rm.group(1).split(",")}
print("leaves:", sorted(leaves))

wave_of = {}
for w in graph["waves"]:
    for t in w["tasks"]:
        wave_of.setdefault(t, []).append(w["id"])
check("wave ids start at 0, consecutive", [w["id"] for w in graph["waves"]] == list(range(len(graph["waves"]))))
check("every leaf in exactly one wave", all(len(wave_of.get(l, [])) == 1 for l in leaves), str({l: wave_of.get(l) for l in leaves}))
check("no unknown/group ids in graph", set(wave_of) <= set(leaves), str(set(wave_of) - set(leaves)))
check("every leaf names files", all(v["files"] for v in leaves.values()))

for w in graph["waves"]:
    seen = {}
    for t in w["tasks"]:
        for f in leaves[t]["files"]:
            if f in seen: check(f"wave {w['id']} disjoint files", False, f"{f} in {seen[f]} and {t}")
            seen[f] = t
check("same-wave leaves disjoint files (all waves)", ok)

# test leaf after code leaf: tests/test_X.py covers shortlinks/X.py
bad = []
for t, v in leaves.items():
    for f in v["files"]:
        tm = re.match(r"tests/test_(\w+)\.py", f)
        if tm:
            code = f"shortlinks/{tm.group(1)}.py"
            for c, cv in leaves.items():
                if code in cv["files"] and wave_of[c][0] >= wave_of[t][0]:
                    bad.append((t, c))
check("test leaf after every code leaf it covers", not bad, str(bad))

# criteria coverage
crits = set()
n = None
for line in req.splitlines():
    rm = re.match(r"### Requirement (\d+):", line)
    if rm: n = rm.group(1)
    cm = re.match(r"(\d+)\. ", line)
    if cm and n and not line.startswith("- "): crits.add(f"{n}.{cm.group(1)}")
cited = set().union(*(v["reqs"] for v in leaves.values()))
check("every criterion cited by >=1 leaf", crits <= cited, f"missing={sorted(crits - cited)} total={len(crits)}")
print("RESULT:", "ALL PASS" if ok else "FAILURES")
