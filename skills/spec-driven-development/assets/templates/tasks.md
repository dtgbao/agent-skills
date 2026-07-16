# Implementation Plan: {{SPEC_TITLE}}

## Overview

<Describe the implementation order, integration strategy, and verification approach.>

---

## Task Dependency Graph

```json
{
	"waves": [
		{ "wave": 1, "tasks": [1] },
		{ "wave": 2, "tasks": [2] },
		{ "wave": 3, "tasks": [3] }
	]
}
```

```text
1 (foundation)
└── 2 (implementation)
    └── 3 (checkpoint)
```

| Task | Depends On |
| ---- | ---------- |
| 1    | —          |
| 2    | 1          |
| 3    | 2          |

---

## Tasks

- [ ] 1. <Required behavior outcome>
  - **RED:** Add `<test path>` with one focused test for <required behavior>.
  - **Verify RED:** Run `<focused test command>`; expect <failure caused by missing behavior>.
  - **GREEN:** Implement the smallest change in `<implementation paths>` that satisfies the failing test.
  - **Verify GREEN:** Run `<focused test command>`; expect it to pass, then run `<related regression command>`.
  - **REFACTOR:** <Remove duplication or state why no cleanup is needed>, then rerun `<focused or related test command>` and expect it to pass.
  - _Requirements: <1.1, 1.2> or Bugfix: <EB1, UB1>_

- [ ]\* 2. [TDD Exception] <Optional generated, configuration-only, or throwaway outcome>
  - **Reason:** <Explain concretely why test-first does not apply to this task.>
  - **Approval:** <Record the user's explicit approval of this exception.>
  - **Check:** Run `<verification command>`; expect <observable successful result>.
  - _Requirements: <optional requirement identifier>_

- [ ] 3. Checkpoint — <Integrated behavior>
  - **Check:** Run `<integration command>`.
  - **Expected:** <Describe the successful result, including relevant warning or failure expectations.>
  - _Requirements: <covered identifiers>_

---

## Notes

- Tasks marked with `*` are optional and remain incomplete unless explicitly requested.
- Use `[TDD Exception]` only for a user-approved exception recorded in the task.
- Mark a task `[x]` only after its complete TDD cycle or stated checkpoint/exception check passes.

<!-- Replace the example waves, tree, dependency table, and tasks with one consistent, acyclic, complete plan. Preserve one accepted task form per task and remove every placeholder before approval. -->
