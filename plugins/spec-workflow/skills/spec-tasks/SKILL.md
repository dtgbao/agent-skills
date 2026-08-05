---
name: spec-tasks
description: Convert an approved requirements.md+design.md, or bugfix.md+design.md, into a discrete, dependency-ordered implementation task list. Use when the user wants to plan tasks for a spec'd feature or bugfix, says "/spec-tasks" or "break this into tasks", or wants to revise an existing tasks.md. Requires design.md to exist first. Pauses for approval before execution begins.
argument-hint: "<feature-slug or bugfix-slug> [notes or revision request]"
---

# Spec Tasks

This is the final phase before implementation for both feature and bugfix
specs. Do not start implementing code in this skill — that happens only in
the separate `spec-execute` skill, after the user approves this task list.

## 0. Load context and determine spec type

Read `docs/steering/*.md` if present. Then check `docs/specs/<slug>/`:

- **Feature spec** (`requirements.md` exists): read `requirements.md` and
  `design.md`. Both are required.
- **Bugfix spec** (`bugfix.md` exists, no `requirements.md`): read
  `bugfix.md` and `design.md`. Both are required.

If either required file is missing, stop and tell the user which earlier
phase to run first.

If `docs/specs/<slug>/tasks.md` already exists, treat `$ARGUMENTS` as a
revision request and preserve the completion state (`[x]`) of any task that
hasn't conceptually changed.

## 1. Read the structure, then the type-specific rules

Read `references/structure.md` for the shared tasks.md shape — hierarchical
parent/subtask numbering, the `[ ]*` optional marker, Checkpoint tasks, and
the Task Dependency Graph. This applies identically to both spec types.

Then read the citation/property-test rules for this spec's type:

- Feature spec → `references/feature-tasks.md`
- Bugfix spec → `references/bugfix-tasks.md`

## 2. Present and gate

Show the full tasks.md content. End with:

> Does this task breakdown look right? Reply with changes, or say "approved"
> to start implementation (`/spec-execute <slug>`).

Wait for explicit approval before treating the spec as ready to execute.

## 3. On approval

Write the final content to `docs/specs/<slug>/tasks.md`. Tell the user
the plan is saved and ready — they can run `spec-execute <slug>` to start
implementing, either one task at a time or by naming a task number.
