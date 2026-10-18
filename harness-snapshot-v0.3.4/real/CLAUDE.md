# Eval mode: sdd plugin test

This project is an automated test of the installed `sdd` plugin (project scope, `sdd@bao-plugins`). No human answers questions. Write all eval output under `eval/`. Prose in short, plain sentences.

## Rules

1. **Commands.** The Script lives outside this project; your first message names its file. Read it yourself. Keep it out of project files and out of subagent prompts: give a subagent only what the skill says. Run the Script commands in order. A turn that starts with `/sdd:<skill> ...` has the skill loaded: follow it. A later command cannot be invoked by you (the skills are user-invoked). Run it by reading the installed skill at `/Users/baodang/Documents/code/agent-skills/plugins/sdd/skills/<skill>/SKILL.md` with `${CLAUDE_PLUGIN_ROOT}` = `/Users/baodang/Documents/code/agent-skills/plugins/sdd` and `$ARGUMENTS` = the Script args. Log each command as `slash` or `manual load` in `eval/commands.md`.
2. **Scripted user.** Never call AskUserQuestion. Each time a skill says to ask, append the question and options to `eval/QA.md`, then take the answer from the Script. No line fits → the most conservative option, marked `UNSCRIPTED`.
3. **Subagents.** Dispatch exactly as the skill says: Agent tool, `subagent_type: sdd:spec-task-runner` or `sdd:spec-analyst`, the `model` the skill names, foreground. Never use `general-purpose` instead. Agent type missing → stop, write that in the report.
4. **Logs.** Per dispatch, append to `eval/dispatch.md`: leaf or round, subagent_type, model passed, attempt, STATUS, and the raw report block. Analyst rounds: save the raw output to `eval/analyst-round-<n>.md`.
5. **Tests.** `uv run --no-project --with pytest --with hypothesis python -m pytest -q`. Do not commit. Do not edit files under `/Users/baodang/Documents/code/agent-skills`.
6. **Report.** Write `eval/report.md`:

```markdown
# <project> eval

Orchestrator: <model, effort> · Result: PASS | PARTIAL | FAIL

## Plugin load
- Slash command expanded? `${CLAUDE_PLUGIN_ROOT}` resolved (paste one resolved path)? Agent types `sdd:spec-task-runner`, `sdd:spec-analyst` available? Frontmatter tools/model applied (what did the agent say it ran as)?

## Summary
<3–6 bullets>

## Step trace
| Skill | Step | Action | Done-when held | Evidence |

## Dispatches
| # | Leaf/round | Size | Model passed | Attempt | Status | Notes |

## Artifact checks
| Artifact | Done-when item | Pass/Fail | Evidence |

## Issues
| ID | Severity | Plugin file:line | Problem | Proposed fix |

## Metrics
- Questions, dispatches per model, retries/escalations, gates, tests pass/fail
```

End your final message with: `REPORT: <path> RESULT: <PASS|PARTIAL|FAIL> ISSUES: <n>`.
