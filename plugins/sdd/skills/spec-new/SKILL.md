---
name: spec-new
description: "Start or resume a spec: Requirements-First, Design-First, Bugfix, or Quick Plan."
argument-hint: "[feature or bug description | spec-name]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, Agent, Task
---

Input: $ARGUMENTS. `SPEC` per `${CLAUDE_PLUGIN_ROOT}/shared/state.md`.

## Steps

1. Name. Feature or bug noun phrase, kebab-case, ≤5 words, workflow name dropped. Input empty → ask what to build or fix. `docs/specs/<name>/` exists → ask: Resume | New name.
   - Resume → `SPEC drift <dir>`, read `.spec.json`, jump to step 5 at first phase in `order` not `approved`.
   - Done when: name unique, or resume point known.
2. Size. No workflow named and typo or one-line change → say spec unneeded, do it direct, stop. Named workflow wins.
3. Workflow. Input names one → use it. Else ask via AskUserQuestion, options below.
   - Requirements-First: need clear, architecture open
   - Design-First: stack or architecture fixed first
   - Bugfix: defect, regressions costly
   - Quick Plan: familiar feature, one pass, no gates
   - Done when: workflow chosen.
4. State. `SPEC init docs/specs/<name> <workflow>`.
5. Run workflow. Read the chosen file; read files it links when a step reaches them:
   - Requirements-First → `${CLAUDE_PLUGIN_ROOT}/shared/workflows/requirements-first.md`
   - Design-First → `${CLAUDE_PLUGIN_ROOT}/shared/workflows/design-first.md`
   - Bugfix → `${CLAUDE_PLUGIN_ROOT}/shared/workflows/bugfix.md`
   - Quick Plan → `${CLAUDE_PLUGIN_ROOT}/shared/workflows/quick-plan.md`
   - Done when: workflow's last step done.
