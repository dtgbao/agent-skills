# Implementation Plan: {{SPEC_TITLE}}

## Overview

<Describe the vertical implementation order, integration checkpoints, and verification approach.>

## Tasks

- [ ] 1. <Required capability outcome>
  - [ ] 1.1 Prove <observable behavior>
    - **RED:** Add `<test path>` with one focused assertion for <missing behavior>.
    - **Verify RED:** Run `<focused command>`; expect <failure caused by the missing behavior>.
    - _Requirements: <1.1> or Bugfix: <EB1, UB1>_
  - [ ] 1.2 Implement <observable behavior>
    - **GREEN:** Implement the approved contract from `design.md` in `<implementation paths or symbols>`.
    - **Verify GREEN:** Run `<focused command>` and `<related regression command>`; expect both to pass.
    - **REFACTOR:** <Cleanup or explicit no-cleanup decision>, then rerun `<focused or related command>`.
    - _Requirements: <1.1> or Bugfix: <EB1, UB1>_

- [ ] 2. Checkpoint — <Integrated vertical slice>
  - **Check:** Run `<integration command>`.
  - **Expected:** <Observable successful result, including warning or failure expectations>.
  - _Requirements: <covered identifiers> or Bugfix: <covered identifiers>_

## Task Dependency Graph

```json
{
  "waves": [
    {
      "wave": 1,
      "tasks": [
        { "id": "1.1", "dependsOn": [] }
      ]
    },
    {
      "wave": 2,
      "tasks": [
        { "id": "1.2", "dependsOn": ["1.1"] }
      ]
    },
    {
      "wave": 3,
      "tasks": [
        { "id": "2", "dependsOn": ["1.2"] }
      ]
    }
  ]
}
```

## Notes

- Tasks marked with `*` are optional and remain incomplete unless explicitly requested.
- Use `[TDD Exception]` only for a user-approved generated, configuration-only, or throwaway outcome. Include Reason, Approval, and Check entries.
- Parent capability tasks contain no implementation prose; their required children determine completion.
- Mark a parent `[x]` only when every required child is `[x]`.

<!-- Replace every example task and graph entry with one consistent plan. Keep architecture, schemas, algorithms, and full contracts in design.md. -->
