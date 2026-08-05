---
name: spec-bugfix
description: Start the Bugfix Analysis phase for a bug — phase 1 of 3 (Bugfix Analysis → Design → Tasks). Use when the user reports a bug, asks to "fix this issue", "debug X", or wants a tracked bugfix spec. Produces bugfix.md capturing current (defective), expected (correct), and unchanged (must-not-regress) behavior, and pauses for approval before the design phase.
argument-hint: "<bug description> [reproduction steps, constraints]"
---

# Spec Bugfix — Analysis Phase

This is phase 1 of 3 for a bugfix: **Bugfix Analysis → Design → Tasks**,
mirroring the feature-spec flow but tailored to a surgical fix. Do not
diagnose the root cause or propose a fix in this skill — that's
`spec-design`'s job (Mode C), once this analysis is approved.

## 0. Load context

Read `.claude/steering/*.md` if present, for product/tech/structure
context.

## 1. Identify the bugfix spec

Derive a short kebab-case slug from `$ARGUMENTS` (e.g. "login button does
nothing on Safari" → `login-button-safari`). Check whether
`.claude/specs/<slug>/bugfix.md` already exists.

- **Doesn't exist:** new bugfix. Create `.claude/specs/<slug>/`.
- **Exists and not yet through tasks:** treat `$ARGUMENTS` as new
  information and update the analysis.
- **Exists with an approved design/tasks already:** ask whether this is a
  regression of the same bug (continue this spec) or a genuinely new issue
  that should get its own slug.

## 2. Investigate before writing anything

Don't draft the analysis from the bug report alone. Trace the issue in the
codebase first and get a concrete sense of current behavior. Save deep
root-cause work for the design phase — this phase only needs enough
investigation to state current and expected behavior accurately, not to
explain *why* it's happening yet.

## 3. Draft bugfix.md

```markdown
# Bugfix Analysis: <Short Title>

## Current Behavior (Defect)
- WHEN <condition> THEN the system <incorrect behavior, stated as
  observed fact>

## Expected Behavior (Correct)
- WHEN <condition> THEN the system SHALL <correct behavior>

## Unchanged Behavior (Regression Prevention)
- WHEN <condition> THEN the system SHALL CONTINUE TO <existing correct
  behavior that must be preserved>
```

Guidelines:

- Include repro steps under Current Behavior where applicable.
- List every closely-related behavior you can identify under Unchanged
  Behavior, not just the obvious one — this is what keeps the eventual fix
  surgical instead of a rewrite. Include any explicit constraints the user
  gave (e.g. "don't touch the public API") here too.
- Use plain "the system" (not a formal glossary) unless the codebase
  already has an established name for the component at fault — bugfix
  specs are narrow enough that a full glossary is usually overkill.

## 4. Present and gate

Show the full bugfix.md content. End with:

> Does this capture the bug accurately? Reply with changes, or say
> "approved" to move on to root-cause analysis and a fix design
> (`/spec-design <slug>`).

Wait for explicit approval before considering this phase done.

## 5. On approval

Write the final content to `.claude/specs/<slug>/bugfix.md`. Tell the user
it's saved and that the next step is `/spec-design <slug>` to diagnose the
root cause and propose a fix.
