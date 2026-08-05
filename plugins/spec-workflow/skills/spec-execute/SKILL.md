---
name: spec-execute
description: Implement one task (or the next available task) from an approved tasks.md. Use when the user says "/spec-execute", "implement task N", "start the next task", or "work on the spec" for a feature that already has an approved tasks.md.
argument-hint: "<feature-slug> [task number]"
---

# Spec Execute

Requirements, design, and tasks should already be approved before this runs.
If `docs/specs/<slug>/tasks.md` doesn't exist, stop and tell the user to
run `spec-tasks` first.

## 0. Load context

Read `docs/steering/*.md` if present, then `design.md` and `tasks.md`
for the spec, plus whichever of `requirements.md` (feature spec) or
`bugfix.md` (bugfix spec) exists — that file, if requirements.md, tells you
*why* and *what counts as done*; if bugfix.md, it tells you what the fix
must achieve and what it must not break. Design tells you *how* either
way. All three files (upstream doc + design.md + tasks.md) are required.

## 1. Pick the task

- If a task number was given in `$ARGUMENTS` (e.g. `2.3`), use that task,
  whether it's a subtask or a checkpoint.
- Otherwise, use the `## Task Dependency Graph` waves to find candidates:
  the earliest wave that still has an unchecked task in it. Within that
  wave, take the first unchecked task by list order.
- **Skip optional (`- [ ]*`) tasks when auto-selecting** — only run one if
  the user explicitly names it or has already said they want optional tasks
  included for this spec.
- If the requested task's dependencies (per the wave graph) aren't complete
  yet, tell the user which task(s) need to happen first instead of
  implementing out of order.

Announce which task you're starting and a one-line plan before making
changes.

## 2. Implement

**If the task is a Checkpoint task:**
Run the project's test suite (and linter/typecheck if the task or steering
docs mention them). Report pass/fail plainly. If anything fails, fix it or
stop and explain what's blocking before checking the box — don't check off
a checkpoint on a red suite. If everything passes, ask the user if they have
questions before continuing, per the task's own instructions.

**If the task is a normal or property-test subtask:**
- Follow the design doc's architecture and interfaces for this task; don't
  improvise a different approach without flagging it.
- Follow conventions in `docs/steering/tech.md` / `structure.md` where
  present.
- Write the code, and write/update tests per the design's testing strategy
  and the task's own notes.
- For property-test tasks specifically: implement the generators and
  assertion exactly as specified, use the stated minimum iteration count,
  and include the tag comment verbatim so it's greppable later.
- Run the test suite / linter for the affected code if the project has one
  available, and fix failures before considering the task done.
- Keep the change scoped to this task. If you discover the task needs
  something tasks.md didn't anticipate, do the minimum needed to complete it
  correctly, and flag the gap to the user rather than silently expanding
  scope into other tasks.

## 3. Mark complete and report

Once implemented and verified:

1. Update `docs/specs/<slug>/tasks.md`, changing this task's `- [ ]` to
   `- [x]` (or `- [x]*` if it was optional). If every subtask under a parent
   task is now checked, check the parent too.
2. Summarize what changed (files touched, what was implemented, test
   results).
3. Say what the next available task is (per the dependency graph), and ask
   whether to continue or stop here. **Do not automatically start the next
   task** — one task per run unless the user explicitly asked to run all
   tasks.

If the user does ask to run all remaining tasks, work through them one at a
time following the wave order, still reporting and marking each one complete
before starting the next, and stop immediately if a task or checkpoint
fails.
