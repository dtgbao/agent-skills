---
name: spec-new
description: "Start a spec: Requirements-First, Design-First, Bugfix, or Quick Plan."
argument-hint: "[feature or bug description]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

Input: $ARGUMENTS

## Steps

1. Name. Kebab-case from input. Input empty → ask what to build or fix. `docs/specs/<name>/` exists → ask: resume or new name.
   - Done when: name unique.
2. Size. Typo or one-line change → say spec unneeded, do it direct, stop.
3. Workflow. Input names one → use it. Else ask via AskUserQuestion, options below. Done when: workflow chosen.
   - Requirements-First: need clear, architecture open
   - Design-First: stack or architecture fixed first
   - Bugfix: defect, regressions costly
   - Quick Plan: familiar feature, one pass, no gates
4. State. Create dir + `.spec.json` per `${CLAUDE_PLUGIN_ROOT}/shared/state.md`.
5. Run workflow. Read only the chosen file:
   - Requirements-First → `${CLAUDE_PLUGIN_ROOT}/shared/workflows/requirements-first.md`
   - Design-First → `${CLAUDE_PLUGIN_ROOT}/shared/workflows/design-first.md`
   - Bugfix → `${CLAUDE_PLUGIN_ROOT}/shared/workflows/bugfix.md`
   - Quick Plan → `${CLAUDE_PLUGIN_ROOT}/shared/workflows/quick-plan.md`
