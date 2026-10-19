---
name: spec-sync
description: "Realign a spec after hand edits: update the affected cases, approve, and reopen them for spec-run."
argument-hint: "<spec-name>"
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash, AskUserQuestion, Agent, Task
---

Spec: $ARGUMENTS. `SPEC` = `python3 ${CLAUDE_PLUGIN_ROOT}/shared/scripts/spec.py`. `WRITE` is as in `${CLAUDE_PLUGIN_ROOT}/skills/spec-new/SKILL.md`.

## Steps

1. Run `SPEC drift docs/specs/<name>`. If it prints `NO DRIFT`, run `SPEC status` and stop.
2. `WRITE(update, <the drift output>, "Update the cases, Properties and Decisions for each CHANGED, ADDED or REMOVED criterion. Each `OLD VALUE … criterion` or `… Design/Plan` line is text that still holds the old value: update it so that the spec agrees. `OLD VALUE … <file>` lines are hints for the cases.")`.
3. Show the WROTE and KEY lines. Ask: Approve | Change. For Change, do as in `spec-new` step 5.
4. Run `SPEC approve docs/specs/<name> requirements design`. The script reopens each case whose text or criterion changed. Run `SPEC ready docs/specs/<name>` and show its WAVE lines. Tell the user to type `/sdd:spec-run <name>`.

Done when: `SPEC drift` prints `NO DRIFT`.
