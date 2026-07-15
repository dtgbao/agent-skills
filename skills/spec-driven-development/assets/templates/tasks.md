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

- [ ] 1. <Required task outcome>
  - <Implementation boundary or concrete deliverable>
  - <Smallest check that proves the outcome>
  - _Requirements: <1.1, 1.2> or Bugfix: <EB1, UB1>_

- [ ]\* 2. <Optional task outcome>
  - <Implementation boundary or concrete deliverable>
  - <Smallest check that proves the outcome>
  - _Requirements: <optional requirement identifier>_

- [ ] 3. Checkpoint — <Integrated behavior>
  - Run `<command>` and resolve failures before continuing.
  - _Requirements: <covered identifiers>_

---

## Notes

- Tasks marked with `*` are optional and remain incomplete unless explicitly requested.
- Mark a task `[x]` only after its stated check passes.

<!-- Replace the example waves, tree, dependency table, and tasks with one consistent, acyclic, complete plan. Remove every placeholder before approval. -->
