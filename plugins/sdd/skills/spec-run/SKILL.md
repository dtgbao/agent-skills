---
name: spec-run
description: "Build an approved spec: one lane-runner subagent per lane, in parallel waves, each driven by spec.py one test at a time."
argument-hint: "<spec-name> [lane] [--inline] [--model haiku|sonnet] [--effort low|medium|high]"
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash, AskUserQuestion, Agent, Task
---

Arguments: $ARGUMENTS. `SPEC` = `python3 ${CLAUDE_PLUGIN_ROOT}/shared/scripts/spec.py`. Keep your context small: do not read `spec.md`, the code or the diffs. The script and the runners do that.

## Steps

1. Ready. Run `SPEC ready docs/specs/<name>`. If it prints `NOT READY`, show its lines and the command that it names, then stop. If it prints `NOTHING TO RUN`, stop. Else note the WAVE lines. If the arguments name a lane, run only that lane.
2. Run each wave in order.
   - Start one Agent call for each lane of the wave, all in ONE message, in the foreground: `subagent_type: sdd:lane-runner`. The prompt is one line: `Run: python3 ${CLAUDE_PLUGIN_ROOT}/shared/scripts/spec.py tdd docs/specs/<name> <lane>`.
   - Model and effort from the lane tier: S = `haiku`; M = `sonnet`, `effort: low`; L = `sonnet`, `effort: medium`. The script drives each step, so a low tier is sufficient. `--model` and `--effort` replace these values for all lanes. Never use a model or an effort above sonnet high.
   - `--inline`, or no Agent tool: do not start subagents. Run the command of each lane yourself and do the loop of `${CLAUDE_PLUGIN_ROOT}/agents/lane-runner.md`.
   - After the wave, run `SPEC verify docs/specs/<name> <lanes of the wave>` one time.
3. Results. For each lane that `verify` does not show as `DONE`:
   - `COUNTEREXAMPLE`: show it. Ask: Fix code | Fix test | Fix requirement. For Fix code or Fix test, start the lane again with one more line in the prompt: the choice and the counterexample. For Fix requirement, stop; the user edits `spec.md` and runs `/sdd:spec-sync <name>`.
   - `OPEN`, or a reply with `STATUS: failed | blocked`: start the lane again one tier up (haiku, sonnet low, sonnet medium, sonnet high). The script keeps the progress, so the lane continues at its open case. With `--model` or `--effort`, the retry also goes one step up from those values. After 2 attempts, show the cause and ask: Retry | Skip lane | Stop.
   - A `SUITE: FAIL` line names the lane of each failing test. Start that lane again, with the failing test name in the prompt.
   Start the next wave only when all lanes that it needs are `DONE`.
4. Report. Run `SPEC verify docs/specs/<name>`. Show its output, and one line for each lane: tier, model, attempts.

Done when: `verify` prints `RESULT: PASS`, or the user stopped.
