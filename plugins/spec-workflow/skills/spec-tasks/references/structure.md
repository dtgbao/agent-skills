# tasks.md structure (shared by feature and bugfix specs)

## Structure

```markdown
# Implementation Plan: <Feature or Bugfix Name>

## Overview
<Short paragraph: the overall approach and how the steps below build on each
other.>

## Tasks

- [ ] 1. <Parent task group title>
  - [ ] 1.1 <Subtask title>
    - <Implementation detail or sub-step>
    - <Implementation detail or sub-step>
    - _<citation line — see type-specific reference file>_

  - [ ]* 1.2 <Optional subtask, e.g. a unit test>
    - <Implementation detail>
    - _<citation line>_

- [ ] 2. Checkpoint — Ensure all tests pass
  - Run <the project's test command> and verify all tests pass. Ask the user
    if any questions arise before proceeding.

- [ ] 3. <Next parent task group title>
  - [ ] 3.1 ...

## Notes
<Bullets: meaning of the `*` marker, any dev dependency that must be
installed before certain tasks (e.g. a property-testing library), any
testability seam that must stay in sync with real logic, and what the
checkpoint tasks are for.>

## Task Dependency Graph

​```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2", "2.1"] }
  ]
}
​```
```

## Guidelines

- **Group with parent tasks, implement in subtasks.** A top-level numbered
  item (`1.`, `2.`, ...) is a named group; the actual actionable, checkable
  work lives in its `N.M` subtasks. Check off a parent only once every
  subtask under it is checked.
- Each subtask should be small enough to implement and verify in one
  focused pass, but complete enough to be independently testable — avoid
  both "rewrite the whole feature" tasks and "rename one variable" tasks.
- **Mark genuinely optional work with `- [ ]*`** (asterisk immediately
  after the checkbox) — typically standalone unit/property tests that
  improve confidence but don't block the feature from working. Don't mark
  anything load-bearing as optional.
- **Insert checkpoint tasks** as their own top-level item (no subtasks, no
  citation line) after a natural chunk of work — at minimum before the
  final task and after the first substantial chunk of implementation.
  Their job is "run the test suite / linter, confirm it's green, ask the
  user if anything's unclear before continuing."
- Include tasks for tests, not just implementation, unless the user's
  steering docs say otherwise.
- Don't include non-coding tasks (e.g. "deploy to prod", "get design
  sign-off") unless the user specifically wants them tracked here.
- **Build the `## Task Dependency Graph` last**, after the task list is
  final. Group subtask IDs into waves: tasks with no unmet dependencies on
  each other share a wave (and can run in any order/in parallel); a task
  depending on another goes in a later wave. This is the single source of
  truth for ordering — don't also scatter dependency notes through
  individual tasks.
