---
name: spec-status
description: Show the status of specs created with this workflow — which artifacts each has, task completion progress, and which workflow (Requirements-First, Design-First, Bugfix, or Quick Spec) it's using. Use when the user asks "what's the status of my specs", "show spec progress", "/spec-status", or names a specific slug to check.
argument-hint: "[feature-slug or bugfix-slug]"
---

# Spec Status

Because Design-First specs write `design.md` before `requirements.md`,
"furthest phase" is not a fixed order across all specs — report which
artifacts exist rather than assuming requirements always comes first.

## If no slug is given

List every subdirectory of `.claude/specs/`. For each, determine its type
from which files are present:

- **Feature spec** — has `requirements.md` and/or `design.md`. Report which
  of `requirements.md` / `design.md` / `tasks.md` exist (in whichever order
  they were written), and if `tasks.md` exists, `<completed>/<total>`
  subtasks checked off — count leaf `N.M` subtasks and checkpoint tasks,
  not parent group headers.
- **Bugfix spec** — has `bugfix.md`. Report which of `bugfix.md` /
  `design.md` / `tasks.md` exist, and the same task-completion count if
  `tasks.md` exists.

Keep this to a compact table or list — one line per spec.

If `.claude/specs/` doesn't exist or is empty, say so and mention
`/spec-new` as the place to start.

## If a slug is given

Show that spec in detail, based on its type:

**Feature spec:**
- Which of requirements.md / design.md / tasks.md exist, whether design.md
  includes a `## Correctness Properties` section, and — if only design.md
  exists so far — note this is a Design-First spec awaiting requirements
  derivation (`/spec-requirements <slug>`)
- The full task list from tasks.md with checkbox state, grouped by parent
  task, flagging which are optional (`*`) and which are checkpoints
- Using the `## Task Dependency Graph`, which wave is next and which
  task(s) in it are still unchecked and ready to run via `spec-execute`

**Bugfix spec:**
- Which of bugfix.md / design.md / tasks.md exist
- A one-line summary of Current vs. Expected Behavior from bugfix.md, and
  the Root Cause summary from design.md if it exists
- If tasks.md exists, the same task list / dependency-graph detail as a
  feature spec, noting whether all three required property tests (bug
  reproducible, bug fixed, no regressions) are present and their status
