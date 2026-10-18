# 06-lifecycle-sonnet (plugin v0.2.0)

Model: Sonnet · Skills run: spec-new (Quick Plan), spec-run ×2, spec-sync · Result: PARTIAL

Spec name: `slugify`. Workspace: `workspace/docs/specs/slugify/`.

## Summary

- Hand-edit detection works. `spec.py drift` printed `DRIFT requirements`, `STALE design`, `STALE tasks`, `CHANGED 1.3`, `CHANGED 2.3`. `.spec.json` then showed design and tasks `stale`.
- spec-sync refined design, edited leaves, unticked leaf 1.1, group 1 and both checkpoints. Run 2 changed the code: `MAX_LEN` 50 → 40. `len(slugify('a'*45))` = **40**.
- Run 2 ended with a red checkpoint (13 pass, 1 fail). Test leaf 3.1 hard-codes `"a"*49` (`tests/test_slugify.py:31-33`). I judged "tests use `MAX_LEN`" and kept 3.1 ticked. That was wrong. Script rule "checkpoint red → Stop" applied. Run stopped. Checkpoints 2 and 4 stay `[ ]`.
- Routing test passed. Tasks forced to `draft` → spec-run step 1 stops and gives `/sdd:spec-new slugify`.
- Wave dispatch in one message, disjoint files, `check-tasks` PASS ×2, checkpoint ran the README test command. New defect: tick-mark edits to `tasks.md` cause a false `DRIFT tasks` (06v2-1).

## Step trace

| Skill | Step | Action taken | Done-when held | Evidence |
|---|---|---|---|---|
| spec-new | 1 Name | `slugify`. `docs/specs` did not exist | Yes | `ls docs/specs` → no such dir |
| spec-new | 2 Size | Not trivial | n/a | — |
| spec-new | 3 Workflow | Input names Quick Plan, no question | Yes | — |
| spec-new | 4 State | `SPEC init docs/specs/slugify quick-plan` | Yes | `INIT docs/specs/slugify quick-plan`; all `pending` |
| quick-plan | 1 Questions | 1 call, 4 questions, scripted answers | Yes | Q&A #1. Assumptions in Introduction |
| quick-plan | 2 Draft | 3 files, `SPEC draft` | Yes | `check-tasks` RESULT: PASS (first try). Done-when lists below |
| quick-plan | 3 Approve | Q&A #2 → `SPEC approve` ×3 | Yes | `drift` → `RESULT: NO DRIFT`. 10 criteria hashes stored |
| (extra) | Route test | Copy of `.spec.json`, tasks → `draft`, then restored | Yes | See "Routing test" |
| spec-run 1 | 1 Load | `drift` NO DRIFT; all `approved` | Yes | — |
| spec-run 1 | 2 Mode | `--mode waves` given | Yes | — |
| spec-run 1 | 3 Scope | 1.1, 1.2, 3.1, 3.2 (`--optional` keeps `*`) | Yes | — |
| spec-run 1 | 4 Graph | `check-tasks` PASS | Yes | Output below |
| spec-run 1 | 5 wave 0 | 1.1 `[-]`, 1 Agent call → done → `[x]` | Yes | `textkit/slug.py` |
| spec-run 1 | 5 wave 1 | 1.2 `[-]`, 1 Agent call → done → `[x]`. Group 1 → `[x]` | Yes | `textkit/unique.py` |
| spec-run 1 | 5 checkpoint 2 | Ran README test cmd. Green → `[x]` | Yes | `1 passed` |
| spec-run 1 | 5 wave 2 | 3.1 and 3.2 `[-]`, 2 Agent calls in ONE message. Both done → `[x]`. Group 3 → `[x]` | Yes | 7 + 6 tests |
| spec-run 1 | 5 checkpoint 4 | Ran README test cmd. Green → `[x]` | Yes | `14 passed` |
| spec-run 1 | 7 Report | No `[-]` left | Yes | `grep` marks |
| (manual) | Step 3 | `sed` "at most 50 characters" → 40 in `requirements.md` (1.3, 2.3). `.spec.json` untouched | n/a | diff below |
| spec-sync | 1 Load | `drift` output pasted below | Yes | DRIFT/CHANGED/stale seen |
| spec-sync | 2 Upstream | design `stale` → edited 5 lines 50 → 40, `SPEC draft design`, gate Approve, `SPEC approve design` | Yes | design `approved` |
| spec-sync | 3 Coverage | Matrix below | Yes | — |
| spec-sync | 4 Evidence | Checked `[x]` leaves that cite 1.3 or 2.3 | Yes, but one verdict wrong | Evidence table below |
| spec-sync | 5 Propose | Table, Q&A #3 → Apply all | Yes | — |
| spec-sync | 6 Apply | Edited 3 lines in leaf text. Unticked 1.1, group 1, checkpoints 2 and 4. `SPEC approve tasks` | Yes | `check-tasks` PASS. No `stale` |
| spec-run 2 | 1 Load | `drift` → NO DRIFT. All `approved` | Yes | — |
| spec-run 2 | 3 Scope | Only 1.1 (`[ ]`). 3.2 is `[x]*` | Yes | — |
| spec-run 2 | 5 wave 0 | 1.1 `[-]` → Agent → done → `[x]`. Group 1 → `[x]` | Yes | `MAX_LEN = 40` at `textkit/slug.py:4` |
| spec-run 2 | 5 checkpoint 2 | README test cmd: **red**, 1 failed 13 passed. I ticked early by mistake, then reverted | No | `test_truncate_has_no_trailing_hyphen` |
| spec-run 2 | Stop | Script "checkpoint red → Stop" | n/a | Checkpoints 2 and 4 `[ ]` |

### `spec.py drift` at the start of spec-sync (pasted)

```
DRIFT requirements requirements.md
STALE design
STALE tasks
CHANGED 1.3
CHANGED 2.3
RESULT: DRIFT
```

State after: `requirements: approved`, `design: stale`, `tasks: stale`. The old `DRIFT tasks` did not print because `tasks` was already `stale` (loop skips non-`approved`).

### Routing test (before step 3)

Copy of `.spec.json` with `tasks: draft`. spec-run step 1: `drift` → `RESULT: NO DRIFT`. A phase is not `approved` → stop. Route table (`shared/state.md`): `pending` or `draft` → `/sdd:spec-new slugify` (resume). Message is right. `.spec.json` restored from copy; `drift` → NO DRIFT; tasks `approved`.

### Hand edit

```
25c25 3. THE Slugifier SHALL return a Slug of at most 50 characters ...  →  40
37c37 3. THE Slug_Allocator SHALL return a Slug of at most 50 characters, including the suffix.  →  40
```

### `check-tasks` outputs (run 1 start; run 2 start and after sync were identical)

```
PASS graph is last section
PASS graph JSON parses
PASS wave ids 0..n in order
PASS graph ids are leaves
PASS every leaf in exactly one wave
PASS deps name leaves
PASS deps in earlier waves
PASS every leaf has Files
PASS every leaf has Kind
PASS every leaf has _Requirements:_
PASS optional * only on Kind test
PASS same-wave leaves touch disjoint files
PASS test leaf deps on a code leaf
PASS pin leaf has Expect red|green
PASS every criterion cited
PASS cited ids exist
PASS every property has a leaf
PASS final top-level task is checkpoint
RESULT: PASS
```

`check-tasks` checks structure only. It does not check ticks. I checked ticks with `grep`.

### Tick state

| Point | Groups | Checkpoints |
|---|---|---|
| After run 1 | 1 `[x]`, 3 `[x]` | 2 `[x]`, 4 `[x]` |
| After sync | 1 `[ ]`, 3 `[x]` | 2 `[ ]`, 4 `[ ]` |
| After run 2 (stopped) | 1 `[x]`, 3 `[x]` | 2 `[ ]` (red), 4 `[ ]` |

Checkpoint command run: `uv run --no-project --with pytest --with hypothesis python -m pytest` (README, `workspace/README.md`). Typecheck: none (README says "none configured"; checkpoint text says `typecheck: none`). No ambiguity this time.

### spec-sync coverage matrix

| Criterion | Leaves citing | Design component | Class |
|---|---|---|---|
| 1.1 | 1.1, 3.1 | Slugifier | covered |
| 1.2 | 1.1, 3.1 | Slugifier | covered |
| 1.3 | 1.1, 3.1 | Slugifier | **changed** |
| 1.4 | 1.1, 3.1 | Slugifier | covered |
| 1.5 | 1.1, 3.1 | Slugifier | covered |
| 2.1 | 1.2, 3.2 | Slug_Allocator | covered |
| 2.2 | 1.2, 3.2 | Slug_Allocator | covered |
| 2.3 | 1.2, 3.2 | Slug_Allocator | **changed** |
| 2.4 | 1.2, 3.2 | Slug_Allocator | covered |
| 2.5 | 1.2, 3.2 | Slug_Allocator | covered |

Orphans: none. Uncovered: none.

### spec-sync evidence table (leaves that cite 1.3 or 2.3)

| Leaf | Evidence | Verdict I gave | Right verdict |
|---|---|---|---|
| 1.1 | `slug.py:4` `MAX_LEN = 50` ≠ new 1.3 | todo (untick) | todo |
| 1.2 | `unique.py:12` uses `MAX_LEN - len(suffix)` | done | done (value comes from 1.1) |
| 3.1 | `grep 50` found nothing; tests use `MAX_LEN` | done | **partial**: `test_slugify.py:31-33` hard-codes `"a"*49` |
| 3.2 | `test_unique_slug.py` uses `MAX_LEN` throughout | done | done |

My `grep "50"` missed the literal `49`. The skill step 4 asks "code matches the current criterion text?" and leaves the method open.

## Scripted Q&A

| # | Question (as the skill would ask) | Options | Answer | Scripted? |
|---|---|---|---|---|
| 1 | Quick Plan questions (1 call, 4 Qs): non-ASCII handling? empty title result? type of `existing`? test library? | Free text | "ASCII via NFKD; empty → 'untitled'; existing is set[str]; Hypothesis" | Yes |
| 2 | Quick Plan final question | Approve all · Analyze requirements · Refine | Approve all | Yes |
| 3 | spec-sync design gate (after refinement) | Approve · Request changes | Approve | Yes ("Approve all") |
| 4 | spec-sync step 5 proposal | Apply all · Pick · Cancel | Apply all | Yes |
| 5 | spec-run 2 checkpoint red | Continue · Stop | Stop | Yes |
| — | spec-run mode | not asked (`--mode waves`) | — | — |

## Artifact checks

| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| requirements.md | 2–7 criteria per requirement, numbered `N.M` | Pass | 5 + 5 criteria |
| requirements.md | Each criterion one EARS pattern, one SHALL, ≤40 words | Pass | Ubiquitous, Event, Unwanted. Longest ≈ 28 words |
| requirements.md | Every term in Glossary | Pass | Slugifier, Slug_Allocator, Slug, Title, Existing_Set |
| requirements.md | Every input has bound or format | Pass | Title any Unicode string; `set[str]`; length bound 50 |
| requirements.md | Failure/edge criterion for input | Pass | 1.4 (empty), 2.5 (empty set) |
| requirements.md | No unmeasured adjectives | Pass | none |
| design.md | Every criterion maps to component or property | Pass | `_Requirements:_` on 2 components |
| design.md | Interface sketch per component | Pass | 2 signatures |
| design.md | Error Handling for each external dependency | Pass | none exist; stated |
| design.md | ≥1 Mermaid diagram | Pass | flowchart |
| design.md | File tree as `diff` | Pass | — |
| design.md | Call tree as `diff` per changed control flow | Pass | slugify, unique_slug |
| design.md | Criteria Classification lists every criterion | Pass | 10 rows |
| design.md | Testing Strategy lists every Property | Pass | 4 rows, ≥100 |
| design.md | Non-functional constraint has owner | Pass (n/a) | none |
| tasks.md | `check-tasks` RESULT: PASS | Pass | output above |
| Property tests | Tag `Feature: slugify, Property N: <title>` | Pass | `test_slugify.py:37,46`; `test_unique_slug.py:41,53` |
| Property tests | ≥100 iterations | Pass | `@settings(max_examples=100)` ×4 |

## Extra checks

**Same-wave runners.** Wave 2 had 3.1 and 3.2, 2 Agent calls in one message. Files disjoint (`tests/test_slugify.py` / `tests/test_unique_slug.py`). Both import modules that earlier waves wrote; `deps` forced that order. No clash, no read/write race. Each runner ran its own test file only (7 and 6 tests). Runner reports arrived as messages after each call returned.

**Wave rules.** Wave 0: 1.1. Wave 1: 1.2. Wave 2: 3.1, 3.2. Code leaves were serial because 1.2 imports 1.1. Parallelism was only in the test wave.

**`[-]` revert.** No runner failed, so the revert rule was not exercised. No `[-]` left after either run.

**Final state.** `len(slugify('a'*45))` = 40; `len(unique_slug('a'*45, {'a'*40}))` = 40. Full suite: 13 passed, 1 failed (`test_truncate_has_no_trailing_hyphen`: expects `"a"*49`, gets `"a"*40`). The test is stale, not the code.

## Issues

| ID | Severity | Plugin file:line | Problem | Proposed fix |
|---|---|---|---|---|
| 06v2-1 | high | `shared/scripts/spec.py:40,110-115`; `skills/spec-run/SKILL.md:22-23` | `sha()` hashes all bytes of `tasks.md`. spec-run owns `tasks.md` and ticks boxes. After run 1, `drift` printed `DRIFT tasks tasks.md` with no real edit. It also re-hashes and prints once. Each spec-run, spec-sync and spec-new resume starts with a false drift. A real hand edit of `tasks.md` during a run hides in the same noise. | Hash `tasks.md` with checkbox marks normalized (`[x]`, `[-]` → `[ ]`). Or ignore `tasks.md` in `drift` and use `check-tasks` only. |
| 06v2-2 | med | `skills/spec-sync/SKILL.md:20-21` | Step 4 says check `[x]` leaves that cite a changed criterion, but gives no method. A grep for the old value misses literals such as `49`. A wrong "done" verdict leaves a stale test ticked and gives a red checkpoint. | Rule: untick every `[x]` leaf that cites a `CHANGED` id, unless `Verify` was re-run green on the new text. Or: run each such leaf's `Verify` and read the criterion text against the test body. |
| 06v2-3 | low | `skills/spec-sync/SKILL.md:22` | Step 5 lists "untick leaf" only. Group lines and checkpoints are not mentioned. I unticked group 1 and both checkpoints. A checkpoint that ran before the fix is stale evidence. | Add: untick the group of an unticked leaf and every checkpoint after it. |
| 06v2-4 | low | `skills/spec-new/SKILL.md:14`; `shared/workflows/quick-plan.md:5-9` | Resume says "jump to step 5 at first phase not `approved`". Quick Plan has no per-phase gate. For `tasks: draft` the route table sends the user to `/sdd:spec-new`, but no Quick Plan step says what to do with existing drafts (step 1 would re-ask the questions). | In `quick-plan.md`, add: drafts exist → skip to step 3 (final question). |
| 06v2-5 | low | `skills/spec-run/SKILL.md:23` | "Red → show output, ask Continue \| Stop" has no rule for which leaf to untick or fix. After Stop, leaf 3.1 stays `[x]` while its test fails. | On red: tell the user which test failed and name the leaf that owns the file (`Files`). Offer untick. |
| 06v2-6 | low | `shared/artifacts/tasks.md:25,70` | Checkpoint title still ends with "ask user on questions". `spec-run` asks the user only on red. The phrase has no executor. | Drop the phrase or define it in `spec-run` step 5. |

## Ambiguity log

- "Checkpoint, once every group above it is done" (`spec-run:23`) → checkpoint 2 runs after wave 1 (group 1 done), checkpoint 4 after wave 2. In run 2 with scope {1.1}, I ran checkpoint 2 only, because I had unticked both and group 3 was already `[x]`. Reading B (run 4 also) would give the same red.
- "Check every unchecked leaf, plus every `[x]` leaf citing a changed criterion" (`spec-sync:20`) → I read it as a judgement per leaf (code and test body vs. new text). I used `grep`. That produced the wrong verdict for 3.1 (06v2-2).
- "Untick leaf (`[x]` no longer matches)" → I also unticked group 1 and the two checkpoints (06v2-3).
- Design stale before `tasks` → spec-sync step 2 says "propose refinement, gate". I edited all `50` in design.md and used the gate.md flow (`SPEC draft design` then `SPEC approve design`). Scripted answer "Sync → Apply all" mapped to Approve.
- "Checkpoint red → Stop" (script) vs "Counterexample → fix implementation" (script) → the red is an example test, not a property counterexample. I used Stop.
- Run 2 ticked checkpoint 2 before reading the result (my error, reverted). Not a plugin issue.

## Metrics

- Questions asked: 5 (Quick Plan Qs, Approve all, design gate, sync Apply all, checkpoint red) · Subagent dispatches: 5 (4 in run 1: 3 messages; 1 in run 2) · Gates: 1 (sync design) · Tests run: run 1 final 14 pass / 0 fail; run 2 final 13 pass / 1 fail.

## v0.1.0 issues

| Old ID | Status | Evidence |
|---|---|---|
| 06-1 hand edit not detected | fixed | `spec.py drift` printed `DRIFT requirements`, `STALE design`, `STALE tasks`, `CHANGED 1.3`, `CHANGED 2.3` with `.spec.json` unchanged by hand. Phases showed `stale` |
| 06-2 sync cannot propagate value change | fixed (residual: 06v2-2) | Sync built a `changed` class, edited design and leaf text, unticked 1.1. Run 2 scope = {1.1}, changed `slug.py:4` to 40, `len(slugify('a'*45))` = 40. My `done` verdict on test leaf 3.1 was wrong; the skill gives no method |
| 06-3 spec-run routing for draft/pending | fixed | Tasks forced to `draft` → step 1 stops, route table gives `/sdd:spec-new slugify`. `stale` → `/sdd:spec-sync` (`shared/state.md:37-38`; `spec-run/SKILL.md:13`) |
| 06-4 groups/checkpoints never ticked | fixed (residual: 06v2-6) | `spec-run/SKILL.md:22-23`. After run 1 groups 1, 3 and checkpoints 2, 4 were `[x]` |
| 06-5 test/typecheck command unclear | fixed | Checkpoint title holds the README command and `typecheck: none` (`shared/artifacts/tasks.md:25`). I ran it with no guess |
| 06-6 reader/writer race in a wave | fixed (rule); race not seen | `shared/artifacts/tasks.md:31` adds "reads or imports → deps". 3.1 and 3.2 sat after their code leaves; `check-tasks` PASS |
| 06-7 runner test scope vague | fixed | `agents/spec-task-runner.md` step 3: "Run `Verify` (your test files only)". 3.1 and 3.2 ran only their own file |
| 06-8 `Task` vs `Agent`, wait for reports | fixed | `allowed-tools` lists `Agent, Task`. `spec-run/SKILL.md:20` "Wait for every report before marking" |
| 06-9 setup leaf forced citation | fixed (text); not exercised | `shared/artifacts/tasks.md:18` has `_Requirements: none (setup)_`. My spec had no setup leaf |
| 06-10 unnamespaced commands | fixed | `/sdd:spec-sync` (`spec-run:16`), `/sdd:spec-new` in route table, `/sdd:spec-run` in `quick-plan.md:11` |
| 06-11 "read only the chosen file" | fixed | `spec-new/SKILL.md:24`: "read files it links when a step reaches them" |

REPORT: /Users/baodang/Documents/code/agent-skills/docs/sdd-eval/v0.2.0/06-lifecycle-sonnet/report.md RESULT: PARTIAL ISSUES: 6
