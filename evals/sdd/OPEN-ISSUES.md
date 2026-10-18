# sdd: open issues

As of round 0.4.1 (2026-10-18). One list, duplicates merged. Source ids point to the run reports: `v0.3.2` P*, `v0.3.3` L*, `v0.3.4` run issues (f1 / b1 / a1 I*), `v0.4.1` run issues (07a / 07b / 07c I*).

## Medium

| # | Where | Problem | Proposed fix | Source |
|---|---|---|---|---|
| Q1 | `skills/spec-analyze/SKILL.md:17`, `agents/spec-analyst.md:56` | `CHECK` is a self-report. In 0.3.4, 7 findings said pass but failed when counted | Orchestrator recounts gaps, `SHALL` and assertions per option and ignores `CHECK` on a mismatch. Analyst lists the assertions inside `CHECK` | v0.3.4 a1 I1, f1 I2 |
| Q2 | same | The `CHECK` target `gaps=1 shall=1 asserts=1` fails every correct `NEEDS_OWNER` finding | Separate target for owner findings: `gaps=1 owner=sole` | v0.3.4 a1 I2, f1 I1 |
| Q3 | `skills/spec-analyze/SKILL.md:19` | Cross-check by shared term misses check-order clashes between rejection rules (a1 F16–F20, 2 left open) | For each changed rejection criterion, list the other rejection criteria that can match the same input; the spec must state their order | v0.3.4 a1 I3 |

## Low (for owner review)

| # | Where | Problem → proposed fix | Source |
|---|---|---|---|
| L1 | `skills/spec-analyze/SKILL.md` step 4 | Apply can push a requirement past 7 criteria → split or supersede, log it | v0.3.3 L1 |
| L2 | `agents/spec-analyst.md` | A and B both reserve new numbers, so gaps appear after A is chosen → number only A; B reuses A's id | v0.3.3 L2 |
| L3 | `agents/spec-task-runner.md` | NOTES `file:line`: Haiku cites wrong lines; new files have no `git diff` → cite from `git diff -U0`, or `grep -n` for new files | v0.3.3 L4, v0.3.4 f1 I5, b1 I3 |
| L4 | `shared/gate.md` | Count line and Analyze-first threshold (">8 requirements") have no bugfix form → `bugfix.md: N current, N expected, N unchanged`; threshold by criteria | v0.3.2 P11, v0.3.3 L5, v0.3.4 b1 I1, I2 |
| L5 | `shared/artifacts/bugfix-design.md` | Root-cause `file:line` not checked → `grep -n` each cite before the gate | v0.3.3 L6, v0.3.4 b1 I4 |
| L6 | `shared/artifacts/bugfix-design.md` | Interface-level criterion forced into a property → allow example-only criteria | v0.3.3 L7 |
| L7 | `skills/spec-analyze/SKILL.md` | Growth: owner answers add interfaces that create new failure paths; growth metric counts one-assertion splits; split advice has no gate option | v0.3.2 P9, v0.3.3 L8 |
| L8 | `skills/spec-analyze/SKILL.md` step 3 | `NEEDS_OWNER` ask has no defined options → `Answer | Defer`, prefer Defer when the answer adds an interface the code lacks | v0.3.2 P10 |
| L9 | `skills/spec-analyze/SKILL.md` | Deferred proposals keep criterion numbers that later clash → deferred items hold no number | v0.3.3 L9 |
| L10 | `shared/state.md` | zsh variable warning easy to miss → show one copy-paste command form; "never put `python3` in a variable" | v0.3.3 L10 |
| L11 | `skills/spec-run/SKILL.md:23` | Checkpoint below only skipped `*` leaves: rule works but does not say it runs and ticks | v0.3.2 P12 |
| L12 | `agents/spec-task-runner.md:13` | Runner Done-when "every cited id has a check in your Verify" cannot hold for code leaves tested by a later test leaf → "…or is cited by a `Kind: test` leaf that deps on this leaf" | v0.3.2 P13, v0.3.4 f1 I3 |
| L13 | `skills/spec-sync/SKILL.md` step 5 | Confirmed `SUSPECT` leaf does not get the changed criterion text in its runner prompt → add the changed id to that leaf's prompt | v0.3.4 f1 I4 |
| L14 | `shared/gate.md` | High/medium Open Questions after the last VERIFY are parked with no ask → list them at the gate with their options | v0.3.4 f1 I6 |
| L15 | `agents/spec-task-runner.md:15` | Runner fixed its own generator after a red run (counterexample was invalid input) instead of stopping → allow a test-only fix when the input is outside the precondition; report it as `fixed test: <input>` | v0.3.4 a1 I4 |
| L16 | `agents/spec-analyst.md:15` | `FOCUSED` has no rule for real medium FAILURE/EDGE gaps → report them as low, or as notes after the findings | v0.3.4 a1 I5 |
| L24 | `skills/spec-brainstorm/SKILL.md` steps 3–4 | Surface (CLI, library, UI) stayed unasked; playback 1 guessed it wrong → in step 3, surface is a frontier question unless input or code fixes it; add `Surface:` to the playback | v0.4.1 07a I1, I2 |
| L25 | `skills/spec-new/SKILL.md` step 4 | Playback `Workflow:` line has no rule to choose Requirements-First vs Design-First when the stack is fixed → Design-First only when stack or architecture is the main constraint | v0.4.1 07a I3 |
| L26 | `skills/spec-brainstorm/SKILL.md` Brief | "A why that follows from the what" is still a judgment → add one example (tag + filter → find related notes) | v0.4.1 07b I1 |
| L27 | `skills/spec-new/SKILL.md` step 2 | Done-when does not require the one-line brief in chat → add "brief shown" | v0.4.1 07b I2 |
| L28 | `shared/workflows/bugfix.md:7` | Facts settled from code reach the user only in `bugfix.md` (step 3) → show them in one line before the ask | v0.4.1 07c I1 |
| L29 | `skills/spec-brainstorm/SKILL.md` Brief | Unclear whether a defect claim the code cannot confirm still counts → a user-reported wrong behavior counts; the Bugfix Investigate step tests it | v0.4.1 07c I2 |

## Not plugin defects

- The slash command does not expand when the app starts a session, so every eval ran skills by manual load. `$ARGUMENTS` and `${CLAUDE_PLUGIN_ROOT}` expansion in skill text are still unverified by a typed command.
- 0.3.4 reused the 0.3.3 sessions, so each orchestrator remembered its earlier run.
- The orchestrators reported "effort low"; the app metadata says medium.
