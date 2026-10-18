# 03-bugfix-sonnet

Model: Sonnet · Skills run: spec-new (Bugfix), spec-run `--mode single` · Result: PARTIAL

## Summary
- `spec-new` bugfix flow finished. Three artifacts drafted and approved. Root cause cites `pager/paginate.py:14`. The citation is correct.
- `spec-run` without `--optional` ran only leaf 3.1 (the fix). Every other leaf is `*`. The exploration test and the preservation tests never ran. The Bugfix order (red, green, fix) did not happen. (03-1)
- Wave rule "test after code" conflicts with Bugfix order. A literal graph check stops the run. I read it as an exception and went on. (03-2)
- The exploration test cannot go red once the fix is in. A later `--optional` run of leaf 1.1 came back `blocked`. Single mode left the leaf `[-]`. (03-3, 03-4)
- Checkpoints have no rule in single mode. The design Done-when list does not fit the bugfix skeleton. (03-5, 03-6)

## Step trace
| Skill | Step | Action taken | Done-when held | Evidence |
|---|---|---|---|---|
| spec-new | 1 Name | `paginate-last-page-missing`; `docs/specs/` absent in WS | Yes | dir created |
| spec-new | 2 Size | Bug fix is one line, but input names the Bugfix workflow. Did not stop. | n/a | ambiguity A1 |
| spec-new | 3 Workflow | Input starts with "Bugfix:". Used it. No question. | Yes | — |
| spec-new | 4 State | Wrote `.spec.json` per state.md | Yes | all phases `pending` |
| spec-new | 5 Run workflow | Read `shared/workflows/bugfix.md` | Yes | — |
| bugfix wf | 1 Facts | Repro, current, expected were in input. "Behavior that must hold" was missing. Asked 1 question. | Yes after answer | Q1 |
| bugfix wf | 2 Draft bugfix.md | 2 Current, 2 Expected, 8 Unchanged | Yes (4/4 items, see checks) | `docs/specs/…/bugfix.md` |
| bugfix wf | 3 Gate | Show path and count. Options Approve / Request changes / Analyze first. Answer Approve. Phase `approved`. | Yes | `.spec.json` |
| bugfix wf | 4 Investigate | Traced `paginate` → `total_pages`. Cause: floor division. | Yes: cause explains 1.1 and 1.2 | `paginate.py:14`, `:21-23` |
| bugfix wf | 5 Draft design.md | Bugfix skeleton. Kept Overview and Testing Strategy. | Partial (see checks) | `design.md` |
| bugfix wf | 6 Gate | Approve. Phase `approved`. | Yes | `.spec.json` |
| bugfix wf | 7 Draft tasks.md | Bugfix order. 4 test leaves marked `*`. | Yes (4/4) | `tasks.md` |
| bugfix wf | 8 Gate | Approve. Tell user `/spec-run`. | Yes | `.spec.json` |
| spec-run | 1 Load | `tasks` phase = `approved` | Yes | — |
| spec-run | 2 Mode | `--mode single` given | Yes | — |
| spec-run | 3 Scope | `[ ]` leaves: 1.1 1.2 3.1 3.2 3.3. Drop `*` leaves. Scope = {3.1}. | Yes | — |
| spec-run | 4 Graph | Wave rule "test after code" is broken by 1.1/1.2. Did not stop. | n/a | ambiguity A2, issue 03-2 |
| spec-run | 5 single: 3.1 | Showed leaf. Ask Run. Marked `[-]`. Dispatched runner. Report `done`. Marked `[x]`. | Yes | 2 passed |
| spec-run | 7 Report | Only 3.1 in scope and `[x]`. Skipped leaves not listed with a reason by the skill. | Yes (literal) | — |
| spec-run (supplement, `--optional`) | 5 single: 1.1 | Run. Marked `[-]`. Runner report `blocked`. Retry not dispatched (A5). Stop. | No | leaf 1.1 still `[-]` |

Run order note: I ran the exploration and preservation tests on a scratch copy of the unfixed code BEFORE the literal `spec-run`. `spec-run` would not have run them. Test text was written by me from the leaf text.

## Scripted Q&A
| # | Question (as the skill would ask) | Options | Answer | Scripted? |
|---|---|---|---|---|
| 1 | Facts (bugfix.md:7): "What behavior must stay unchanged?" | free text | "Exact multiples still work: 20 items, size 10 → 2 pages. page < 1 raises ValueError. size < 1 raises ValueError. Empty list → total_pages 0, page 1 returns empty items." | Yes |
| 2 | Gate bugfix.md (gate.md:6) | Approve / Request changes / Analyze first | Approve | Yes |
| 3 | Gate design.md | Approve / Request changes | Approve | Yes |
| 4 | Gate tasks.md | Approve / Request changes | Approve | Yes |
| 5 | spec-run leaf 3.1 (spec-run:22) | Run / Skip / Stop | Run | Yes |
| 6 | spec-run leaf 1.1 (supplement) | Run / Skip / Stop | Run | Yes |
| 7 | Failed leaf 1.1 (blocked) | Retry once, then Stop (script). Skill gives no option list in single mode. | Retry, then Stop. Retry not dispatched. | Yes, partly (A5) |
| — | Checkpoints 2 and 4 | no question asked: single mode has no rule | logged | — |

Facts question: the skill did ask. It asked only for "behavior that must hold". Expected result was implied by the input.

## Pre-fix and post-fix test evidence

Exploration test, unfixed code (`count // size`), scratch copy. Red:

```
tests/test_paginate_bug.py FF                                            [100%]
_________________________ test_last_partial_page_items _________________________
>       assert paginate(list(range(25)), 3, 10).items == [20, 21, 22, 23, 24]
E       assert [] == [20, 21, 22, 23, 24]
______________________ test_last_partial_page_total_pages ______________________
>       assert paginate(list(range(25)), 3, 10).total_pages == 3
E       assert 2 == 3
E        +  where 2 = Page(items=[], page=3, total_pages=2).total_pages
FAILED tests/test_paginate_bug.py::test_last_partial_page_items - assert [] =...
FAILED tests/test_paginate_bug.py::test_last_partial_page_total_pages - asser...
============================== 2 failed in 0.45s ===============================
```

Preservation tests, unfixed code, scratch copy. Green:

```
test_3_1_exact_multiple_total_pages PASSED   test_3_2_exact_multiple_items PASSED
test_3_3_page_zero_raises PASSED             test_3_4_size_zero_raises PASSED
test_3_5_empty_total_pages PASSED            test_3_6_empty_items PASSED
test_3_7_non_multiple_full_page PASSED       test_3_8_page_above_total_pages PASSED
============================== 8 passed in 0.38s ===============================
```

Final run in WS after the fix (existing 2 tests + exploration 2 tests). Green:

```
tests/test_paginate.py::test_exact_multiple PASSED
tests/test_paginate.py::test_page_zero_raises PASSED
tests/test_paginate_bug.py::test_last_partial_page_items PASSED
tests/test_paginate_bug.py::test_last_partial_page_total_pages PASSED
============================== 4 passed in 0.40s ===============================
```

Preservation test file `tests/test_paginate_preservation.py` is NOT in WS. Leaf 1.2 never ran. The 8 preservation tests were not rerun after the fix.

## Artifact checks
| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| bugfix.md | Repro exact: start state, input, observed | Pass | Introduction lists 4 repro lines |
| bugfix.md | Each Current `1.n` has Expected `2.n`, same condition | Pass | 1.1↔2.1, 1.2↔2.2 |
| bugfix.md | Unchanged covers named + code-exposed neighbors | Pass | 3.1–3.6 user-named; 3.7, 3.8 from code (`paginate.py:22-25`). Caveat: code was read before step 4 (A3, 03-11). |
| bugfix.md | One observable assertion per item | Pass | each item has one `==` or one raise |
| design.md | Every criterion maps to ≥1 component or property | Pass | `_Requirements:_` on Fix; Validates on Property 1, 2. Current items 1.1, 1.2 not cited. |
| design.md | Every external dependency has Error Handling entry | Skipped | no external dependency; bugfix skeleton has no Error Handling section |
| design.md | Every component has interface sketch | Pass | `def total_pages(count: int, size: int) -> int` |
| design.md | ≥1 Mermaid diagram | Skipped (Fail if literal) | bugfix skeleton has no Architecture slot; visuals.md says use smallest view; no actor interaction |
| design.md | File/Folder Structure as `diff` | Skipped (Fail if literal) | no section in bugfix skeleton; only one file changes, no layout change |
| design.md | Changed component call tree as `diff` | Pass | "Call-tree change" diff block |
| design.md | Testing Strategy lists every property from correctness.md | Pass | Kept Testing Strategy at the end; lists Property 1, 2, tag comment, 100 iterations. Skeleton has no such section (A4). |
| design.md | Every non-functional constraint has owner | Skipped | none exist |
| tasks.md | Every criterion cited by ≥1 leaf | Pass | 1.1, 1.2, 2.1, 2.2, 3.1–3.8 cited |
| tasks.md | Every leaf in exactly one wave | Pass | waves 0–2 hold 1.1 1.2 3.1 3.2 3.3 once each |
| tasks.md | Every leaf names its files | Pass | `Files:` line on each leaf |
| tasks.md | Graph JSON parses | Pass | `json.loads` OK |
| tasks.md | Wave rule: test leaf after code leaf it covers | Fail by design | 1.1, 1.2 sit before 3.1 (Bugfix order). 03-2 |
| tasks.md | Wave rule: same-wave leaves touch disjoint files | Pass | 3.2, 3.3 use separate files |

Design Done-when items applied: 1, 3, 6, 7. Skipped: 2, 4, 5, 8. Reason for each skip is in the table. The skeleton replaced Architecture, File/Folder, Components, Data Models, Correctness Properties, Error Handling. Done-when items 4, 5, 2 point at those replaced sections.

## Required extra checks
- Root cause: `pager/paginate.py:14` `return count // size` (floor). Consequence at `:21-23`. Correct. Fix `(count + size - 1) // size` made both exploration tests pass.
- Optional marking: 1.1, 1.2, 3.2, 3.3 are `*`. Only 3.1 is not. `spec-run` without `--optional` skips all four. Effect: no red test before the fix, no preservation test before the fix, no property test. Bugfix order step 1, 2 and 4 do not run. Only 3.1 runs.
- Leaves left `[-]` after `spec-run`: literal run: none. Supplement run: 1.1 stays `[-]` (single mode has no rule to reset it).
- `.spec.json` after run: unchanged and valid: workflow `bugfix`, order `requirements, design, tasks`, all three phases `approved`. `spec-run` writes nothing to it, so it holds no run progress.
- Checkpoint (tasks 2, 4) in single mode: single steps (spec-run:21-24) cover leaves only. Scope (spec-run:17) selects leaves. A checkpoint is a top-level task with no children. No step runs tests or asks the user. Logged: nothing done. The waves-only rule (spec-run:31) runs tests at a checkpoint. Single mode has no equivalent.

## Issues
| ID | Severity | Plugin file:line | Problem | Proposed fix |
|---|---|---|---|---|
| 03-1 | high | `skills/spec-run/SKILL.md:17`, `shared/artifacts/tasks.md:6,27-32` | `spec-run` drops `*` leaves. Format marks all test leaves `*`. Bugfix exploration and preservation leaves are tests, so they are dropped. Only the fix runs. | In tasks.md state: Bugfix exploration and preservation leaves are never `*`. Or `spec-run` keeps leaves tagged as bugfix pins. |
| 03-2 | high | `shared/artifacts/tasks.md:19` vs `:27-32`; `skills/spec-run/SKILL.md:18` | Wave rule "test leaf after code leaf it covers" contradicts Bugfix order (tests before fix). Literal graph check at spec-run step 4 says "Broken → stop". | Add exception to the wave rule for Bugfix exploration/preservation leaves. |
| 03-3 | high | `agents/spec-task-runner.md:16`; `shared/artifacts/tasks.md:29` | Runner Done-when says "tests green". Exploration leaf must be red on unfixed code. No instruction tells the runner to report `done` for an expected red. No guard tells the runner that the fix is already in. Leaf 1.1 came back `blocked` when run after the fix. | Add to the runner: leaf says "red" → expected red = `done`; report the failing output. Add to `spec-run`: run exploration leaves before the fix leaf or refuse to run them after. |
| 03-4 | med | `skills/spec-run/SKILL.md:24` vs `:29` | Single mode "Else show report" does not say what mark the leaf gets. Waves mode resets to `[ ]`. Leaf 1.1 stayed `[-]`. Single mode also has no Retry option (Run / Skip / Stop only). | Single mode: non-`done` → reset to `[ ]`, ask Retry / Skip / Stop. |
| 03-5 | med | `skills/spec-run/SKILL.md:21-24,31` | Single mode has no checkpoint step. Final tests do not run. Checkpoint `[ ]` marks and group marks `[ ]` are never updated. Step 7 "every in-scope leaf" ignores groups. | Add a single-mode checkpoint step (run tests, ask user). State how group tasks are marked. |
| 03-6 | med | `shared/artifacts/design.md:3-11,64` | One Done-when list for two skeletons. "Replace middle sections" does not name the sections. Items 2, 4, 5, 8 point at sections the bugfix skeleton does not have. Testing Strategy (item 7) is also not in the bugfix skeleton. | Add a separate Done-when list under the bugfix skeleton. Name the kept sections. |
| 03-7 | low | `skills/spec-new/SKILL.md:15` | "Typo or one-line change → spec unneeded". This fix is a one-line change. Rule can be read as skipping the Bugfix workflow the user named. | Say the rule judges the request, not the final diff size; or let a named workflow override. |
| 03-8 | low | `shared/workflows/bugfix.md:14,17`; `shared/state.md:16` | Only step 2 sets phase `draft`. Steps 5 and 7 do not. `draft` is never set for design and tasks. | Add "Set phase `draft`" to steps 5 and 7. |
| 03-9 | low | `shared/workflows/bugfix.md:18` | Tells the user `/spec-run <name>`. Plugin command is `/sdd:spec-run`. | Use the namespaced name. |
| 03-10 | low | `shared/artifacts/design.md:81-82`, `shared/correctness.md:9-10`, `shared/artifacts/tasks.md:10` | Bugfix Validation Properties are bullets ("Fix check", "Preservation"). Tasks and correctness.md expect `### Property N`. Mapping is unclear. I used "Property 1/2" in the bullets. | Make the bugfix skeleton use `Property N` headings. |
| 03-11 | med | `shared/workflows/bugfix.md:9,12`; `shared/artifacts/bugfix.md:8` | Step 2 Done-when needs Unchanged items from "code read exposed". Code is read in step 4, after the step 2 draft and gate. | Move Investigate before the draft, or drop the code-read clause from the bugfix.md Done-when. |

## Ambiguity log
- A1: "Typo or one-line change → say spec unneeded" → ran Bugfix flow → user named Bugfix and asked for a spec; defect has an exact repro.
- A2: Wave rule "Test leaf after code leaf it covers" vs Bugfix order → followed Bugfix order, did not stop at step 4 → stopping would block every bugfix spec.
- A3: "code read exposed" in bugfix.md Done-when → I had read the fixture code during setup, so I added 3.7 and 3.8 → the workflow reads code only at step 4.
- A4: "replace middle sections" → kept Overview and Testing Strategy, replaced the rest → the Done-when list needs Testing Strategy.
- A5: Failed leaf "Retry once, then Stop" → did not dispatch the retry for 1.1 → cause is repo state (fix already applied), not flakiness. Retry gives the same result. Marked UNSCRIPTED shortcut.
- A6: Peeked ahead: I read `shared/artifacts/tasks.md` (whole file) before step 7 and `design.md` before step 5 in one `cat`. Minor deviation from "read only when a step says so".
- A7: Checkpoint mark and group mark in single mode → left untouched → no step covers them.
- A8: Exploration/preservation tests were run on a scratch copy of unfixed code, outside `spec-run`, to get the pre-fix evidence the brief asks for.

## Metrics
- Questions asked: 7 (1 facts, 3 gates, 2 Run, 1 failed-leaf) · Subagent dispatches: 2 (3.1 done, 1.1 blocked) · Gates: 3 · Tests run: pre-fix exploration 0 pass / 2 fail; pre-fix preservation 8 pass / 0 fail; post-fix in WS 4 pass / 0 fail
- Leaves: 5 total. `[x]` 1 (3.1). `[-]` 1 (1.1). `[ ]` 3 (1.2, 3.2, 3.3).
- Files in WS changed: `pager/paginate.py`, `tests/test_paginate_bug.py`, `docs/specs/paginate-last-page-missing/*`.
