---
name: spec-new
description: "Start or resume a spec: Requirements-First, Design-First, Bugfix, or Quick Plan."
argument-hint: "[feature or bug description | spec-name]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, Agent, Task
---

Input: $ARGUMENTS. `SPEC` per `${CLAUDE_PLUGIN_ROOT}/shared/state.md`.

## Steps

1. Route. Input names a dir in `docs/specs/` → Resume: `SPEC drift <dir>`, read `.spec.json`, jump to step 6 at first phase in `order` not `approved`. Input empty → use the confirmed `spec-brainstorm` playback in this conversation; none → ask what to build or fix. No workflow named and typo or one-line change → say spec unneeded, do it direct, stop. Named workflow wins.
   - Done when: resume point known, or new-spec input in hand.
2. Clarity. Input is a confirmed playback → step 3. Else read `${CLAUDE_PLUGIN_ROOT}/skills/spec-brainstorm/SKILL.md`, run its steps on the input.
   - Done when: input is a defect report, brief clear and shown in chat, playback confirmed, or user said skip.
3. Name. Feature or bug noun phrase, kebab-case, ≤5 words, workflow name dropped. `docs/specs/<name>/` exists → ask: Resume (as step 1) | New name.
   - Done when: name unique, or resume point known.
4. Workflow. Input names one → use it. Else ask via AskUserQuestion, options below. Playback recommends one, or input is a defect report (→ Bugfix) → put it first, marked `(Recommended)`.
   - Requirements-First: need clear, architecture open
   - Design-First: stack or architecture is the main constraint. A fixed stack alone → Requirements-First
   - Bugfix: defect, regressions costly
   - Quick Plan: familiar feature, one pass, no gates
   - Done when: workflow chosen.
5. State. `SPEC init docs/specs/<name> <workflow>`.
6. Run workflow. Read the chosen file; read files it links when a step reaches them:
   - Requirements-First → `${CLAUDE_PLUGIN_ROOT}/shared/workflows/requirements-first.md`
   - Design-First → `${CLAUDE_PLUGIN_ROOT}/shared/workflows/design-first.md`
   - Bugfix → `${CLAUDE_PLUGIN_ROOT}/shared/workflows/bugfix.md`
   - Quick Plan → `${CLAUDE_PLUGIN_ROOT}/shared/workflows/quick-plan.md`
   - Done when: workflow's last step done.
