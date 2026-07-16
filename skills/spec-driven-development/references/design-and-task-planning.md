# Design and Task Planning

Use this reference while writing `design.md` or `tasks.md`. Ground both artifacts in the repository and approved upstream decisions so an engineer with little local context can implement the work without inventing architecture, interfaces, or verification steps.

## Contents

- [Shared Gate](#shared-gate)
- [Writing `design.md`](#writing-designmd)
- [Writing `tasks.md`](#writing-tasksmd)

## Shared Gate

Confirm the spec covers one focused capability or defect. When independent subsystems remain bundled together, return to scope clarification and split them before planning. Each resulting spec must produce useful, testable behavior on its own.

Inspect the affected code, tests, configuration, and repository instructions before naming paths, symbols, dependencies, or commands. Follow established patterns unless an approved decision explicitly changes them.

## Writing `design.md`

### Map the Repository

Identify the files or modules that own the affected behavior before choosing components:

- Record which existing units change and what responsibility each retains.
- Name new units only when they create a clear boundary or independently testable responsibility.
- Keep files that change together near each other when repository conventions allow it.
- Prefer focused files over large units that combine unrelated responsibilities.
- Include a targeted split when an affected file has become an obstacle to the approved change; leave unrelated restructuring outside the design.

The repository map is design evidence, not a speculative file inventory. Every listed location must contribute to an approved requirement, bugfix boundary, or validation need.

### Define Boundaries and Interfaces

For each component, state:

- Its responsibility and collaborators
- Its repository location
- The public API, schema, command, event, or internal contract it consumes and produces
- Relevant parameter, return, field, and error types
- Ownership of state, resources, transactions, and lifecycle
- The requirement or bugfix identifiers it validates

A component boundary is ready when a reader can explain what it does, how to use it, and what it depends on without reading its internals. Keep naming and types consistent across components and later tasks.

### Explain Behavior and Failure Handling

Describe control flow and data flow from entry point through dependencies. Cover concurrency, retries, partial failure, recovery, compatibility, and observability only where they materially apply. Preserve unchanged bugfix behavior explicitly.

Use diagrams for relationships or state transitions that are materially clearer visually. Keep straightforward sequences in prose.

### Design the Testing Strategy

Map each important behavior and correctness property to the smallest useful test layer:

- Unit tests for focused logic and contracts
- Integration tests for boundaries, persistence, APIs, or events
- End-to-end tests for critical journeys
- Regression tests for reproduced defects and unchanged behavior

Prefer real behavior over mock interactions. Identify seams that make test-first implementation practical without adding production APIs solely for tests.

### Review the Design

Before approval:

1. **Coverage:** Every requirement or bugfix boundary maps to a concrete design decision and validation strategy.
2. **Repository fit:** Paths, interfaces, dependencies, and commands come from inspected code.
3. **Consistency:** Component names, types, and data flow agree throughout the artifact.
4. **Failure behavior:** Important errors and recovery paths have explicit handling.
5. **Scope:** Every component serves the focused spec.
6. **Placeholder scan:** Replace every placeholder, `TBD`, `TODO`, vague instruction, and unresolved choice.

Resolve each finding inline before validation and user approval.

## Writing `tasks.md`

Start from approved, synchronized upstream artifacts. Lock the file and interface structure before decomposing tasks so neighboring tasks agree on paths, symbols, and contracts.

### Right-Size Tasks

A task is the smallest unit that carries its own verification cycle and merits an independent review gate.

- Fold setup, configuration, scaffolding, generated artifacts, and documentation into the behavior task that needs them.
- Split tasks where one outcome could be accepted while another is rejected.
- End every task with an independently observable result.
- Keep a complete test cycle within the same behavior task as its production change.
- Use a checkpoint only for integration evidence across completed behavior tasks.

Within a behavior task, keep each action small and ordered:

1. Write one focused failing test.
2. Run it and confirm the expected failure.
3. Implement the minimum behavior that makes it pass.
4. Run the focused and relevant regression tests.
5. Refactor while tests remain green.

### Record Exact Implementation Context

Each task must give its implementer enough information to act without rediscovery:

- Exact files to create, modify, and test
- Existing symbols or interfaces it consumes
- New or changed signatures, schemas, events, or commands it produces
- The behavior boundary and requirement or bugfix identifiers it covers
- Exact verification commands and expected failure or success output
- Required setup or fixtures owned by the task

Include concise signatures, schemas, assertions, or pseudocode when they prevent ambiguity. Keep the design artifact as the source of truth for architecture; avoid duplicating full implementations that would drift before execution.

### Preserve Dependency Clarity

Represent the same acyclic dependencies three ways:

- JSON execution waves
- An ASCII dependency tree
- A task-to-dependencies table

Every task identifier must appear consistently. A task may enter a wave only after every dependency appears in an earlier wave. Tasks in one wave must be safe to execute concurrently without shared files, mutable state, or unresolved interface decisions.

### Use One Accepted Task Form

Use the scaffolded structure for every required and optional task.

**Behavior task**

```markdown
- [ ] 1. <Observable outcome>
  - **RED:** <Focused test and behavior>
  - **Verify RED:** Run `<command>`; expect <failure caused by missing behavior>.
  - **GREEN:** <Smallest implementation boundary>
  - **Verify GREEN:** Run `<command>`; expect <success and relevant regressions to remain green>.
  - **REFACTOR:** <Cleanup or explicit no-cleanup decision>, then rerun `<command>`.
  - _Requirements: <identifiers> or Bugfix: <identifiers>_
```

**Approved TDD exception**

```markdown
- [ ] 2. [TDD Exception] <Outcome>
  - **Reason:** <Why test-first does not apply>
  - **Approval:** <Where the user explicitly approved the exception>
  - **Check:** Run `<command>`; expect <observable result>.
  - _Requirements: <identifiers> or Bugfix: <identifiers>_
```

Use this form only for an explicit user-approved exception such as throwaway exploration, generated output, or configuration-only work.

**Integration checkpoint**

```markdown
- [ ] 3. Checkpoint — <Integrated outcome>
  - **Check:** Run `<integration command>`.
  - **Expected:** <Observable successful result and warning expectations>.
  - _Requirements: <covered identifiers> or Bugfix: <covered identifiers>_
```

### Eliminate Plan Failures

Replace these with concrete content before approval:

- `TBD`, `TODO`, “implement later,” or “fill in details”
- “Add appropriate error handling,” “add validation,” or “handle edge cases” without named behavior
- “Write tests” without the test target, command, and expected result
- “Similar to Task N” instead of restating the task-local contract
- Code steps that omit the path, symbol, or interface being changed
- References to types, functions, or methods no task or existing file defines
- Commands without expected failure or success evidence

### Review the Task Plan

Before approval:

1. **Spec coverage:** Every required upstream identifier is implemented and verified by at least one required task.
2. **Dependency agreement:** JSON waves, tree, and table express the same acyclic graph.
3. **Interface consistency:** Names, paths, types, and schemas match the design and neighboring tasks.
4. **TDD structure:** Every behavior task has the complete ordered cycle; every exception records approval; every checkpoint has an expected result.
5. **Placeholder scan:** No vague or incomplete instruction remains.
6. **Execution readiness:** Every task has exact context and verification evidence.

Resolve findings inline, validate `tasks.md`, and obtain the phase's required approval. Then return to the main instructions for implementation of approved tasks.
