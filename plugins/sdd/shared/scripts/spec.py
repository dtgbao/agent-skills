#!/usr/bin/env python3
"""sdd spec state + tasks checker. Stdlib only.

  spec.py init <dir> <workflow>        create dir + .spec.json
  spec.py draft <dir> <phase>...       phase -> draft
  spec.py approve <dir> <phase>...     phase -> approved, store hash; tasks also stores criteria baseline
  spec.py edited <dir> <phase>         approved file edited: store hash, later phases -> stale
  spec.py drift <dir>                  detect hand edits (DRIFT) and criterion text changes (CHANGED/ADDED/REMOVED)
  spec.py check-tasks <dir>            validate tasks.md against shared/artifacts/tasks.md rules
"""
import hashlib
import json
import re
import sys
from pathlib import Path

WORKFLOWS = ("requirements-first", "design-first", "bugfix", "quick-plan")
PHASES = ("requirements", "design", "tasks")
KINDS = ("setup", "slice", "test", "pin", "fix")
TEST_FILE = re.compile(r"(^|/)(tests?|__tests__)/|(^|/)test_[^/]*$|_test\.[^/]+$|\.(test|spec)\.[^/]+$")
SLICE_MAX_FILES = 5
SLICE_MAX_CRITERIA = 3


def state_path(d):
    return Path(d) / ".spec.json"


def load(d):
    return json.loads(state_path(d).read_text())


def save(d, s):
    state_path(d).write_text(json.dumps(s, indent=2) + "\n")


def phase_file(d, s, phase):
    if phase == "requirements":
        return Path(d) / ("bugfix.md" if s["workflow"] == "bugfix" else "requirements.md")
    return Path(d) / f"{phase}.md"


def sha(p):
    """tasks.md: checkbox marks normalized, so spec-run ticks are not drift."""
    if not p.exists():
        return ""
    text = p.read_text()
    if p.name == "tasks.md":
        text = re.sub(r"^(\s*- )\[[ x-]\]", r"\1[ ]", text, flags=re.M)
    return hashlib.sha256(text.encode()).hexdigest()


def criteria(d, s):
    """{id: text}. requirements.md: `### Requirement N` + `M. ... SHALL` -> N.M. bugfix.md: `N.M WHEN ...`."""
    p = phase_file(d, s, "requirements")
    out, req = {}, None
    if not p.exists():
        return out
    for line in p.read_text().splitlines():
        if m := re.match(r"^### Requirement (\d+)", line):
            req = m.group(1)
        elif m := re.match(r"^(\d+\.\d+)\s+(WHEN|IF|WHILE|WHERE|THE)\b", line):
            out[m.group(1)] = line.strip()
        elif req and (m := re.match(r"^(\d+)\.\s+(.*\bSHALL\b.*)$", line)):
            out[f"{req}.{m.group(1)}"] = m.group(2).strip()
    return out


def later(s, phase):
    order = s["order"]
    return order[order.index(phase) + 1:]


def cmd_init(d, workflow):
    if workflow not in WORKFLOWS:
        sys.exit(f"workflow must be one of {WORKFLOWS}")
    Path(d).mkdir(parents=True, exist_ok=True)
    order = ["design", "requirements", "tasks"] if workflow == "design-first" else list(PHASES)
    save(d, {"name": Path(d).name, "workflow": workflow, "order": order,
             "phases": {p: "pending" for p in PHASES}, "hashes": {p: "" for p in PHASES}, "criteria": {}})
    print(f"INIT {d} {workflow}")


def cmd_draft(d, *phases):
    s = load(d)
    for p in phases:
        s["phases"][p] = "draft"
        print(f"DRAFT {p}")
    save(d, s)


def cmd_approve(d, *phases):
    if "tasks" in phases and check_tasks(d, quiet=True):
        sys.exit("REFUSED approve tasks: check-tasks fails. Run `spec.py check-tasks` and fix.")
    s = load(d)
    for p in phases:
        s["phases"][p] = "approved"
        s.setdefault("hashes", {})[p] = sha(phase_file(d, s, p))
        if p == "tasks":
            s["criteria"] = criteria(d, s)
        print(f"APPROVED {p}")
    save(d, s)


def mark_later_stale(s, phase):
    for q in later(s, phase):
        if s["phases"][q] != "pending":
            s["phases"][q] = "stale"
            print(f"STALE {q}")


def cmd_edited(d, phase):
    s = load(d)
    s.setdefault("hashes", {})[phase] = sha(phase_file(d, s, phase))
    mark_later_stale(s, phase)
    save(d, s)


def same(old, new):
    """Baseline holds text; early dev baselines held a 16-char hash."""
    if re.fullmatch(r"[0-9a-f]{16}", old):
        return old == hashlib.sha256(new.encode()).hexdigest()[:16]
    return old == new


def suspects(d, leaves, skip, old, new):
    """Leaves outside AFFECTS whose files still hold a number gone from the criterion (n; n±1 when n ≥ 10)."""
    if re.fullmatch(r"[0-9a-f]{16}", old):
        return []
    gone = {int(n) for n in re.findall(r"\d+", old)} - {int(n) for n in re.findall(r"\d+", new)}
    tokens = {str(m) for n in gone for m in ((n - 1, n, n + 1) if n >= 10 else (n,)) if m >= 2}
    if not tokens:
        return []
    root = Path(d).resolve().parents[2]
    pat = re.compile(r"(?<![\d.])(" + "|".join(sorted(tokens)) + r")(?![\d.])")
    out = []
    for i, v in leaves.items():
        if i in skip:
            continue
        for f in v["files"]:
            p = root / f
            if not p.is_file():
                continue
            for no, line in enumerate(p.read_text(errors="ignore").splitlines(), 1):
                if m := pat.search(line):
                    out.append(f"{i} {f}:{no} ({m.group(1)})")
    return out


def cmd_drift(d):
    s = load(d)
    found = False
    for p in s["order"]:
        if s["phases"][p] == "approved" and s.get("hashes", {}).get(p) and sha(phase_file(d, s, p)) != s["hashes"][p]:
            found = True
            print(f"DRIFT {p} {phase_file(d, s, p).name}")
            s.setdefault("hashes", {})[p] = sha(phase_file(d, s, p))
            mark_later_stale(s, p)
    base = s.get("criteria") or {}
    if base:
        now = criteria(d, s)
        tasks = Path(d) / "tasks.md"
        leaves = parse_tasks(tasks.read_text())[0] if tasks.exists() else {}
        for k in sorted(set(base) | set(now), key=lambda x: [int(n) for n in x.split(".")]):
            tag = "ADDED" if k not in base else "REMOVED" if k not in now else "CHANGED" if not same(base[k], now[k]) else ""
            if not tag:
                continue
            found = True
            print(f"{tag} {k}")
            if tag == "ADDED":
                continue
            hit = [i for i, v in leaves.items() if k in (v["reqs"] or [])]
            if hit:
                print(f"AFFECTS {k} -> {' '.join(hit)}")
            for line in suspects(d, leaves, hit, base[k], now.get(k, "")):
                print(f"SUSPECT {k} -> {line}")
    save(d, s)
    print("RESULT: DRIFT" if found else "RESULT: NO DRIFT")


def parse_tasks(text):
    leaves: dict[str, dict] = {}
    bodies: dict[str, list[str]] = {}
    groups: list[tuple[str, str]] = []
    cur: str | None = None
    for line in text.splitlines():
        if m := re.match(r"^- \[[ x-]\]\*?\s*(\d+)\.\s+(.*)$", line):
            groups.append((m.group(1), m.group(2)))
            cur = None
        elif m := re.match(r"^\s+- \[([ x-])\](\*?)\s*(\d+\.\d+)\s+(.*)$", line):
            cur = m.group(3)
            leaves[cur] = {"id": cur, "optional": m.group(2) == "*", "title": m.group(4)}
            bodies[cur] = []
        elif line.startswith("#"):
            cur = None
        elif cur is not None:
            bodies[cur].append(line)
    for leaf_id, leaf in leaves.items():
        body = "\n".join(bodies[leaf_id])
        f = re.search(r"^\s*- Files:\s*(.*)$", body, re.M)
        leaf["files"] = re.findall(r"`([^`]+)`", f.group(1)) if f else []
        k = re.search(r"^\s*- Kind:\s*(\w+)", body, re.M)
        leaf["kind"] = k.group(1) if k else None
        sm = re.search(r"^\s*- Seam:\s*(\S.*)$", body, re.M)
        leaf["seam"] = sm.group(1).strip() if sm else None
        z = re.search(r"^\s*- Size:\s*([SML])\b", body, re.M)
        leaf["size"] = z.group(1) if z else None
        e = re.search(r"^\s*- Expect:\s*(\w+)", body, re.M)
        leaf["expect"] = e.group(1) if e else None
        r = re.search(r"_Requirements:\s*([^_]*)_", body)
        leaf["reqs"] = None if not r else re.findall(r"\d+\.\d+", r.group(1)) or (["none"] if "none" in r.group(1) else [])
        leaf["props"] = re.findall(r"\*\*Property (\d+)", body)
        leaf["do"] = bool(re.search(r"^\s*- Do:", body, re.M))
        leaf["verify"] = bool(re.search(r"^\s*- Verify:", body, re.M))
        dv = " ".join(re.findall(r"^\s*- (?:Do|Verify):(.*)$", body, re.M))
        tokens = {t.rstrip(",.:;") for chunk in re.findall(r"`([^`]+)`", dv) for t in chunk.split()}
        leaf["reads"] = sorted(t for t in tokens if re.search(r"/|\.[A-Za-z]{1,5}$", t) and t not in leaf["files"])
    return leaves, groups


def cmd_check_tasks(d):
    fails = check_tasks(d)
    print("RESULT: FAIL" if fails else "RESULT: PASS")
    sys.exit(1 if fails else 0)


def check_tasks(d, quiet=False):
    s = load(d)
    text = (Path(d) / "tasks.md").read_text()
    leaves, groups = parse_tasks(text)
    fails = []

    def check(name, bad):
        if not quiet:
            print(f"FAIL {name}: {bad}" if bad else f"PASS {name}")
        if bad:
            fails.append(name)

    heads = re.findall(r"^## (.+)$", text, re.M)
    check("graph is last section", "" if heads and heads[-1].strip() == "Task Dependency Graph" else f"last = {heads[-1:]}")
    m = re.search(r"## Task Dependency Graph\s*```json\s*(\{.*?\})\s*```", text, re.S)
    try:
        g = json.loads(m.group(1)) if m else None
    except json.JSONDecodeError as ex:
        g = None
        if not quiet:
            print(f"FAIL graph JSON parses: {ex}")
    check("graph JSON parses", "" if g else "no JSON graph")
    if not g:
        return fails

    waves = g.get("waves", [])
    deps = g.get("deps", {})
    check("wave ids 0..n in order", "" if [w["id"] for w in waves] == list(range(len(waves))) else [w["id"] for w in waves])
    where = {}
    for w in waves:
        for t in w["tasks"]:
            where.setdefault(t, []).append(w["id"])
    check("graph ids are leaves", sorted(set(where) - set(leaves)))
    check("every leaf in exactly one wave", {k: where.get(k, []) for k in leaves if len(where.get(k, [])) != 1})
    check("deps name leaves", {k: v for k, v in deps.items() if k not in leaves or any(x not in leaves for x in v)})
    wave_of = {k: v[0] for k, v in where.items() if len(v) == 1}
    check("deps in earlier waves", [f"{k}<-{x}" for k, v in deps.items() for x in v
                                    if k in wave_of and x in wave_of and wave_of[x] >= wave_of[k]])

    check("every leaf has Files", [k for k, v in leaves.items() if not v["files"]])
    check("every leaf has Kind", [k for k, v in leaves.items() if v["kind"] not in KINDS])
    check("every leaf has _Requirements:_", [k for k, v in leaves.items() if v["reqs"] is None])
    check("every leaf has Size S|M|L", [k for k, v in leaves.items() if not v["size"]])
    check("every leaf has Verify", [k for k, v in leaves.items() if not v["verify"]])
    check("setup/slice/fix leaf has Do", [k for k, v in leaves.items() if v["kind"] in ("setup", "slice", "fix") and not v["do"]])
    check("slice/test/pin leaf has Seam", [k for k, v in leaves.items() if v["kind"] in ("slice", "test", "pin") and not v["seam"]])
    slices = {k: v for k, v in leaves.items() if v["kind"] == "slice"}
    check("slice holds a test file and a code file (vertical)",
          [k for k, v in slices.items() if not (any(TEST_FILE.search(f) for f in v["files"])
                                                and any(not TEST_FILE.search(f) for f in v["files"]))])
    check(f"slice touches <= {SLICE_MAX_FILES} files", [f"{k}={len(v['files'])}" for k, v in slices.items()
                                                       if len(v["files"]) > SLICE_MAX_FILES])
    check(f"slice cites <= {SLICE_MAX_CRITERIA} criteria", [f"{k}={len(v['reqs'] or [])}" for k, v in slices.items()
                                                           if len(v["reqs"] or []) > SLICE_MAX_CRITERIA])
    check("test leaf holds only test files", [k for k, v in leaves.items() if v["kind"] == "test"
                                              and any(not TEST_FILE.search(f) for f in v["files"])])
    check("optional * only on Kind test", [k for k, v in leaves.items() if v["optional"] and v["kind"] != "test"])
    clash = []
    for w in waves:
        seen = {}
        for t in w["tasks"]:
            for f in leaves.get(t, {}).get("files", []):
                if f in seen:
                    clash.append(f"wave {w['id']}: {seen[f]} & {t} -> {f}")
                seen[f] = t
    check("same-wave leaves touch disjoint files", clash)
    race = []
    for w in waves:
        owner = {f: t for t in w["tasks"] for f in leaves.get(t, {}).get("files", [])}
        for t in w["tasks"]:
            for f in leaves.get(t, {}).get("reads", []):
                if f in owner and owner[f] != t:
                    race.append(f"wave {w['id']}: {t} reads {f} written by {owner[f]}")
    check("no same-wave read of another leaf's file (Do/Verify paths)", race)
    check("test leaf deps on a slice", [k for k, v in leaves.items() if v["kind"] == "test" and slices
                                       and not any(x in slices for x in deps.get(k, []))])
    fixes = [k for k, v in leaves.items() if v["kind"] == "fix"]

    pins = [k for k, v in leaves.items() if v["kind"] == "pin"]
    check("pin leaf has Expect red|green", [k for k in pins if leaves[k]["expect"] not in ("red", "green")])
    if s["workflow"] == "bugfix":
        check("bugfix has pins", "" if pins else "no Kind: pin leaf")
        check("bugfix has a fix leaf", "" if fixes else "no Kind: fix leaf")
        check("pins run before fix", [f"{p}>={c}" for p in pins for c in fixes
                                      if p in wave_of and c in wave_of and wave_of[p] >= wave_of[c]])

    crit = set(criteria(d, s))
    cited = {r for v in leaves.values() for r in (v["reqs"] or []) if r != "none"}
    need = {c for c in crit if not c.startswith("1.")} if s["workflow"] == "bugfix" else crit
    check("every criterion cited", sorted(need - cited))
    check("cited ids exist", sorted(cited - crit))
    design = Path(d) / "design.md"
    props = set(re.findall(r"^#{3,4} Property (\d+)", design.read_text(), re.M)) if design.exists() else set()
    check("every property has a leaf", sorted(props - {p for v in leaves.values() for p in v["props"]}))
    check("final top-level task is checkpoint", "" if groups and groups[-1][1].startswith("Checkpoint") else groups[-1:])
    if not quiet:
        for num, title in groups:
            if not title.startswith("Checkpoint"):
                continue
            above = [wave_of[k] for k in leaves if int(k.split(".")[0]) < int(num) and k in wave_of]
            below = [k for k in leaves if int(k.split(".")[0]) > int(num) and k in wave_of]
            early = [k for k in below if above and wave_of[k] <= max(above)]
            if early:
                print(f"WARN checkpoint {num} runs after later-group leaves {early} (shared waves)")
    return fails


CMDS = {"init": cmd_init, "draft": cmd_draft, "approve": cmd_approve, "edited": cmd_edited,
        "drift": cmd_drift, "check-tasks": cmd_check_tasks}

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in CMDS:
        sys.exit(__doc__)
    CMDS[sys.argv[1]](*sys.argv[2:])
