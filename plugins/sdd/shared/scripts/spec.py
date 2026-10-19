#!/usr/bin/env python3
"""sdd: spec state, plan checks and the script-driven TDD loop. Stdlib only.

State (main session)
  spec.py init <dir> <feature|bugfix>          create <dir>/.spec.json
  spec.py status <dir>                         phase states and the next command
  spec.py check <dir> [requirements]           validate spec.md (all, or the requirements only)
  spec.py approve <dir> <requirements|design>  store the section hash; design also stores the criteria baseline
  spec.py drift <dir>                          hand edits, changed criteria, affected cases, old values
  spec.py ready <dir>                          approved + no drift + check, then the lane waves to run
  spec.py verify <dir> [lane...]               lane results, full suite, coverage; ticks the plan
TDD loop (lane runner)
  spec.py tdd <dir> <lane>                     lane brief and the next step
  spec.py tdd <dir> <lane> run                 run the current case and print the next step
  spec.py tdd <dir> <lane> mutant <file> <old> <new>   prove a test that passed on its first run
  spec.py tdd <dir> <lane> report              3-line lane report
"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SELF = Path(__file__).resolve()
TEST_FILE = re.compile(r"(^|/)(tests?|__tests__)/|(^|/)test_[^/]*$|_test\.[^/]+$|\.(test|spec)\.[^/]+$")
SLICE_MAX = 3
MISSING = re.compile(
    r"ImportError|ModuleNotFoundError|NameError|SyntaxError|IndentationError|ERROR collecting"
    r"|AttributeError: (module|type object) '[^']+' has no attribute"
    r"|AttributeError: '(?!NoneType)\w+' object has no attribute"
    r"|TypeError: .*(unexpected keyword argument|positional argument|required (positional|keyword)"
    r"|takes (no|\d+) |object is not callable|object is not iterable|abstract)"
    r"|is not a function|is not defined|Cannot find module|does not provide an export|is not a constructor")


# ---------- parse ----------

def section(text, *names):
    """Body of the first `## <name>` section, up to the next `## `."""
    for name in names:
        m = re.search(rf"^## {name}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
        if m:
            return m.group(1)
    return ""


def sub(text, name):
    m = re.search(rf"^### {name}\s*$(.*?)(?=^### |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def ids(s):
    return [x for x in re.split(r"[,\s]+", s.strip()) if x]


def num(x):
    return [int(n) for n in x.split(".")]


def tok(case_id):
    """c1.1a -> c1_1a, P2 -> p2: the token in the test name."""
    return case_id.lower().replace(".", "_")


def parse(d):
    p = Path(d) / "spec.md"
    text = p.read_text() if p.exists() else ""
    req = section(text, "Requirements", "Bug")
    design = section(text, "Design")
    plan = section(text, "Plan")
    sp = {"text": text, "req": req, "design": design, "plan": plan, "criteria": {}, "props": {}, "lanes": {},
          "test": "", "suite": ""}
    if m := re.search(r"^Test:\s*`(.+)`\s*$", text, re.M):
        sp["test"] = m.group(1)
    if m := re.search(r"^Suite:\s*`(.+)`\s*$", text, re.M):
        sp["suite"] = m.group(1)
    for m in re.finditer(r"^- (\d+\.\d+)\s+(.+)$", req, re.M):
        sp["criteria"][m.group(1)] = m.group(2).strip()
    sp["open"] = [ln.strip() for ln in sub(req, "Open questions").splitlines() if ln.strip().startswith("-")
                  and not re.match(r"^-\s*none\b", ln.strip(), re.I)]
    for m in re.finditer(r"^- (P\d+)\s*\(([\d.,\s]+)\):\s*(.+)$", design, re.M):
        sp["props"][m.group(1)] = {"reqs": ids(m.group(2)), "text": m.group(3).strip()}
    for b in re.split(r"^### Lane ", plan, flags=re.M)[1:]:
        head, _, body = b.partition("\n")
        hm = re.match(r"([A-Z][A-Za-z0-9]*):\s*(.+)$", head.strip())
        if not hm:
            continue
        lid = hm.group(1)
        lane = {"id": lid, "title": hm.group(2), "files": [], "tier": None, "after": [], "slices": [], "bad": []}
        if m := re.search(r"^Files:\s*(.+)$", body, re.M):
            lane["files"] = re.findall(r"`([^`]+)`", m.group(1))
        if m := re.search(r"^Tier:\s*([SML])\b", body, re.M):
            lane["tier"] = m.group(1)
        if m := re.search(r"^After:\s*(.+)$", body, re.M):
            lane["after"] = [] if m.group(1).strip().lower() == "none" else ids(m.group(1))
        cur, cases = None, []
        for ln in body.splitlines():
            if m := re.match(r"^- \[([ x])\] ([A-Z][A-Za-z0-9]*?\d+) (.+?) · req ([\d.,\s]+?) · seam `([^`]+)`\s*$", ln):
                cases: list[dict] = []
                cur = {"id": m.group(2), "title": m.group(3), "reqs": ids(m.group(4)), "seam": m.group(5), "cases": cases}
                lane["slices"].append(cur)
            elif re.match(r"^- \[[ x]\] ", ln):
                cur = None
                lane["bad"].append(ln.strip())
            elif cur and (m := re.match(r"^\s+- (keep )?(c\d+\.\d+[a-z]?|P\d+):\s*(.*)$", ln)):
                cid = m.group(2)
                kind = "prop" if cid.startswith("P") else "keep" if m.group(1) else "case"
                crit = sp["props"].get(cid, {}).get("reqs", []) if kind == "prop" else [re.sub(r"[a-z]+$", "", cid[1:])]
                cases.append({"id": cid, "kind": kind, "text": m.group(3).strip(), "reqs": crit,
                                     "slice": cur["id"], "seam": cur["seam"]})
        sp["lanes"][lid] = lane
    return sp


def root_of(d):
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=d, capture_output=True, text=True)
    return Path(r.stdout.strip()) if r.returncode == 0 else Path(d).resolve().parents[2]


# ---------- state ----------

def spath(d):
    return Path(d) / ".spec.json"


def load(d):
    return json.loads(spath(d).read_text())


def save(d, s):
    spath(d).write_text(json.dumps(s, indent=2) + "\n")


def h(text):
    return hashlib.sha256(re.sub(r"^(\s*- )\[[ x]\]", r"\1[ ]", text, flags=re.M).encode()).hexdigest()


def hashes(sp):
    return {"requirements": h(sp["req"]), "design": h(sp["design"] + sp["plan"])}


def cmd_init(d, workflow):
    if workflow not in ("feature", "bugfix"):
        sys.exit("workflow must be feature or bugfix")
    Path(d).mkdir(parents=True, exist_ok=True)
    save(d, {"workflow": workflow, "phases": {"requirements": "pending", "design": "pending"},
             "hashes": {}, "baseline": {}})
    print(f"INIT {d} {workflow}")


def need(sp, s):
    """Criteria that need a case: all for a feature; Expected 2.x and Unchanged 3.x for a bugfix."""
    return {k for k in sp["criteria"] if s["workflow"] != "bugfix" or not k.startswith("1.")}


def waves(lanes):
    left, done, out = dict(lanes), set(), []
    while left:
        w = [k for k, v in left.items() if set(v["after"]) & set(left) == set()]
        if not w:
            return None
        out.append(sorted(w))
        done |= set(w)
        for k in w:
            del left[k]
    return out


def problems(d, only_req=False):
    s, sp = load(d), parse(d)
    out = []

    def bad(name, items):
        if items:
            out.append(f"{name}: {items}")

    if not sp["req"]:
        return ["no `## Requirements` (or `## Bug`) section in spec.md"]
    bad("no criteria (`- N.M <EARS text>`)", "" if sp["criteria"] else "none")
    bad("criterion needs exactly one SHALL", [k for k, v in sp["criteria"].items() if len(re.findall(r"\bSHALL\b", v)) != 1])
    if s["workflow"] == "bugfix":
        groups = {k.split(".")[0] for k in sp["criteria"]}
        bad("bugfix needs Current 1.x, Expected 2.x, Unchanged 3.x", sorted({"1", "2", "3"} - groups))
    bad("open questions remain", sp["open"])
    if only_req:
        return out
    if not sp["design"] or not sp["plan"]:
        return out + ["no `## Design` or `## Plan` section"]
    bad("`Test:` line with {target}", "" if "{target}" in sp["test"] else "missing")
    bad("`Suite:` line", "" if sp["suite"] else "missing")
    bad("property cites unknown criteria", [p for p, v in sp["props"].items() if set(v["reqs"]) - set(sp["criteria"])])
    lanes = sp["lanes"]
    bad("no lanes (`### Lane A: <title>`)", "" if lanes else "none")
    bad("plan line is not `- [ ] A1 <title> · req 1.1 · seam `<seam>``", [x for v in lanes.values() for x in v["bad"]])
    bad("lane needs Tier S|M|L", [k for k, v in lanes.items() if not v["tier"]])
    bad("lane After names unknown lane", [k for k, v in lanes.items() if set(v["after"]) - set(lanes)])
    bad("lane needs a test file and a code file", [k for k, v in lanes.items()
                                                    if not (any(TEST_FILE.search(f) for f in v["files"])
                                                            and any(not TEST_FILE.search(f) for f in v["files"]))])
    owner, clash = {}, []
    for k, v in lanes.items():
        for f in v["files"]:
            if f in owner:
                clash.append(f"{f}: {owner[f]} & {k}")
            owner[f] = k
    bad("lanes must own different files", clash)
    if waves(lanes) is None:
        out.append("lane After has a cycle")
    seen, cover = set(), {}
    for k, v in lanes.items():
        bad(f"lane {k} has no slices", "" if v["slices"] else "none")
        for sl in v["slices"]:
            bad(f"slice {sl['id']} id must start with lane id {k}", "" if sl["id"].startswith(k) else sl["id"])
            bad(f"slice {sl['id']} cites more than {SLICE_MAX} criteria", "" if len(sl["reqs"]) <= SLICE_MAX else sl["reqs"])
            bad(f"slice {sl['id']} cites unknown criteria", sorted(set(sl["reqs"]) - set(sp["criteria"])))
            got = set()
            for c in sl["cases"]:
                if c["id"] in seen:
                    out.append(f"case id used twice: {c['id']}")
                seen.add(c["id"])
                if c["kind"] == "prop" and c["id"] not in sp["props"]:
                    out.append(f"{c['id']} in {sl['id']} is not in Design ### Properties")
                for r in c["reqs"]:
                    got.add(r)
                    cover.setdefault(r, []).append(c["id"])
                if c["kind"] != "prop" and c["reqs"][0] not in sl["reqs"]:
                    out.append(f"case {c['id']} cites {c['reqs'][0]}, which slice {sl['id']} does not cite")
                if c["kind"] == "keep" and not c["reqs"][0].startswith("3."):
                    out.append(f"keep case {c['id']} must cite an Unchanged 3.x criterion")
            bad(f"slice {sl['id']} criteria with no case", sorted(set(sl["reqs"]) - got))
    bad("criteria with no case or property", sorted(need(sp, s) - set(cover), key=num))
    bad("properties in no slice", sorted(set(sp["props"]) - seen))
    return out


def cmd_check(d, what=""):
    errs = problems(d, only_req=what == "requirements")
    for e in errs:
        print(f"FAIL {e}")
    print("RESULT: FAIL" if errs else "RESULT: PASS")
    sys.exit(1 if errs else 0)


def cmd_approve(d, *phases):
    s, sp = load(d), parse(d)
    for p in phases:
        if p not in ("requirements", "design"):
            sys.exit("phase must be requirements or design")
        errs = problems(d, only_req=p == "requirements")
        if errs:
            sys.exit("REFUSED: " + "; ".join(errs))
        now = hashes(sp)[p]
        if p == "design" and s["hashes"].get("requirements") != hashes(sp)["requirements"]:
            old = s.get("req_criteria", {})
            diff = sorted({k for k in set(old) | set(sp["criteria"]) if old.get(k) != sp["criteria"].get(k)}, key=num)
            sys.exit(f"REFUSED: the Requirements changed after gate 1 (criteria {', '.join(diff) or 'text'}). "
                     "Show the change to the user and approve requirements again, or undo it.")
        if p == "requirements" and s["phases"]["design"] == "approved" and s["hashes"].get("requirements") != now:
            s["phases"]["design"] = "stale"
            print("STALE design")
        s["phases"][p] = "approved"
        s["hashes"][p] = now
        if p == "requirements":
            s["req_criteria"] = sp["criteria"]
        if p == "design":
            s["baseline"] = sp["criteria"]
        print(f"APPROVED {p}")
    save(d, s)


def drift(d):
    """Lines; does not change state."""
    s, sp = load(d), parse(d)
    lines = []
    now = hashes(sp)
    for p in ("requirements", "design"):
        if s["phases"][p] in ("approved", "stale") and s["hashes"].get(p) != now[p]:
            lines.append(f"DRIFT {p}")
        if s["phases"][p] == "stale":
            lines.append(f"STALE {p}")
    base = s.get("baseline") or {}
    if not base:
        return lines
    cases = {c["id"]: (lid, c) for lid, ln in sp["lanes"].items() for sl in ln["slices"] for c in sl["cases"]}
    root = root_of(d)
    for k in sorted(set(base) | set(sp["criteria"]), key=num):
        old, new = base.get(k), sp["criteria"].get(k)
        tag = "ADDED" if old is None else "REMOVED" if new is None else "CHANGED" if old != new else ""
        if not tag:
            continue
        lines.append(f"{tag} {k}")
        hit = [cid for cid, (_, c) in cases.items() if k in c["reqs"]]
        if hit:
            lines.append(f"AFFECTS {k} -> {' '.join(hit)}")
        if tag == "CHANGED" and old and new:
            gone = {g for g in set(re.findall(r"\d+", old)) - set(re.findall(r"\d+", new)) if int(g) > 1}
            if gone:
                pat = re.compile(r"(?<!\d)(?<!\d\.)(" + "|".join(sorted(gone)) + r")(?!\d)(?!\.\d)")
                for ok, ov in sp["criteria"].items():
                    if ok != k and pat.search(ov):
                        lines.append(f"OLD VALUE {k} -> criterion {ok}: {ov[:80]}")
                for no, line in enumerate((sp["design"] + sp["plan"]).splitlines(), 1):
                    if pat.search(line) and not re.match(r"^\s+- (keep )?c\d", line):
                        lines.append(f"OLD VALUE {k} -> spec.md Design/Plan: {line.strip()[:80]}")
                for lid in sorted({cases[c][0] for c in hit}):
                    for f in sp["lanes"][lid]["files"]:
                        fp = root / f
                        if fp.is_file():
                            for no, line in enumerate(fp.read_text(errors="ignore").splitlines(), 1):
                                if pat.search(line):
                                    lines.append(f"OLD VALUE {k} -> {f}:{no}: {line.strip()[:80]}")
    return lines


def cmd_drift(d):
    lines = drift(d)
    print("\n".join(lines) if lines else "NO DRIFT")


def cmd_status(d):
    s = load(d)
    print(f"WORKFLOW {s['workflow']}")
    for p, v in s["phases"].items():
        print(f"{p}: {v}")
    lines = drift(d) if s["phases"]["design"] != "pending" else []
    if lines:
        print("\n".join(lines))
        print("NEXT: /sdd:spec-sync")
    elif s["phases"]["requirements"] != "approved":
        print("NEXT: requirements gate (spec-new)")
    elif s["phases"]["design"] != "approved":
        print("NEXT: design gate (spec-new)")
    else:
        todo = sum(open_cases(d).values())
        print(f"NEXT: /sdd:spec-run ({todo} open cases)" if todo else "NEXT: done")


# ---------- lane run state ----------

def rdir(d):
    p = Path(d) / ".run"
    p.mkdir(exist_ok=True)
    return p


def lane_cases(sp, lane):
    return [c for sl in sp["lanes"][lane]["slices"] for c in sl["cases"]]


def case_hash(sp, c):
    crit = " ".join(sp["criteria"].get(r, "") for r in c["reqs"])
    prop = sp["props"].get(c["id"], {}).get("text", "")
    return hashlib.sha256(f"{c['text']}|{crit}|{prop}".encode()).hexdigest()[:16]


def lane_state(d, sp, lane):
    """Load the run state. A case whose text or criteria changed goes back to todo (prior: its test exists)."""
    p = rdir(d) / f"{lane}.json"
    old = json.loads(p.read_text()) if p.exists() else {}
    st = {"cases": {}}
    for c in lane_cases(sp, lane):
        hc = case_hash(sp, c)
        o = old.get("cases", {}).get(c["id"])
        if o and o["hash"] == hc:
            st["cases"][c["id"]] = o
        else:
            st["cases"][c["id"]] = {"hash": hc, "status": "todo", "prior": bool(o), "old_src": (o or {}).get("src")}
    p.write_text(json.dumps(st, indent=1))
    return st


def save_lane(d, lane, st):
    (rdir(d) / f"{lane}.json").write_text(json.dumps(st, indent=1))


def log(d, lane, msg):
    with open(rdir(d) / f"{lane}.log", "a") as f:
        f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")


def open_cases(d):
    sp = parse(d)
    return {lane: sum(1 for v in lane_state(d, sp, lane)["cases"].values() if v["status"] != "done") for lane in sp["lanes"]}


def current(sp, st, lane):
    return next((c for c in lane_cases(sp, lane) if st["cases"][c["id"]]["status"] != "done"), None)


def test_files(sp, lane):
    return [f for f in sp["lanes"][lane]["files"] if TEST_FILE.search(f)]


def code_files(sp, lane):
    return [f for f in sp["lanes"][lane]["files"] if not TEST_FILE.search(f)]


def find_tests(root, files, token):
    """[(file, name)] of tests whose name holds the token (python def, or js it/test)."""
    out = []
    for f in files:
        p = root / f
        if not p.is_file():
            continue
        t = p.read_text(errors="ignore")
        for m in re.finditer(rf"^\s*(?:async\s+)?def (test_{token}(?:_\w*)?)\s*\(", t, re.M):
            out.append((f, m.group(1)))
        for m in re.finditer(rf"""\b(?:it|test)\(\s*['"`]((?:test_)?{token}\b[^'"`]*)['"`]""", t):
            out.append((f, m.group(1)))
    return out


def target(cmd, files, name=None):
    if name is None:
        return cmd.replace("{target}", files)
    if "pytest" in cmd:
        return cmd.replace("{target}", f"{files}::{name}")
    if "vitest" in cmd or "jest" in cmd:
        return cmd.replace("{target}", f'{files} -t "{name}"')
    return cmd.replace("{target}", files)


def run(cmd, cwd):
    try:
        r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=900)
        return r.returncode, r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT after 900 s"


def classify(rc, out):
    """pass | red | missing | counterexample | notfound, and the line that shows it."""
    if rc == 0:
        return "pass", ""
    lines = out.splitlines()
    if "Falsifying example" in out:
        fx = [ln.strip() for ln in lines if "Falsifying example" in ln or re.match(r"^\s+\w+=", ln)]
        return "counterexample", " ".join(fx)[:400]
    if re.search(r"no tests ran|ERROR: not found|No test files found|no tests to run", out, re.I):
        return "notfound", ""
    if "DID NOT RAISE" in out:
        return "red", next(ln for ln in lines if "DID NOT RAISE" in ln).strip()[:200]
    elines = [ln.strip() for ln in lines if re.match(r"^E\s", ln)]
    first = next((ln for ln in elines if re.search(r"Error|Exception|assert|Failed", ln)), "")
    m = MISSING.search(first) if first else MISSING.search(out[:4000])
    if m:
        return "missing", (first or next((ln.strip() for ln in lines if m.group(0) in ln), m.group(0)))[:200]
    if not first:
        first = next((ln.strip() for ln in lines if re.search(r"Error|assert|Expected|Received", ln)), "")
    return "red", (first or (lines[-1] if lines else "fail"))[:200]


# ---------- tdd ----------

def tdd_cmd(d, lane, verb=""):
    return f"python3 {SELF} tdd {d} {lane} {verb}".strip()


def step_text(d, sp, st, lane):
    c = current(sp, st, lane)
    if c is None:
        return f"LANE DONE. Run: {tdd_cmd(d, lane, 'report')}\nThen reply with its output and STATUS: done."
    cs = st["cases"][c["id"]]
    crit = "\n".join(f"  criterion {r}: {sp['criteria'].get(r, '?')}" for r in c["reqs"])
    head = f"NEXT {c['id']} (slice {c['slice']}, seam `{c['seam']}`)\n{crit}\n  case: {c['text']}"
    if c["kind"] == "prop":
        head += f"\n  property: {sp['props'][c['id']]['text']}"
    if cs.get("phase") == "code":
        return (f"{head}\nRED is recorded: {cs.get('red', '')}\n"
                f"DO, in ONE message: (1) edit {', '.join(code_files(sp, lane))}: the minimum code that makes this test "
                f"pass, and no code for other cases; (2) run: {tdd_cmd(d, lane, 'run')}")
    if cs.get("nored"):
        return (f"{head}\nThe test passed on its first run. Prove that it checks the behavior. Run:\n"
                f"{tdd_cmd(d, lane, 'mutant')} <code file> '<exact old text>' '<new text>'\n"
                "The new text must break the behavior of this case, for example `<` to `<=`, or a changed constant. "
                f"The script changes a temp copy only. If the test is wrong, fix the test and run: {tdd_cmd(d, lane, 'run')}")
    what = {"case": "Use the literal values of the case; for several values, use one parametrized test. Call only the seam.",
            "keep": "This case pins behavior that must NOT change. It must pass on the current code.",
            "prop": "Write a property test with 100 or more examples. The generator bounds and the oracle come from "
                    f"the property text, as literal values. Put the comment `# {c['id']}` above it."}[c["kind"]]
    verb = "Change the existing" if cs.get("prior") else "Write ONE"
    return (f"{head}\nDO, in ONE message: (1) {verb} test named `test_{tok(c['id'])}_<few_words>` in "
            f"{', '.join(test_files(sp, lane))}. {what} Write no other test. (2) run: {tdd_cmd(d, lane, 'run')}")


def brief(d, sp, st, lane):
    ln = sp["lanes"][lane]
    reqs = sorted({r for c in lane_cases(sp, lane) for r in c["reqs"]}, key=num)
    props = [c["id"] for c in lane_cases(sp, lane) if c["kind"] == "prop"]
    done = sum(1 for v in st["cases"].values() if v["status"] == "done")
    parts = [f"LANE {lane}: {ln['title']}",
             f"WRITE ONLY: {', '.join(ln['files'])}",
             "INTERFACES:\n" + (sub(sp["design"], "Interfaces") or "none"),
             "ERRORS:\n" + (sub(sp["design"], "Errors") or "none"),
             "CRITERIA:\n" + "\n".join(f"- {r} {sp['criteria'].get(r, '?')}" for r in reqs)]
    if props:
        parts.append("PROPERTIES:\n" + "\n".join(f"- {p} {sp['props'][p]['text']}" for p in props))
    parts.append(f"PROGRESS: {done}/{len(st['cases'])} done")
    parts.append(step_text(d, sp, st, lane))
    return "\n\n".join(parts)


def later_tests(root, sp, st, lane, cur):
    out = []
    for c in lane_cases(sp, lane):
        cs = st["cases"][c["id"]]
        if c["id"] != cur["id"] and cs["status"] != "done" and not cs.get("prior"):
            out += [n for _, n in find_tests(root, test_files(sp, lane), tok(c["id"]))]
    return out


def test_src(root, f, n):
    """Hash of the test's source (decorators + body), to see if a reopened case changed its test."""
    lines = (root / f).read_text(errors="ignore").splitlines()
    i = next((k for k, ln in enumerate(lines) if re.search(rf"\b{re.escape(n)}\b", ln)), None)
    if i is None:
        return ""
    a = i
    while a > 0 and lines[a - 1].strip().startswith(("@", "#")):
        a -= 1
    b = i + 1
    while b < len(lines) and (not lines[b].strip() or lines[b][:1].isspace()):
        b += 1
    return hashlib.sha256("\n".join(ln.rstrip() for ln in lines[a:b] if ln.strip()).encode()).hexdigest()[:16]


def done(d, lane, st, cs, cid, root, f, n, **kw):
    cs.update(status="done", phase=None, nored=False, src=test_src(root, f, n), **kw)
    save_lane(d, lane, st)


def lane_target(root, sp, st, lane, cur):
    """The lane test files, without the tests of open cases (they can be stale until their turn)."""
    files = " ".join(test_files(sp, lane))
    if "pytest" not in sp["test"]:
        return target(sp["test"], files)
    skip = [f"--deselect {f}::{n}" for c in lane_cases(sp, lane)
            if c["id"] != cur["id"] and st["cases"][c["id"]]["status"] != "done"
            for f, n in find_tests(root, test_files(sp, lane), tok(c["id"]))]
    return target(sp["test"], " ".join([files] + skip))


OPS = [(r"(?<![<>=!])<=", "<"), (r"(?<![<>=!-])>=", ">"), (r"(?<![<>=!])<(?![<=])", "<="),
       (r"(?<![<>=!-])>(?![>=])", ">="), (r"==", "!="), (r"!=", "=="), (r" and ", " or "), (r" or ", " and "),
       (r"\bTrue\b", "False"), (r"\bFalse\b", "True"), (r" \+ ", " - "), (r" - ", " + "), (r"//", "/")]


def mutants(root, files):
    """(file, line no, old line, new line): changed lines first (git diff), then the rest."""
    out, rest = [], []
    for f in files:
        p = root / f
        if not p.is_file():
            continue
        lines = p.read_text().splitlines()
        r = subprocess.run(["git", "diff", "-U0", "HEAD", "--", f], cwd=root, capture_output=True, text=True)
        changed = {int(m.group(1)) + i for m in re.finditer(r"^@@ .*\+(\d+)(?:,(\d+))? @@", r.stdout, re.M)
                   for i in range(int(m.group(2) or 1))}
        if not r.stdout:
            changed = set(range(1, len(lines) + 1))
        for no, ln in enumerate(lines, 1):
            body = ln.strip()
            if not body or body.startswith(("#", "import ", "from ", "def ", "class ", "@", '"""')):
                continue
            cands = [(f, no, ln, re.sub(pat, new, ln, count=1)) for pat, new in OPS if re.search(pat, ln)]
            cands += [(f, no, ln, ln[:m.start()] + str(int(m.group()) + 1) + ln[m.end():])
                      for m in list(re.finditer(r"(?<![\w.])\d+(?![\w.])", ln))[:2]]
            (out if no in changed else rest).extend(cands)
    return out + rest


def auto_mutant(root, sp, lane, f, n, budget=15, seconds=15):
    """Try simple mutants on a temp copy; return 'file:line old -> new (fail line)' for the first one that the test kills."""
    tmp = Path(tempfile.mkdtemp(prefix="sdd-mutant-"))
    start = time.time()
    try:
        dst = tmp / "repo"
        shutil.copytree(root, dst, ignore=shutil.ignore_patterns(".git", ".venv", "node_modules", "__pycache__",
                                                                 ".hypothesis", ".pytest_cache", ".run"))
        for i, (file, no, old, new) in enumerate(mutants(root, code_files(sp, lane))):
            if i >= budget or time.time() - start > seconds:
                break
            orig = (dst / file).read_text()
            lines = orig.splitlines(keepends=True)
            lines[no - 1] = new + ("\n" if lines[no - 1].endswith("\n") else "")
            (dst / file).write_text("".join(lines))
            res, line = classify(*run(target(sp["test"], f, n), dst))
            (dst / file).write_text(orig)
            if res in ("red", "counterexample"):
                return f"{file}:{no} `{old.strip()}` -> `{new.strip()}` ({line})"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return None


def tdd_run(d, sp, st, lane):
    root = root_of(d)
    c = current(sp, st, lane)
    if c is None:
        return step_text(d, sp, st, lane)
    cs = st["cases"][c["id"]]
    again = f"Then run: {tdd_cmd(d, lane, 'run')}"
    extra = later_tests(root, sp, st, lane, c)
    if extra:
        return f"STOP: {', '.join(extra)} test later cases. Delete them. Write one test at a time.\n{again}"
    found = find_tests(root, test_files(sp, lane), tok(c["id"]))
    if not found:
        return f"NO TEST for {c['id']} in {', '.join(test_files(sp, lane))}.\n" + step_text(d, sp, st, lane)
    if len(found) > 1:
        return f"STOP: {len(found)} tests for {c['id']}: {[n for _, n in found]}. Keep ONE.\n{again}"
    f, n = found[0]
    if cs.get("prior") and cs.get("old_src") and cs.get("phase") != "code" and test_src(root, f, n) == cs["old_src"]:
        return (f"UNCHANGED: `{n}` is the old test. The case or its criterion changed, so change the test to match "
                f"the case first.\n{again}")
    res, line = classify(*run(target(sp["test"], f, n), root))
    if res == "counterexample":
        cs.update(status="counterexample", cx=line)
        save_lane(d, lane, st)
        log(d, lane, f"{c['id']} counterexample {line}")
        return f"COUNTEREXAMPLE in {n}: {line}\nSTOP. Change no code and no test. Reply with STATUS: failed and this line."
    if res == "notfound":
        return f"The test command found no test `{n}` in {f}. Check the name and the file.\n{again}"
    if cs.get("phase") != "code":
        if c["kind"] == "keep":
            if res == "pass":
                done(d, lane, st, cs, c["id"], root, f, n, how="keep")
                log(d, lane, f"{c['id']} keep pass")
                return f"KEEP OK {c['id']}.\n" + step_text(d, sp, st, lane)
            return f"KEEP FAILS on the current code: {line}\nReply with STATUS: blocked and this line."
        if res == "pass":
            killed = auto_mutant(root, sp, lane, f, n)
            if killed:
                done(d, lane, st, cs, c["id"], root, f, n, how="no-red", mutant=killed)
                log(d, lane, f"{c['id']} no-red, auto mutant killed {killed}")
                return (f"NO-RED {c['id']}: the test passed at once, and it kills the mutant {killed}. Done.\n" + step_text(d, sp, st, lane))
            cs["nored"] = True
            save_lane(d, lane, st)
            return "NO-RED and no automatic mutant failed the test.\n" + step_text(d, sp, st, lane)
        if res == "missing":
            return (f"MISSING NAME: {line}\nThis is not a red: a name is missing, not the behavior. Add the smallest "
                    f"stub in {', '.join(code_files(sp, lane))}: the name only, with no behavior.\n{again}")
        cs.update(phase="code", red=line, nored=False)
        save_lane(d, lane, st)
        log(d, lane, f"{c['id']} red {line}")
        return step_text(d, sp, st, lane)
    if res != "pass":
        return f"STILL RED: {line}\nChange the code, not the test.\n{again}"
    last = [x for x in lane_cases(sp, lane) if x["slice"] == c["slice"]][-1]["id"] == c["id"]
    rc2, out2 = run(lane_target(root, sp, st, lane, c), root) if last else (0, "")
    if rc2 != 0:
        tail = "\n".join(out2.strip().splitlines()[-8:])
        return f"GREEN for {n}, but other tests of the lane fail:\n{tail}\nFix the code, not the other tests.\n{again}"
    done(d, lane, st, cs, c["id"], root, f, n, how="red-green")
    log(d, lane, f"{c['id']} green")
    return f"GREEN {c['id']}.\n" + step_text(d, sp, st, lane)


def tdd_mutant(d, sp, st, lane, file, old, new):
    root = root_of(d)
    c = current(sp, st, lane)
    if c is None or not st["cases"][c["id"]].get("nored"):
        return "No mutant is needed now.\n" + step_text(d, sp, st, lane)
    if file not in code_files(sp, lane):
        return f"Change a code file of this lane: {', '.join(code_files(sp, lane))}. Not a test file."
    text = (root / file).read_text()
    if old not in text:
        return f"`{old}` is not in {file}. Copy the old text exactly."
    found = find_tests(root, test_files(sp, lane), tok(c["id"]))
    if len(found) != 1:
        return f"Need exactly one test for {c['id']}. Run: {tdd_cmd(d, lane, 'run')}"
    f, n = found[0]
    tmp = Path(tempfile.mkdtemp(prefix="sdd-mutant-"))
    try:
        dst = tmp / "repo"
        shutil.copytree(root, dst, ignore=shutil.ignore_patterns(".git", ".venv", "node_modules", "__pycache__",
                                                                 ".hypothesis", ".pytest_cache", ".run"))
        (dst / file).write_text(text.replace(old, new, 1))
        res, line = classify(*run(target(sp["test"], f, n), dst))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if res == "pass":
        return (f"MUTANT SURVIVED: {n} still passes with `{old}` -> `{new}`. The test does not see this change. "
                f"Make the test check the behavior of the case, or change code that the case needs.\n"
                f"Then run: {tdd_cmd(d, lane, 'run')}")
    if res == "missing":
        return f"MUTANT INVALID: {line}. Change behavior (an operator or a value), not a name."
    done(d, lane, st, st["cases"][c["id"]], c["id"], root, f, n, how="no-red", mutant=f"{file}: {old} -> {new}")
    log(d, lane, f"{c['id']} no-red, mutant killed {file}: {old} -> {new} ({line})")
    return f"MUTANT KILLED ({line}). {c['id']} is done.\n" + step_text(d, sp, st, lane)


def tdd_report(d, sp, st, lane):
    vals = list(st["cases"].values())
    cnt = {k: sum(1 for v in vals if v.get("how") == k) for k in ("red-green", "no-red", "keep")}
    done = sum(1 for v in vals if v["status"] == "done")
    rc, out = run(target(sp["test"], " ".join(test_files(sp, lane))), root_of(d))
    last = out.strip().splitlines()[-1] if out.strip() else ""
    open_ = [f"{k} ({v['status']})" for k, v in st["cases"].items() if v["status"] != "done"]
    return (f"LANE {lane}: {done}/{len(vals)} done · red-green {cnt['red-green']} · no-red {cnt['no-red']} · keep {cnt['keep']}\n"
            f"TESTS: {last}\nOPEN: {', '.join(open_) or 'none'}")


def cmd_tdd(d, lane, verb="", *args):
    sp = parse(d)
    if lane not in sp["lanes"]:
        sys.exit(f"no lane {lane}; lanes: {', '.join(sp['lanes'])}")
    st = lane_state(d, sp, lane)
    if verb == "":
        print(brief(d, sp, st, lane))
    elif verb == "run":
        print(tdd_run(d, sp, st, lane))
    elif verb == "mutant" and len(args) == 3:
        print(tdd_mutant(d, sp, st, lane, *args))
    elif verb == "report":
        print(tdd_report(d, sp, st, lane))
    else:
        sys.exit(__doc__)


# ---------- orchestrator ----------

def sync_ticks(d, sp):
    p = Path(d) / "spec.md"
    text = p.read_text()
    for lane in sp["lanes"]:
        st = lane_state(d, sp, lane)
        for sl in sp["lanes"][lane]["slices"]:
            done = all(st["cases"][c["id"]]["status"] == "done" for c in sl["cases"])
            text = re.sub(rf"^- \[[ x]\] {re.escape(sl['id'])} ", f"- [{'x' if done else ' '}] {sl['id']} ", text, flags=re.M)
    p.write_text(text)


def cmd_ready(d):
    s = load(d)
    bad = [p for p, v in s["phases"].items() if v != "approved"]
    if bad:
        sys.exit(f"NOT READY: not approved: {', '.join(bad)}. Run /sdd:spec-new <name> to resume.")
    lines = drift(d)
    if lines:
        sys.exit("NOT READY: drift\n" + "\n".join(lines) + "\nRun /sdd:spec-sync <name>.")
    errs = problems(d)
    if errs:
        sys.exit("NOT READY: check fails\n" + "\n".join(errs))
    sp = parse(d)
    todo = open_cases(d)
    sync_ticks(d, sp)
    lanes = {k: v for k, v in sp["lanes"].items() if todo[k]}
    if not lanes:
        print("NOTHING TO RUN: all cases are done.")
        return
    print("READY")
    for i, w in enumerate(waves(lanes) or []):
        print(f"WAVE {i}: " + " ".join(f"{k}(tier {sp['lanes'][k]['tier']}, {todo[k]} open)" for k in w))


def cmd_verify(d, *lanes):
    s, sp = load(d), parse(d)
    root = root_of(d)
    ok = True
    for lane in lanes or tuple(sp["lanes"]):
        st = lane_state(d, sp, lane)
        open_ = [k for k, v in st["cases"].items() if v["status"] != "done"]
        cx = [f"{k}: {v.get('cx', '')}" for k, v in st["cases"].items() if v["status"] == "counterexample"]
        gone = [k for k, v in st["cases"].items() if v["status"] == "done"
                and not find_tests(root, test_files(sp, lane), tok(k))]
        if cx:
            print(f"LANE {lane}: COUNTEREXAMPLE {'; '.join(cx)}")
        elif open_ or gone:
            print(f"LANE {lane}: OPEN {', '.join(open_)}" + (f" · TEST MISSING {', '.join(gone)}" if gone else ""))
        else:
            print(f"LANE {lane}: DONE {len(st['cases'])} cases")
        ok = ok and not (open_ or gone or cx)
    rc, out = run(sp["suite"], root)
    last = out.strip().splitlines()[-1] if out.strip() else ""
    print(f"SUITE: {'PASS' if rc == 0 else 'FAIL'} {last}")
    if rc != 0:
        ok = False
        for ln in out.splitlines():
            if m := re.match(r"^(FAILED|ERROR) (\S+)", ln):
                t = m.group(2)
                owner = next((k for k, v in sp["lanes"].items() if any(t.startswith(f) for f in v["files"])), "none")
                print(f"  {m.group(1)} {t} (lane {owner})")
    done = {k for lane in sp["lanes"] for k, v in lane_state(d, sp, lane)["cases"].items() if v["status"] == "done"}
    cover = {r for lane in sp["lanes"] for c in lane_cases(sp, lane) if c["id"] in done for r in c["reqs"]}
    want = need(sp, s)
    miss = sorted(want - cover, key=num)
    print(f"COVERAGE: {len(want) - len(miss)}/{len(want)} criteria" + (f" · open {', '.join(miss)}" if miss else ""))
    sync_ticks(d, sp)
    print("RESULT: PASS" if ok and not miss else "RESULT: FAIL")


CMDS = {"init": cmd_init, "status": cmd_status, "check": cmd_check, "approve": cmd_approve, "drift": cmd_drift,
        "ready": cmd_ready, "verify": cmd_verify, "tdd": cmd_tdd}

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in CMDS:
        sys.exit(__doc__)
    CMDS[sys.argv[1]](*sys.argv[2:])
