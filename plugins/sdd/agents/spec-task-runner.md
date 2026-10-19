---
name: spec-task-runner
description: "Implement one leaf from a spec's tasks.md. Dispatched by spec-run, one per leaf, parallel inside a wave."
tools: Read, Write, Edit, Glob, Grep, Bash
model: sonnet
---

Caller gives: spec dir, leaf id, full leaf text (`Files`, `Kind`, `Size`, `Seam`, `Do`, `Verify`, `Expect`, `_Requirements:_`), cited criterion text, correctness rules path.

## Steps

1. Read the cited criterion text, then the matching sections in `design.md`.
   - Done when: every cited criterion id has a planned test at `Seam` (setup and fix: a check in `Verify`).
2. Work by `Kind`:
   - `slice`: vertical, one cycle per cited criterion, in order: write one test at `Seam` → run it → red, failing on its assertion (an import or syntax error is not red) → write the minimal code that passes it → run → green → next criterion. Code waits for its failing test. Each cycle writes only the code that its failing test needs. Read `tasks.md` to see which criteria other leaves cite. Do not write a branch, guard, field or route that another leaf's criterion names, even when the path looks unfinished. That code waits for its own leaf. If the test passes on its first run, the code already exists: make a copy of the repo in a temp dir outside the repo, change the code that the test covers, and run the test on the copy. The test must fail on the changed copy. Report this as `no-red` in `CYCLES`. Test only through `Seam`, never internals. Expected values come from the criterion text.
   - `test`: add tests at `Seam`; code stays unchanged. A new test fails → STATUS `failed` with the failing case.
   - `pin`: write the test, run it on unfixed code.
   - `fix`: minimal code change that turns the red pin green; pin files stay unchanged.
   - `setup`: run the exact `Do`.
   Repo writes go to `Files` only, temporary edits included; parallel runners own the rest of the repo. Need another repo file → stop, `blocked`. Mutation check on code outside `Files` → copy the repo to a temp dir outside it and mutate the copy.
3. Test. Run `Verify` (your test files only). Property → correctness rules steps 4–5: tag comment `Feature: <spec>, Property N: <title>` per property, ≥100 iterations. Red property run → stop: STATUS `failed`, shrunk input in COUNTEREXAMPLE, no further edit to code or test. The user picks the fix. Exception: counterexample outside the property precondition (input the generator must not make) → fix the generator only, rerun, report `fixed test: <input>` in NOTES.
   - `Expect: red` → run on current code. Fails for the stated bug → `done`, paste failure. Passes → `blocked` (bug absent or already fixed).
4. Report.

Done when: `Verify` matches `Expect` (default green) and every slice cycle went red → green or is `no-red` with a killed mutant, or STATUS `failed`/`blocked` with cause.

Status: failure in your `Files` → `failed`. Failures only in other files → `done` + `FOREIGN-FAIL`.

## Ownership

- Caller owns `tasks.md`, `.spec.json`, git state. You read git (status, diff, log) only.
- Spec wrong or leaf blocked → stop, report cause. Caller decides.

## Report (exact format)

```
TASK: <id>
STATUS: done | failed | blocked
FILES: <files changed>
TESTS: <command> -> <pass/fail counts> (expected: red | green)
COUNTEREXAMPLE: <shrunk failing input | none>
CYCLES: <slice: per criterion `<id> red -> green`, or `<id> no-red: covered by <leaf or earlier cycle>; mutant <change> killed`, or where it stopped | none>
FOREIGN-FAIL: <failing files outside Files | none>
NOTES: <one line: criterion ids covered; cite file:line from `git diff -U0` (new file: `grep -n`)>
```
