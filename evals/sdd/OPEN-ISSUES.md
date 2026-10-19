# sdd: open issues

As of round 0.5.0 (2026-10-19). One list, duplicates merged. Source ids point to the run reports: round 0.4.2 real `f1` / `b1` / `a1` I*, simulated `07a` / `07c` I*; round 0.4.3 `a1-r2` / `f1-r2` I*; round 0.5.0 `f1-slice` I*. Older issue ids (Q1–Q3, L1–L29) are in git history.

## Status of the 0.4.1 list

- Held: Q1 (the recount caught 7 off-target `CHECK` lines), Q3 (2 check-order clashes found), L1 (the past-7 rule split 2 requirements), L4, L5, L7 (`+new` / `+split`), L24–L28.
- Partly held: Q2 → Q5, L8 → L36, L14 → Q8, L16 → Q6, L6 → L42.
- No issue reported, not proven: L2, L3, L9–L13, L15, L29.

## Status of Q4–Q10

Fixed in the plugin text. Round 0.4.3 (Sonnet) confirmed Q5, Q6, Q10 and the Q7/Q8 asks. It also found gaps in the Q4, Q8 and Q9 fixes; those gaps are fixed too. No eval has run on the last fixes. Remove a row below when an eval confirms it.

## Medium

| # | Where | Problem | Proposed fix | Source |
|---|---|---|---|---|
| Q4 | `skills/spec-analyze/SKILL.md:17` | The repair list has no rule for an option with `shall=1` and 2 assertions, an option that closes no gap, or one that closes part of the gap | Option with asserts≠1 or that does not close the gap → drop it; one option left → A \| Defer | a1 I1 |
| Q5 | `agents/spec-analyst.md:59` | `CHECK` said on target for 7 off-target findings. `NEEDS_OWNER` questions ask 2–3 things but say `gaps=1` | `CHECK` names each gap and assertion (`gaps=1 [<gap>]`); one question mark per owner question | a1 I2 |
| Q6 | `agents/spec-analyst.md:15` vs `:27` | `FOCUSED` makes medium FAILURE/EDGE low, but `NEEDS_OWNER` must be ≥ medium. 2 gaps were dropped; one came back in VERIFY | `NEEDS_OWNER` keeps medium in `FOCUSED` | a1 I3 |
| Q7 | `shared/gate.md:6`, `skills/spec-analyze/SKILL.md:22` | Split spec is offered only at a requirements gate. Standalone analyze on approved requirements, then resume → no gate offers it | End of standalone analyze with a split recommendation → ask Split spec \| Continue | a1 I4 |
| Q8 | `shared/gate.md:7`, `skills/spec-analyze/SKILL.md:22` | High/medium Open Questions are asked only on the gate "Analyze first" path. Standalone analyze parks them; design decides them alone | spec-analyze step 5: ask each high/medium item left: Answer \| Keep deferred | a1 I5 |
| Q9 | `agents/spec-task-runner.md:14` | A runner edited a file outside its `Files` for a mutation check during a parallel wave, then restored it | No edit outside `Files`, temporary edits and mutation checks included | a1 I6 |
| Q10 | `shared/correctness.md:10`, `agents/spec-task-runner.md:15` | A property test imported its oracle bound (`PERCENT_MAX`) from the code under test, so a criterion change could not make it fail | Oracle and generator bounds come from the criterion text as literals, never from the code under test | f1 I1 |
| Q11 | `skills/spec-analyze/SKILL.md:17`, `shared/artifacts/requirements.md` | An existing criterion with two `SHALL` was found as low AMBIGUITY and deferred without a question. The gate approved a document that fails its own Done-when | An EARS violation in any criterion is medium; step 4 splits it | f1-r2 I-4 |
| Q12 | `agents/spec-analyst.md:37` | An option contradicted an existing criterion that shares its term; FOCUSED said no findings; VERIFY found it later (2 extra dispatches) | Checklist: an option that contradicts a criterion with a shared term also edits that criterion | f1-r2 I-5 |

## Low (for owner review)

| # | Where | Problem → proposed fix | Source |
|---|---|---|---|
| L30 | `skills/spec-analyze/SKILL.md:19` | Only the upper bound (7) is checked; a removal left a requirement with 1 criterion → below 2 → merge with a related requirement, or log it | a1 I7 |
| L31 | `skills/spec-analyze/SKILL.md:19` | Check-order clash also matches rejections with the same response → clash only when the responses differ | a1 I8 |
| L32 | `skills/spec-analyze/SKILL.md:19` | A split renumbers criteria; the decided-findings map is not updated → pass the old → new id map to the next round | a1 I9 |
| L33 | `skills/spec-analyze/SKILL.md:19` | Open Questions line form not named → point to the skeleton line in `shared/artifacts/requirements.md` | a1 I10 |
| L34 | `agents/spec-analyst.md:54` | Option text holds "(Delete 4.2.)", not criterion text → add `SUPERSEDES: <ids>` per option | a1 I11 |
| L35 | `skills/spec-run/SKILL.md:21` | A retry ran on top of a partial write from a reply with no `STATUS:` → show `git diff` of the leaf's `Files` before Retry, ask Keep \| Revert | a1 I12 |
| L36 | `skills/spec-analyze/SKILL.md:17` | "Defer first" on greenfield work recommended Defer on 4 of 4 owner questions → recommend Defer only when the interface is outside the spec's files or scope | f1 I5 |
| L37 | `shared/gate.md:5` | Growth line: which gates show it is not stated → requirements gate only | a1 I13 |
| L38 | `shared/gate.md:5` | Bugfix design has no Components section, so its count has no rule → count components named in `## Fix` | b1 I1 |
| L39 | `agents/spec-analyst.md:42` | `NEEDS_OWNER` options name a criterion number that the caller then drops → owner options name no number | f1 I2 |
| L40 | `agents/spec-analyst.md:31-35` | Checklist does not check the EARS pattern (state inside a WHEN) → add "each option matches one EARS pattern" | f1 I3 |
| L41 | `skills/spec-analyze/SKILL.md:22` | VERIFY takes criterion ids only; owner answers change Glossary entries → VERIFY takes changed Glossary terms too | f1 I4 |
| L42 | `shared/artifacts/bugfix-design.md:3` | "Error type → example-only" is unclear for a state-dependent raise → example-only = interface only (name, signature, error class for bad input, status mapping) | b1 I3 |
| L44 | `agents/spec-task-runner.md:30-38` | Report has no model field → add `MODEL: <model the agent ran as>` | b1 I2, f1-r2 I-7 |
| L45 | `skills/spec-run/SKILL.md:23` | Due checkpoints with the same command run back to back → run once, tick all | f1 I7 |
| L46 | `shared/scripts/spec.py:123-144` | `SUSPECT` matches numbers only: false hits on cent amounts, and it misses imported constants → also report identifiers that `AFFECTS` leaves define and other leaves import | f1 I6, f1-r2 I-3, f1-slice I2 |
| L47 | `skills/spec-brainstorm/SKILL.md:32` | Surface rule unclear when the code names a surface for other features → ask unless input or code names the surface for this feature | 07a I2 |
| L48 | `skills/spec-brainstorm/SKILL.md:30` | No rule when the user story and the code disagree → state the code fact, ask which one is meant | 07a I3 |
| L49 | `shared/workflows/bugfix.md:7` | Order of "show in chat" vs "state in Introduction" unclear; a fact that names only the wrong result → show in chat now, copy to the Introduction at step 3; Expected is missing then | 07c I1, I2 |
| L50 | `agents/spec-analyst.md:12` | Fix chains: each scoping fix opens the next gap; FOCUSED repeats decided gaps as low → skip a finding that matches a decided gap or a deferred id | a1-r2 I5 |
| L51 | `skills/spec-analyze/SKILL.md:17` | Question-mark count passes compound owner questions ("which key …, and which argument?") → count asks, not question marks | a1-r2 I6, f1-slice I6 |
| L52 | `shared/correctness.md` | A concurrency property passed with the lock removed (threads rarely interleave) → inject a yield point between read and write, or repeat ≥1000 times | a1-r2 I8 |
| L53 | `shared/scripts/spec.py:147` | `drift` prints `DRIFT` only on the first run, so a skill that loads second misses it → print it until `approve`, or print `STALE` every run | f1-r2 I-2 |
| L54 | `shared/scripts/spec.py:330` | In waves mode, group checkpoints run after later-group leaves have landed, so they cannot catch a group regression → order waves by group where files allow | f1-slice I8 |

## Not plugin defects

- The slash command does not expand when the app starts a session, so every eval ran skills by manual load. `$ARGUMENTS` and `${CLAUDE_PLUGIN_ROOT}` expansion in skill text are still unverified by a typed command.
- 0.3.4 reused the 0.3.3 sessions, so each orchestrator remembered its earlier run.
- The orchestrators reported "effort low"; the app metadata says medium.
