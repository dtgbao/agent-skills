# 03-bugfix-sonnet (plugin v0.2.0)

Model: Sonnet · Skills run: spec-new (Bugfix), spec-run `--mode single`, spec-run `--mode single --optional` · Result: PASS

## Summary
- `spec-new` Bugfix flow finished. Three artifacts drafted and approved. Root cause cites `pager/paginate.py:14`.
- `spec-run` without `--optional` ran both pins and the fix. Exploration pin 1.1 was red (3 fail). Preservation pin 1.2 was green (6 pass). Fix 2.1 made all 11 tests green. Checkpoint green. v0.1.0 issue 03-1 is fixed.
- `--optional` run executed only leaf 3.1. No `[-]` is left. Final suite: 13 passed.
- `spec.py check-tasks` caught a missing citation (Current items 1.1, 1.2). `spec.py approve` does not enforce it. I approved a FAIL file by my own error, then fixed it and re-gated (03-12).
- New open points: orchestrator checkbox marks trigger `DRIFT tasks` on the next load (03-13). `check-tasks` does not check `Do` and `Verify` (03-14). Checkpoint rule is unclear when a group holds only skipped `*` leaves (03-15). The "pin after fix" drop rule did not fire, because pin 1.1 was already `[x]` (03-16).

## Step trace
| Skill | Step | Action taken | Done-when held | Evidence |
|---|---|---|---|---|
| spec-new | 1 Name | `paginate-last-page`. Dir did not exist | Yes | `docs/specs/` empty before |
| spec-new | 2 Size | Workflow named → wins. Continue | Yes | "Named workflow wins" |
| spec-new | 3 Workflow | Bugfix from input | Yes | – |
| spec-new | 4 State | `SPEC init docs/specs/paginate-last-page bugfix` → `INIT ...` | Yes | `.spec.json` all `pending` |
| bugfix wf | 1 Facts | Repro, current, expected in input. Must-hold fact missing → asked Q1. Scripted answer | Yes | Q&A row 1 |
| bugfix wf | 2 Investigate | Traced `paginate` → `total_pages`. Cause `pager/paginate.py:14` (`count // size`); effect at `:22-23` | Yes | Explains 1.1 and 1.2 |
| bugfix wf | 3 Draft bugfix.md | 2 Current, 2 Expected, 5 Unchanged | Partly | See artifact checks (2.2 and 3.1 hold two assertions) |
| bugfix wf | 4 Gate 1 | `SPEC draft` → `SPEC approve requirements` | Yes | Snapshot S1 |
| bugfix wf | 5 Draft design.md | Per `bugfix-design.md` | Yes | See artifact checks |
| bugfix wf | 6 Gate 2 | draft + approve design | Yes | Snapshot S2 |
| bugfix wf | 7 Draft tasks.md | 4 leaves (3.1 is `*`), 3 waves | First `check-tasks` FAIL, then PASS | Outputs C1, C2 |
| bugfix wf | 8 Gate 3 | Approved once with FAIL (my slip), then fixed, `SPEC draft` + `SPEC approve tasks` again | Yes (second time) | Snapshots S3a, S3b |
| spec-run (run 1) | 1 Load | `SPEC drift` → `RESULT: NO DRIFT`. All phases approved | Yes | Output D1 |
| spec-run (run 1) | 2 Mode | `--mode single` given | Yes | – |
| spec-run (run 1) | 3 Scope | `[ ]` leaves: 1.1, 1.2, 2.1, 3.1(`*`). Dropped 3.1. Scope = 1.1, 1.2, 2.1 + checkpoint 4 | Yes | – |
| spec-run (run 1) | 4 Graph | `check-tasks` PASS (output C2 on the same file; hash unchanged per D1) | Yes | C2 |
| spec-run (run 1) | 5 Leaf 1.1 | Run → `[-]` → runner → `done`, red 3 fail → `[x]` | Yes | Red output R1 |
| spec-run (run 1) | 5 Leaf 1.2 | Run → runner → `done`, green 6 pass → `[x]` | Yes | Green output G1 |
| spec-run (run 1) | 5 Leaf 2.1 | Run → runner → `done`, 11 pass → `[x]`. I re-ran suite: 11 passed | Yes | Output F1 |
| spec-run (run 1) | 5 Groups, checkpoint | Groups 1, 2 → `[x]`. Group 3 stays `[ ]` (only a skipped `*` leaf). I ran checkpoint 4 anyway: 11 passed → `[x]` | Yes (ambiguous rule) | 03-15 |
| spec-run (run 1) | 7 Report | No `[-]` left | Yes | `grep -c '\[-\]'` → 0 |
| spec-run (run 2) | 1 Load | `SPEC drift` → `DRIFT tasks tasks.md`, `RESULT: DRIFT` (caused by my own checkbox marks) | No | Output D2, 03-13 |
| spec-run (run 2) | 3 Scope | `--optional`. `[ ]` leaves: 3.1 only. Pin 1.1 is `[x]` → no pin to drop | Yes | – |
| spec-run (run 2) | 4 Graph | `check-tasks` PASS | Yes | C3 |
| spec-run (run 2) | 5 Leaf 3.1 | Run → `[-]` → runner → `done`, 2 pass → `[x]`. Group 3 → `[x]` | Yes | – |
| spec-run (run 2) | 7 Report | No `[-]`. Suite 13 passed. Scope stayed correct (only 3.1) | Yes | Output F2 |

## Scripted Q&A
| # | Question (as the skill would ask) | Options | Answer | Scripted? |
|---|---|---|---|---|
| 1 | Bugfix step 1: which existing behavior must hold? | free text | Exact multiples work; page < 1 and size < 1 raise `ValueError`; empty list → 0 pages | Yes |
| 2 | Gate 1 (bugfix.md) | Approve · Request changes · Analyze first | Approve | Yes |
| 3 | Gate 2 (design.md) | Approve · Request changes | Approve | Yes |
| 4 | Gate 3 (tasks.md), first time | Approve · Request changes | Approve (file still FAIL, see 03-12) | Yes |
| 4b | Gate 3 (tasks.md), after my fix | Approve · Request changes | Approve | Yes |
| 5 | Leaf 1.1 | Run · Skip · Stop | Run | Yes |
| 6 | Leaf 1.2 | Run · Skip · Stop | Run | Yes |
| 7 | Leaf 2.1 | Run · Skip · Stop | Run | Yes |
| 8 | Leaf 3.1 (run 2) | Run · Skip · Stop | Run | Yes |

No Retry or checkpoint-red question came up.

## Evidence

### Check-tasks outputs
C1 (first draft of tasks.md, leaf 1.1 cited only `2.1, 2.2`):
```
PASS graph is last section
...
PASS pins run before fix
FAIL every criterion cited: ['1.1', '1.2']
PASS cited ids exist
PASS every property has a leaf
PASS final top-level task is checkpoint
RESULT: FAIL
```
C2 (after adding `1.1, 1.2` to leaf 1.1) and C3 (start of run 2): all 20 checks `PASS`, last line `RESULT: PASS`.

### `.spec.json` after each gate
S1 (after Gate 1): `phases` = requirements `approved`, design `pending`, tasks `pending`. `hashes.requirements` = `a2bfefd7...ad24`. `criteria` = `{}`.

S2 (after Gate 2): requirements `approved`, design `approved`, tasks `pending`. `hashes.design` = `c09a8c7f...5aef`.

S3a (Gate 3, first approval, tasks.md still FAIL): all `approved`. `hashes.tasks` = `f51f0421...4bb7`. `criteria` = 9 ids (1.1 1.2 2.1 2.2 3.1 3.2 3.3 3.4 3.5).

S3b (Gate 3, after fix):
```json
{"name":"paginate-last-page","workflow":"bugfix","order":["requirements","design","tasks"],
 "phases":{"requirements":"approved","design":"approved","tasks":"approved"},
 "hashes":{"requirements":"a2bfefd75d4c9e41b1ebcc8c64eecacc999e99a73228f8ef015161270d50ad24",
           "design":"c09a8c7f711ba83f2a716728181b8595342a8ef087f0ee9d93926b0e1bc35aef",
           "tasks":"758036d730a99c9d28a3278118a74ccd0973badc909d8cbfdd5ae778a1554e8f"},
 "criteria":{"1.1":"4b47b9b12a106987","1.2":"6e5dfdb61713645a","2.1":"36dbb98bf2847c63","2.2":"b16774be8ffef64b",
             "3.1":"97085ded12c0f016","3.2":"19df95068a240dad","3.3":"28d69efcf8fdc9b2","3.4":"534ecc2aaf10918f","3.5":"3b2bd70ba6f960cc"}}
```
D1 (run 1 load): `RESULT: NO DRIFT`.

D2 (run 2 load, after run 1 checkbox marks): `DRIFT tasks tasks.md` / `RESULT: DRIFT`. `drift` re-stored the hash (`hashes.tasks` = `241b7af0...1a8f` at the end of run 2). Phases stayed `approved`; `tasks` is the last phase, so nothing went `stale`. After run 2 the same `DRIFT tasks` printed again.

### Run 1 pin outputs (no `--optional`)
Pins ran. R1 = exploration pin 1.1, before the fix, `Expect: red`:
```
tests/test_paginate_bug.py FFF                                           [100%]
___ test_total_pages_partial_last_page ___
>       assert total_pages(25, 10) == 3
E       assert 2 == 3
___ test_paginate_last_partial_page ___
>       assert p.items == [20, 21, 22, 23, 24]
E       assert [] == [20, 21, 22, 23, 24]
___ test_fix_check ___   (Hypothesis, tag "Feature: paginate-last-page, Property 1: Fix check")
E       assert 0 == 1
E       where 0 = total_pages(1, 2)
E       Failing test case: test_fix_check(count=1, size=2)
============================== 3 failed in 0.53s ===============================
```
Runner report: `STATUS: done`, `COUNTEREXAMPLE: count=1, size=2`.

G1 = preservation pin 1.2, before the fix, `Expect: green`:
```
tests/test_paginate_preservation.py ......                               [100%]
============================== 6 passed in 0.49s ===============================
```
The Hypothesis test checks "page above total" with `ceil(count/size)`, so it is green before and after the fix. Criterion 3.5 text says "above `total_pages`". The pin tests a fix-independent form.

F1 = after fix 2.1 (`pager/paginate.py:14` → `return -(-count // size)`):
```
tests/test_paginate.py ..   tests/test_paginate_bug.py ...   tests/test_paginate_preservation.py ......
============================== 11 passed in 0.59s ==============================
```
F2 = end of run 2: `13 passed in 0.54s`.

### Run 2 (`--optional`) answers
- Scope: only 3.1. Boundary tests, 2 passed. Final `tasks.md`: all groups, leaves, and checkpoint `[x]`. `grep -c '\[-\]'` → `0`.
- "Drop red pin after the fix": not exercised. Pin 1.1 was `[x]`, so scope never held it. By text (`skills/spec-run/SKILL.md:15`) a `[ ]` red pin with a `[x]` fix leaf is dropped. The rule does not say how to find "its fix leaf". I would use the `Kind: code` leaf whose `deps` list the pin. See 03-16.
- The checkpoint was already `[x]` from run 1. It did not re-run after the new test leaf 3.1. I ran the full suite by hand: 13 passed.

## Artifact checks
| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| bugfix.md | repro steps exact: starting state, input, observed result | Pass | Introduction: 25 items, size 10, `paginate(list(range(25)), 3, 10)`, observed `Page(items=[], page=3, total_pages=2)` |
| bugfix.md | every Current `1.n` has Expected `2.n` with same condition | Pass | 1.1↔2.1, 1.2↔2.2 |
| bugfix.md | Unchanged covers neighbor paths named or exposed | Pass | 3.1 multiples, 3.2 page<1, 3.3 size<1, 3.4 empty, 3.5 page above total (exposed by `paginate.py:22-23`) |
| bugfix.md | every item has one observable assertion | Fail | 2.2 asserts items and `total_pages`. 3.1 asserts `total_pages` and items. Split needed |
| design.md | Root Cause cites `file:line`, explains every Current item | Pass | `pager/paginate.py:14`, `:22-23`; covers 1.1, 1.2 |
| design.md | Fix names every changed component and its constraint | Pass | `total_pages`; keep guard first; keep 0 for empty |
| design.md | Call-tree Change shows failing path as `diff` | Pass | `diff` fence with `-`/`+` on line 14 |
| design.md | Property 1 = fix check, Property 2 = preservation, each `**Validates:**` | Pass | Headings `### Property 1: Fix check`, `### Property 2: Preservation` |
| design.md | Regression Strategy names pin tests for every Unchanged item | Pass | 3.1–3.5 each listed |
| tasks.md | `check-tasks` prints `RESULT: PASS` | Pass (after fix) | C1 FAIL → C2 PASS |
| tasks.md | Bugfix order: red pin, green pin, fix, checkpoint | Pass | Waves 0 (1.1, 1.2), 1 (2.1), 2 (3.1); `deps` 2.1→1.1,1.2 |
| tasks.md | Pins never `*` | Pass | 1.1 and 1.2 have no `*`; `*` only on 3.1 (`Kind: test`) |
| tasks.md | Leaf fields in order Files/Kind/Do/Verify/_Requirements_ | Pass (by eye) | `check-tasks` does not test `Do` and `Verify` (03-14) |

Fit of design Done-when items to the bugfix skeleton: all five items of `shared/artifacts/bugfix-design.md` fit its skeleton. None points to a missing section.

## Issues
| ID | Severity | Plugin file:line | Problem | Proposed fix |
|---|---|---|---|---|
| 03-12 | med | `shared/scripts/spec.py:83` (`cmd_approve`), `shared/gate.md:9`, `shared/workflows/bugfix.md:17-19` | `SPEC approve tasks` runs no check. I approved a `tasks.md` that printed `RESULT: FAIL`, and the state went `approved` with a criteria baseline. Gate step 1 does not say to run `check-tasks` before the user sees the count line. | `approve tasks` runs `check-tasks` and refuses on FAIL. Or gate.md step 1 runs it for the tasks phase. |
| 03-13 | med | `skills/spec-run/SKILL.md:13,21-23`, `shared/state.md:29`, `shared/scripts/spec.py` (`cmd_drift`) | Orchestrator checkbox marks change the `tasks.md` hash. The next `SPEC drift` prints `DRIFT tasks tasks.md` and `RESULT: DRIFT`. It reads like a hand edit. No command records the marks. | Add `SPEC mark <dir> <id> <x|-| >`. Or hash `tasks.md` with checkbox chars stripped. Or `spec-run` calls `SPEC edited <dir> tasks` after marks. |
| 03-14 | low | `shared/artifacts/tasks.md:13-14,35`, `shared/scripts/spec.py:156` | Done-when says `check-tasks` covers fields. It checks `Files`, `Kind`, `_Requirements:_`, and `Expect`. It does not check `Do` and `Verify`. | Add two checks. Or narrow the Done-when text. |
| 03-15 | low | `skills/spec-run/SKILL.md:22-23` | "Checkpoint, once every group above it is done": group 3 held only a skipped `*` leaf and stayed `[ ]`. Literal reading never reaches the checkpoint. After a later `--optional` run the checkpoint is `[x]` and does not re-run. | Say "every group with in-scope leaves". State whether an `[x]` checkpoint re-runs when new leaves finish. |
| 03-16 | low | `skills/spec-run/SKILL.md:15` | "`Expect: red` pin whose fix leaf is `[x]` → drop". The text does not say how to find the fix leaf. The rule did not fire here, because pin 1.1 was `[x]`. Unverified. | Define: fix leaf = `Kind: code` leaf with the pin in `deps`. Add an eval that resets a red pin to `[ ]` after the fix. |
| 03-17 | low | `shared/artifacts/bugfix.md:6-8` vs `shared/ears.md` rules | Done-when needs one assertion per item. The skeleton shows Expected forms that invite two outcomes (items and total). Nothing checks it. | Add an Expected example with one assertion. |

## v0.1.0 issues
Read after the run: `docs/sdd-eval/03-bugfix-sonnet/report.md`.

| Old ID | Status | Evidence |
|---|---|---|
| 03-1 `*` drops pins | fixed | `shared/artifacts/tasks.md:21` "Pins are never `*`"; `spec.py` check "optional * only on Kind test". Run 1 without `--optional` ran 1.1, 1.2, 2.1. |
| 03-2 wave rule vs bugfix order | fixed | Pins have `Kind: pin`, outside the "test leaf deps on code leaf" rule. Fix leaf `deps` on pins (`tasks.md` wave rules). `check-tasks` printed `PASS pins run before fix`. |
| 03-3 runner and red expectation | fixed | `agents/spec-task-runner.md` step 3 handles `Expect: red`. Leaf 1.1 reported `done` with red output (R1). Pin-after-fix guard exists in text (`spec-run/SKILL.md:15`) but did not fire (03-16). |
| 03-4 single mode mark on failure | changed | `spec-run/SKILL.md:21` now: `failed`/`blocked` → `[ ]`, ask Retry · Skip · Stop. Text fixed. No leaf failed, so not run. |
| 03-5 no checkpoint step | changed | Checkpoint step is at `spec-run/SKILL.md:23`, group rule at `:22`. Checkpoint ran and went `[x]`. Rule is unclear for groups that hold only skipped `*` leaves (03-15). |
| 03-6 design Done-when does not fit | fixed | New `shared/artifacts/bugfix-design.md` with own Done-when list. All five items passed (see artifact checks). |
| 03-7 "one-line change" skips workflow | fixed | `skills/spec-new/SKILL.md:16`: "Named workflow wins." Bugfix ran although the fix is one line. |
| 03-8 `draft` never set for design and tasks | fixed | `shared/gate.md:5` sets `SPEC draft` at every gate. Gates 2 and 3 printed `DRAFT design` / `DRAFT tasks`. |
| 03-9 wrong command name | fixed | `shared/workflows/bugfix.md:19`: `/sdd:spec-run <name>`. |
| 03-10 bugfix properties are bullets | fixed | `bugfix-design.md` skeleton uses `### Property 1: Fix check` and `### Property 2: Preservation`. `check-tasks` printed `PASS every property has a leaf`. |
| 03-11 Unchanged items need code read before investigation | fixed | `shared/workflows/bugfix.md:9` investigates before the draft at `:11`. Neighbor path 3.5 came from that step. |

## Ambiguity log
- "Any missing → ask via AskUserQuestion" (bugfix.md:7), input holds repro, current, expected but not "behavior that must hold" → asked Q1 → the fourth fact was missing.
- "Checkpoint, once every group above it is done" (spec-run:23) with group 3 holding only a skipped `*` leaf → ran the checkpoint → Done-when needs every in-scope leaf `[x]`, and the checkpoint is in scope.
- spec-run step 4 in run 1: I did not call `check-tasks` again after the gate. The file hash was unchanged (D1), so I used C2 → the output would be identical.
- "Group → `[x]` when all its leaves are `[x]`" (spec-run:22) → I counted a `*` leaf as a leaf. Group 3 became `[x]` only in run 2.
- Preservation criterion 3.5 says "above `total_pages`" → the runner tested above `ceil(count/size)` → the buggy total would make the pin red before the fix.
- Gate 3 after the FAIL → I fixed my own file and re-ran the gate without asking → no "Request changes" was scripted.

## Metrics
- Questions asked: 9 · Subagent dispatches: 4 (1.1, 1.2, 2.1, 3.1) · Gates: 4 (3 artifacts + 1 re-gate of tasks) · Tests run: pre-fix 3 fail (pin 1.1) and 6 pass (pin 1.2); post-fix 11 pass; end of run 2 13 pass, 0 fail
