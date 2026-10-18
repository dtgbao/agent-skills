# 06-lifecycle-sonnet

Model: Sonnet · Skills run: spec-new (Quick Plan), spec-run, spec-sync, spec-run · Result: PARTIAL

Spec name: `slugify-unique-slug`. Workspace: `workspace/docs/specs/slugify-unique-slug/`.

## Summary

- Quick Plan, wave run 1 and the checkpoints worked. 8 leaves ran in 3 waves. 13 tests passed. No `[-]` mark was left.
- **Key finding: the manual edit (50 → 40) was NOT detected.** `.spec.json` still showed `approved` for all phases after the edit. Only `/spec-analyze` sets `stale` (`spec-analyze/SKILL.md:20`). `spec-sync` reads only that flag (`spec-sync/SKILL.md:18`). It has no other way to see a text edit.
- `spec-sync` found "all covered, no unchecked leaf". It proposed zero changes. `.spec.json` and `tasks.md` stayed byte-identical. Run 2 had an empty scope and ran nothing.
- End state is inconsistent. `requirements.md` says max 40. `design.md`, `slug.py` and `tests/test_prop_slug_format.py` say 50. `slugify("a"*45)` returns 45 characters, which breaks new criterion 1.5. The tests are green.
- Parallel runners: no file conflict, no flaky run. One runner saw `slug.py` in a half-edited state (see 06-6). The `spec-run` advice "point to `/spec-sync`" is wrong for `pending` and `draft` (06-3).

## Step trace

| Skill | Step | Action taken | Done-when held | Evidence |
|---|---|---|---|---|
| spec-new | 1 Name | `slugify-unique-slug`. `docs/specs/` did not exist | Yes | `ls docs/specs` → no such dir |
| spec-new | 2 Size | Not trivial, continue | n/a | — |
| spec-new | 3 Workflow | Input says "Quick Plan" → chosen, no question | Yes | — |
| spec-new | 4 State | `.spec.json` written, all `pending` | n/a | `order` = requirements, design, tasks |
| spec-new | 5 / quick-plan 1 | Questions logged, scripted answers used | Yes | Q&A #1. Assumptions listed in Introduction |
| quick-plan | 2 Draft | 3 files written, phases `draft` | After 1 fix | First design draft failed "Testing Strategy lists every property". Fixed. Graph JSON parses; 8 leaves in 8 wave slots |
| quick-plan | 3 Approve | Q&A #2 → Approve all → all `approved` | Yes | `.spec.json` |
| spec-run (1) | 1 Load | tasks `approved` → continue | Yes | — |
| spec-run (1) | 2 Mode | `--mode waves` given, no question | Yes | — |
| spec-run (1) | 3 Scope | 8 leaves (5 optional included) | Yes | `--optional` |
| spec-run (1) | 4 Graph | Wave rules hold | Yes | w0: 1.1, 2.1 · w1: 2.2, 4.1, 4.2, 4.3 · w2: 4.4, 4.5. Files disjoint per wave |
| spec-run (1) | 5 wave 0 | Marked 2 `[-]`. 2 Agent calls in one message. Both `done` → `[x]` | Yes | 1.1: pyproject. 2.1: slug.py |
| spec-run (1) | 5 wave 1 | Marked 4 `[-]`. 4 Agent calls in one message. All `done` → `[x]` | Yes | `grep -c '\[-\]'` → 0 |
| spec-run (1) | 5.5 checkpoint 3 | Groups 1, 2 complete → ran tests. No typecheck script | Yes (tests) | 7 passed |
| spec-run (1) | 5 wave 2 | Marked 2 `[-]`. 2 Agent calls in one message. Both `done` → `[x]` | Yes | 13 passed (runner 4.4) |
| spec-run (1) | 5.5 checkpoint 5 | Ran tests | Yes | 13 passed |
| spec-run (1) | 7 Report | All 8 leaves `[x]` | Yes | Groups 1, 2, 4 and checkpoints 3, 5 stay `[ ]` (06-4) |
| (manual) | Step 3 | `sed 's/50/40/g'` on `requirements.md`. 3 lines changed (Intro, 1.5, 1.7) | n/a | `.spec.json` unchanged |
| spec-sync | 1 Load | Read `.spec.json` + 3 files. Stale phases: none | Yes, but wrong | all `approved` |
| spec-sync | 2 Upstream | No stale phase → skip | Vacuous | — |
| spec-sync | 3 Coverage | Matrix built. 13 covered, 0 uncovered, 0 orphan | Yes | Matrix below |
| spec-sync | 4 Evidence | 0 unchecked leaves → empty table | Vacuous | Evidence below |
| spec-sync | 5 Propose | Empty proposal. Q&A #3 → Apply all | Yes | — |
| spec-sync | 6 Apply | Nothing to apply. `tasks` already `approved` | Yes | `.spec.json` and `tasks.md` identical to before (diff) |
| spec-run (2) | 1–4 | Same as run 1. Scope = 0 leaves | n/a | `grep -cE '^  - \[ \]'` → 0 |
| spec-run (2) | 5 | Every wave ∩ scope is empty. No dispatch. Ran tests at checkpoints (reading A) | Vacuous | 13 passed |
| spec-run (2) | 7 Report | Empty table. Done-when true by vacuity | Vacuous | Code still has `MAX_LEN = 50` |

### spec-sync coverage matrix (criterion ↔ leaf refs ↔ design component)

| Criterion | Leaves citing it | Design component | Class |
|---|---|---|---|
| 1.1 | 1.1, 2.1, 4.3 | slugify | covered |
| 1.2 | 2.1, 4.1, 4.2 | slugify | covered |
| 1.3 | 2.1, 4.1, 4.2 | slugify | covered |
| 1.4 | 2.1, 4.1, 4.2 | slugify | covered |
| 1.5 | 2.1, 4.1, 4.2 | slugify | covered |
| 1.6 | 2.1, 4.1, 4.2 | slugify | covered |
| 1.7 | 2.1, 4.1, 4.2 | slugify | covered |
| 2.1 | 2.2, 4.4 | unique_slug | covered |
| 2.2 | 2.2, 4.4 | unique_slug | covered |
| 2.3 | 2.2, 4.4 | unique_slug | covered |
| 2.4 | 2.2, 4.5 | unique_slug | covered |
| 2.5 | 2.2, 4.4 | unique_slug | covered |
| 2.6 | 2.2, 4.4 | unique_slug | covered |

Orphan leaf refs: none. Orphan design refs: none. The matrix is id-only. It cannot see that criterion 1.5 changed from 50 to 40.

### spec-sync evidence table

| Leaf | Files exist | Symbols exported | Tests exist and pass | Verdict |
|---|---|---|---|---|
| (none) | — | — | — | No unchecked leaf. Table is empty |

Tests run by spec-sync: none. The skill said "run those files only". There was nothing to run. I did not run any test in step 4. I read "unchecked leaf" as `N.M` leaves (reading A, see Ambiguity log).

For information only (not in the skill): the checked leaves are stale against the new text. Criterion 1.5 says ≤ 40. `slug.py:4` has `MAX_LEN = 50`. `test_prop_slug_format.py:18` asserts `<= 50`. `design.md` lines 10, 21, 70, 106 say 50.

## Scripted Q&A

| # | Question (as the skill would ask) | Options | Answer | Scripted? |
|---|---|---|---|---|
| 1 | Quick Plan questions (one call, 4 questions): (a) How to handle non-ASCII characters? (b) What does an empty or all-symbol title return? (c) What type is `existing`? (d) Which stack and test library? | Free text per question (the skill gives no option list) | "ASCII only: NFKD-normalize, drop non-ASCII. Empty or all-symbol title → 'untitled'. existing is set[str]. Stack: Python stdlib, Hypothesis for properties." | Yes |
| 2 | Quick Plan final question | Approve all · Analyze requirements · Refine | Approve all | Yes |
| 3 | spec-sync step 5 (empty proposal) | Apply all · Pick · Cancel | Apply all | Yes |
| — | spec-run mode | not asked, `--mode waves` given | — | — |
| — | spec-run failure / checkpoint red | not asked, no failure, no red | — | — |

## Artifact checks

| Artifact | Done-when item | Pass/Fail | Evidence |
|---|---|---|---|
| requirements.md | Every requirement has ≥1 criterion, numbered N.M | Pass | 2 requirements, 7 + 6 criteria |
| requirements.md | Each criterion: one EARS pattern, one behavior, one assertion | Pass | Event, Ubiquitous, Unwanted forms. 1.2 mixes charset and lowercase (one assertion: regex), accepted |
| requirements.md | Every term in Glossary | Pass | textkit, slugify, unique_slug, Title, Slug, Existing |
| requirements.md | Every input has bound or format | Pass | Title `str` 0–10000. `existing` `set[str]` 0–10000 entries (Introduction) |
| requirements.md | Every happy path has an edge criterion | Pass | 1.6, 1.7, 2.5, 2.6 |
| requirements.md | No unmeasured adjectives | Pass | grep: none |
| design.md | Every criterion maps to a component or property | Pass | `_Requirements:_` on both components. Matrix above |
| design.md | Every external dependency has Error Handling | Pass | No external dependency. Section states so |
| design.md | Every component has interface sketch | Pass | Two signatures |
| design.md | ≥1 Mermaid diagram | Pass | flowchart in Architecture |
| design.md | File tree as `diff` block | Pass | File/Folder Structure |
| design.md | Component call tree as `diff` block | Pass | slugify, unique_slug |
| design.md | Testing Strategy lists every property | **Fail, then fixed** | First draft said "one file per property" without listing. Fixed to 5 explicit lines |
| design.md | Non-functional constraint has owner | Pass (n/a) | None |
| tasks.md | Every criterion cited by ≥1 leaf | Pass | Matrix |
| tasks.md | Every leaf in exactly one wave | Pass | Script: leaf set = wave set, no duplicate |
| tasks.md | Every leaf names its files | Pass | — |
| tasks.md | Graph JSON parses | Pass | `json.loads` OK |
| tasks.md | Wave rules (ids from 0, deps earlier, disjoint files, config first) | Pass | Wave listing in step trace |
| tasks.md | Checkpoint after each layer, never in graph | Pass | Groups 3 and 5, not in JSON |
| Property tests | Tag comment `Feature: <spec>, Property N: <title>` | Pass | All 5 files line 1. Example below |
| Property tests | ≥100 iterations | Pass | `max_examples` = 100 (P1, P2, P3, P5), 200 + 100 (P4) |

Test header (`tests/test_prop_slug_format.py`):

```python
# Feature: slugify-unique-slug, Property 1: Slug format
# Validates: Requirements 1.2, 1.3, 1.4, 1.5, 1.6, 1.7
import re

from hypothesis import given, settings
from hypothesis import strategies as st

from textkit.slug import slugify

@settings(max_examples=100)
```

## Extra checks

**Waves and parallel runners**
- All leaves of each wave were dispatched in one message. Wave 0: 2 calls. Wave 1: 4 calls. Wave 2: 2 calls.
- Same-wave files were disjoint: w0 `pyproject.toml` / `slug.py`; w1 `slug.py` / 3 test files; w2 2 test files. No write conflict.
- No flaky run. No test run failed. Runner counts: 1.1 → 1 passed; 2.1 → 1; 2.2 → 1; 4.1 → 2 (own file only); 4.2 → 2 (own file only); 4.3 → 7 (full suite); 4.5 → 10 (full suite); 4.4 → 13 (full suite).
- Race seen: runner 4.2 reported that `slug.py` had `slugify` only, with no `unique_slug`. Runner 2.2 was editing the same file in the same wave. The rule "disjoint files" does not cover a reader against a writer.
- The Agent calls returned at once and ran in the background. Reports arrived later as messages. The skill has no "wait for all reports" instruction.

**`[-]` marks**
- No runner failed, so no revert was needed. The revert rule (`spec-run/SKILL.md:29`) was not exercised.
- `[-]` count after run 1: 0. After run 2: 0. Group lines and checkpoints stay `[ ]` after a full run.

**Typecheck**
- `spec-run/SKILL.md:31` says "test + typecheck scripts from manifest". `pyproject.toml` has no scripts and no type checker. The README says "Typecheck: none configured". I ran the pytest command only and skipped typecheck. The skill has no "skip if absent" text.

**Step 1 advice "point to `/spec-sync`"**
- `stale`: right. `spec-sync` clears it.
- `draft`: wrong. `spec-sync` step 6 would set `approved` with no gate and no user review. The right pointer is the gate (`shared/gate.md`) or `/spec-new` resume.
- `pending`: wrong. `tasks.md` does not exist. `spec-sync` step 1 reads three artifacts and has nothing to sync. The right pointer is `/spec-new <name>` (resume).
- The name is `/spec-sync` here, but the plugin command is `/sdd:spec-sync`.

**Final test output** (`uv run --no-project --with pytest --with hypothesis python -m pytest -v`, after run 2):

```
collected 13 items

tests/test_prop_ascii_only.py::test_cjk_suffix_is_dropped PASSED         [  7%]
tests/test_prop_ascii_only.py::test_examples PASSED                      [ 15%]
tests/test_prop_idempotent.py::test_slugify_idempotent PASSED            [ 23%]
tests/test_prop_idempotent.py::test_examples PASSED                      [ 30%]
tests/test_prop_slug_format.py::test_slug_format PASSED                  [ 38%]
tests/test_prop_slug_format.py::test_examples PASSED                     [ 46%]
tests/test_prop_unique_pure.py::test_unique_slug_does_not_mutate_existing PASSED [ 53%]
tests/test_prop_unique_pure.py::test_unique_slug_does_not_mutate_when_base_taken PASSED [ 61%]
tests/test_prop_unique_pure.py::test_examples PASSED                     [ 69%]
tests/test_prop_unique_smallest.py::test_unique_slug_smallest_free PASSED [ 76%]
tests/test_prop_unique_smallest.py::test_empty_existing_returns_base PASSED [ 84%]
tests/test_prop_unique_smallest.py::test_examples PASSED                 [ 92%]
tests/test_words.py::test_word_count PASSED                              [100%]

============================== 13 passed in 0.97s ==============================
```

Green tests, but the code violates the edited requirement (`slugify("a"*45)` → 45 chars, limit 40).

## Issues

| ID | Severity | Plugin file:line | Problem | Proposed fix |
|---|---|---|---|---|
| 06-1 | high | `shared/state.md:16-19`, `skills/spec-sync/SKILL.md:18`, `skills/spec-analyze/SKILL.md:20` | A manual edit of an approved artifact is not detected. Only `spec-analyze` writes `stale`. `state.md:19` says only spec skills write state, so a hand edit never sets it. `spec-sync` step 1 lists only `stale` phases. The user sees "nothing to sync" after a real change. | Store a content hash per artifact in `.spec.json` at approval (`"hashes": {...}`). In `spec-sync` step 1 and `spec-run` step 1, compare hashes. A mismatch → mark later phases `stale` and name the changed file. Update `state.md:18-19`. |
| 06-2 | high | `skills/spec-sync/SKILL.md:21-23` | Even with detection, sync cannot propagate a value change. The matrix is id-only. Step 4 checks only unchecked leaves. Done leaves (`slug.py`, tests) that no longer match the criterion are never re-checked. A re-run then does nothing. | Add: when a criterion text changed, un-tick every leaf that cites it (or add a "re-verify" leaf). In step 3, compare criterion text against design and code. Step 7 of `spec-run` should say "scope empty → report nothing to run". |
| 06-3 | med | `skills/spec-run/SKILL.md:15` | "Tasks not approved → point to `/spec-sync`" is right only for `stale`. `draft` should go to the gate. `pending` should go to `/spec-new` resume. `/spec-sync` step 6 would approve a `draft` with no gate. | Branch on phase: `stale` → `/sdd:spec-sync`; `draft` → gate; `pending` → `/sdd:spec-new <name>`. |
| 06-4 | med | `skills/spec-run/SKILL.md:25-31`, `shared/artifacts/tasks.md:11` | No step ticks group lines or checkpoints. After a full run, groups 1, 2, 4 and checkpoints 3, 5 stay `[ ]`. Checkpoint text says "ask user on questions", but `spec-run` asks only when red. | In step 5.5, say: group → `[x]` when all its in-scope leaves are `[x]`; checkpoint → `[x]` when green. Define the user question for a green checkpoint, or drop it from the title. |
| 06-5 | med | `skills/spec-run/SKILL.md:31` | "Run test + typecheck scripts from manifest" has no rule for an absent script. `pyproject.toml` has no scripts. The model must guess the test command. The README holds the command, the manifest does not. | Say: read the test and typecheck command from the README or manifest. If absent, skip and list "typecheck: none" in the report. |
| 06-6 | med | `skills/spec-run/SKILL.md:28`, `shared/artifacts/tasks.md:17-19` | The "disjoint files" rule does not cover a reader against a writer. Wave 1 had test leaves 4.1–4.3 importing `slug.py` while leaf 2.2 rewrote it. Runner 4.2 saw `slug.py` without `unique_slug`. No failure this time. | Add to the wave rules: a leaf must not read a file that another leaf in the same wave writes. Or put test leaves one wave after every leaf that touches the module they import. |
| 06-7 | low | `agents/spec-task-runner.md:13` | "Run test files tied to your change" is vague. 4.1 and 4.2 ran only their own file. 4.3, 4.4 and 4.5 ran the full suite. | Say "run your test file(s) only" or "run the full suite" — pick one. |
| 06-8 | low | `skills/spec-run/SKILL.md:6,28` | `allowed-tools` lists `Task`. The tool name in this harness is `Agent`. Agent calls run in the background, and the skill has no instruction to wait for all reports before step 3. | Name the tool as "Task/Agent". Add "wait for every report before marking". |
| 06-9 | low | `shared/artifacts/tasks.md:8` | "Leaf ends with `_Requirements:_`" forces a citation on a setup leaf with no requirement. Leaf 1.1 (pyproject) cites 1.1, which is unrelated. This makes the coverage matrix show 1.1 as covered by it. | Allow `_Requirements: none (setup)_`. Matrix ignores it. |
| 06-10 | low | `shared/workflows/quick-plan.md:11`, `skills/spec-run/SKILL.md:15,18` | Commands are written `/spec-run`, `/spec-sync`. The installed names are `/sdd:spec-run`, `/sdd:spec-sync`. | Use the namespaced form. |
| 06-11 | low | `skills/spec-new/SKILL.md:26`, `shared/artifacts/design.md:9` | Step 5 says "Read only the chosen file". The design Done-when needs `visuals.md` and `correctness.md`. A literal model skips them. I read both because the Done-when list points to them. | Say "read the chosen file; read files it links when drafting". |

## Ambiguity log

- "List `stale` phases" (`spec-sync:18`) → read `.spec.json` only → the skill gives no other detection method. Result: none found.
- "Every unchecked leaf" (`spec-sync:23`) → leaves are `N.M` lines (reading A). Groups and checkpoints are not leaves. Reading B (checkpoints count) has no files or tests to check, so it would give no verdict either.
- "Checkpoint whose earlier groups all complete" (`spec-run:31`) → run after the wave that completes those groups. Checkpoint 3 ran after wave 1. Checkpoint 5 ran after wave 2. In run 2, I ran the tests at both even with no dispatch (reading A). Reading B (skip when the wave is empty) would run nothing.
- "Typecheck scripts from manifest" (`spec-run:31`) → none exist → skipped, listed here.
- "Test files tied to your change" (`spec-task-runner:13`) → each runner chose its own scope (own file or full suite).
- Max length vs `unique_slug` suffix → the limit applies to `slugify` only; the suffix goes on top. Recorded as an assumption in `requirements.md`.
- Step 3 manual edit → changed all three "50" in `requirements.md` (Intro, 1.5, 1.7). A real user would likely do the same.
- Scripted Q&A #1 → the skill gives no option lists for Quick Plan questions. I wrote 4 questions and mapped the one scripted answer to all four.
- Spec-sync with an empty proposal → the skill still says ask Apply all | Pick | Cancel. I asked and took "Apply all" (scripted).
- A model that reads `requirements.md` (40) and `design.md` (50) in the same step 1 might notice the gap by chance. No step tells it to compare. I did not use this path; I followed the literal text.

## Metrics

- Questions asked: 3 calls (Quick Plan questions ×1, Approve all ×1, spec-sync Apply all ×1) · Subagent dispatches: 8 (3 messages) · Gates: 0 (Quick Plan has none) · Tests run: final 13 pass / 0 fail. No failing run at any point.
