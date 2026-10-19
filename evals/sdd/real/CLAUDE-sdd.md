# Eval mode: sdd plugin

This project is an automated test of the installed `sdd` plugin (project scope). No human answers questions.

1. **Script.** Your first message names the Script file and the RUN ARGS. Read the Script yourself. Run its commands in order. You cannot invoke a `/sdd:` command yourself: read the skill at `/Users/baodang/Documents/code/agent-skills/plugins/sdd/skills/<skill>/SKILL.md`, with `${CLAUDE_PLUGIN_ROOT}` = `/Users/baodang/Documents/code/agent-skills/plugins/sdd` and `$ARGUMENTS` = the Script args, and follow it.
2. **Scripted user.** Never call AskUserQuestion. When a skill says to ask, take the answer from the Script. If no answer fits, use the most conservative option and mark it `UNSCRIPTED` in `eval/notes.md`.
3. **Subagents.** Use the Agent tool exactly as the skill says (`sdd:spec-writer`, `sdd:lane-runner`, with the model and effort it names).
4. **Logs.** Keep them minimal: in `eval/notes.md`, one line for each command with its start and end time (`date +%T`), and one line for each UNSCRIPTED answer. Write nothing else under `eval/`.
5. Do not commit. Do not edit files under `/Users/baodang/Documents/code/agent-skills`.

End with one line: `DONE: <commands run> · <final verify RESULT line>`.
