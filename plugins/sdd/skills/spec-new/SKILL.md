---
name: spec-new
description: "Start or resume a spec: requirements, then design and plan, with user gates. Feature or bugfix."
argument-hint: "[feature or bug description | spec-name] [--quick]"
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash, AskUserQuestion, Agent, Task
---

Input: $ARGUMENTS.

You are the main session. Keep your context small: subagents write the spec, and `spec.py` checks it. Do not read `spec.md` in full, and do not write it yourself. The terms have the meanings in `${CLAUDE_PLUGIN_ROOT}/shared/glossary.md`; read it only if a term is not clear.

- `SPEC` = `python3 ${CLAUDE_PLUGIN_ROOT}/shared/scripts/spec.py`
- `WRITE(task, text)` = an Agent call with `subagent_type: sdd:spec-writer`, `model: sonnet`, `effort: medium`, in the foreground. The prompt holds: the spec dir, the task, the text, and the paths `${CLAUDE_PLUGIN_ROOT}/shared/spec-format.md` and `${CLAUDE_PLUGIN_ROOT}/shared/scripts/spec.py`. The reply is a short report: WROTE, COUNTS, OPEN, KEY, CHECK.

## Steps

1. Route.
   - If the input names a directory in `docs/specs/`, run `SPEC status <dir>` and resume at the gate that it names.
   - If the input is empty, use the confirmed `spec-brainstorm` playback in this conversation. If there is none, ask what to build or fix.
   - If the change is a typo or one line, tell the user that a spec is not necessary. Make the change, then stop.
2. Clarity. If the input is not a confirmed playback, read `${CLAUDE_PLUGIN_ROOT}/skills/spec-brainstorm/SKILL.md` and do its step 1. If the input is vague or ambiguous, do the other steps of that skill too.
   - Done when: the input is a defect report, or the brief is clear, or the user confirmed the playback, or the user said "skip".
3. Name and workflow. Make a kebab-case name of 5 words or fewer. The workflow is `bugfix` for a defect report or an input that starts with `Bugfix:`, else `feature`. If `docs/specs/<name>/` exists, ask: Resume | New name. Run `SPEC init docs/specs/<name> <workflow>`.
4. Requirements. `WRITE(requirements, <input, or the playback, word for word>)`.
5. Gate 1. Show the WROTE, COUNTS and KEY lines and the path of `spec.md`. Then ask with ONE AskUserQuestion call:
   - one question for each OPEN item (4 or fewer in each call; the recommended answer first, marked `(Recommended)`);
   - a last question: "Approve the requirements with these answers?" Approve | Change.

   Then:
   - If the user chose Change, ask what to change, then `WRITE(update, <the words of the user>)`, show the new report and ask again.
   - If the user chose Approve, go to step 6 with the answers.
   - With `--quick`: do not ask. Go to step 6 with the recommended answers, and say that they are assumptions.
6. Design and plan, in ONE writer call: `WRITE(design, "Answers: <the answers, or none>")`. The writer applies the answers to the Requirements, then writes Design and Plan. Then run `SPEC approve <dir> requirements`. If it prints `REFUSED`, give the line to `WRITE(update, …)` and run it again.
7. Gate 2. Show the COUNTS and KEY lines. Ask: Approve | Change. For Change, do as in step 5. For Approve, run `SPEC approve <dir> design`.
8. Hand off. Run `SPEC ready <dir>` and show its WAVE lines. Tell the user to type `/sdd:spec-run <name>`.

Done when: `SPEC status <dir>` prints `NEXT: /sdd:spec-run`.
