# sdd eval harness

Rules for every eval session. The session brief gives the scenario. This file gives the method.

## Paths

- Plugin root (`PLUGIN`): `<repo>/plugins/sdd`
- Fixtures: `PLUGIN/evals/fixtures/<fixture>/`. Briefs: `PLUGIN/evals/briefs.md`.
- Run dir: `<repo>/docs/sdd-eval/v<plugin version>/`. Scenario dir (`SCN`): `<run dir>/<scenario-id>/`.
- Workspace (`WS`): `SCN/workspace/` = copy of the fixture. This is the "project root" for the skill. Specs go to `WS/docs/specs/<name>/`.

## Hard limits

1. Write only under `SCN`. `PLUGIN` and other scenario dirs stay read-only.
2. Do not commit. Do not switch branch. Do not run `git add`.
3. Run Python with `uv run --no-project --with pytest --with hypothesis python -m pytest` from `WS`.

## How to run a skill

You simulate a user typing `/sdd:<skill> <args>`.

1. Read `PLUGIN/skills/<skill>/SKILL.md`. Replace `$ARGUMENTS` with the args. Replace `${CLAUDE_PLUGIN_ROOT}` with `PLUGIN`.
2. Follow the steps literally, as a model that sees only that text would. Read a shared file only when a step tells you to read it. Do not use knowledge of plugin files that the step did not load.
3. Honor `allowed-tools` from the frontmatter. If a step needs a tool that is not in the list, log it as an issue, then continue.
4. Scripted user. Do NOT call AskUserQuestion. Each time the skill says to ask the user, log the full question with its options, then take the answer from the brief's script. No script line fits → choose the most conservative option, mark it `UNSCRIPTED`.
5. Subagents. Pass the brief's answer key to no subagent. When a step dispatches `spec-analyst` or `spec-task-runner`, use the Agent tool (`subagent_type: general-purpose`, same model as you). Prompt = the full body of `PLUGIN/agents/<agent>.md` (with `${CLAUDE_PLUGIN_ROOT}` replaced) + the caller inputs. Tell it to use only the tools in the agent's `tools:` line and to work in `WS`. Parallel dispatch = all Agent calls in one message. Run every Agent call in the foreground and wait for its report; a background dispatch can stall the session.

## What to check at each step

- Did the step have a checkable Done-when? Did it hold? Give evidence (file, line, command output).
- Was the instruction ambiguous? Which reading did you take?
- Did files disagree with each other (state values, names, paths, formats)?
- For each drafted artifact: check every item in its `Done when:` list. Pass or fail, with evidence.

## Report

Write `SCN/report.md`. Use ASD-STE100 Simplified Technical English: short sentences, active voice, one idea per sentence. No filler. Use this structure:

```markdown
# <scenario-id>

Model: <model> · Skills run: <list> · Result: PASS | PARTIAL | FAIL

## Summary
<3–5 bullets: what worked, what broke>

## Step trace
| Skill | Step | Action taken | Done-when held | Evidence |

## Scripted Q&A
| # | Question (as the skill would ask) | Options | Answer | Scripted? |

## Artifact checks
| Artifact | Done-when item | Pass/Fail | Evidence |

## Issues
| ID | Severity (high/med/low) | Plugin file:line | Problem | Proposed fix |

## Ambiguity log
- <instruction text> → <reading taken> → <why>

## Metrics
- Questions asked: n · Subagent dispatches: n · Gates: n · Tests run: pass/fail counts
```

Plugin line numbers: cite the line in `PLUGIN` (use `grep -n`). Issue IDs: `<scenario-number>-<n>`, e.g. `03-2`.

When done, end your final message with one line: `REPORT: <path to report.md> RESULT: <PASS|PARTIAL|FAIL> ISSUES: <count>`.
