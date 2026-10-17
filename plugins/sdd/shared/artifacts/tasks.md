# tasks.md

## Format

- Two levels: `- [ ] N. <group>` → `  - [ ] N.M <leaf>`. Leaf = unit of work.
- Optional leaf (tests): `- [ ]*`.
- Marks: `[ ]` todo, `[-]` running, `[x]` done.
- Leaf ends with `_Requirements: x.y, x.z_`.
- Leaf names files it touches.
- Property leaf carries `**Property N: <title>**` and `**Validates: Requirements x.y**` (see `${CLAUDE_PLUGIN_ROOT}/shared/correctness.md`).
- Checkpoint = top-level task "Checkpoint — run tests, ask user on questions". One after each layer, one final. Never in graph.
- Last section `## Task Dependency Graph`: JSON `waves`.

## Wave rules

- Wave ids from `0`. Leaves only.
- Leaf sits in exactly one wave, strictly after every wave holding its dependencies.
- Same-wave leaves touch disjoint files.
- Install/config leaf first. Test leaf after code leaf it covers.

Done when:
- every criterion cited by ≥1 leaf
- every leaf in exactly one wave
- every leaf names its files
- graph JSON parses

## Bugfix order

1. Exploration test: goes red on unfixed code, reproduces bug.
2. Preservation tests: go green on unfixed code, pin unchanged behavior.
3. Fix.
4. Rerun 1 and 2: both green.

Skeleton:

````markdown
# Implementation Plan: <feature>

## Overview

<approach, order of work, 1 paragraph>

## Tasks

- [ ] 1. <group>
  - [ ] 1.1 <leaf>
    - <detail>
    - _Requirements: 1.1_
  - [ ]* 1.2 <optional test leaf>
    - _Requirements: 1.1_

- [ ] 2. Checkpoint — run tests, ask user on questions

## Notes

- `*` = optional, skip for faster MVP
- <constraint worth remembering>

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2"] }
  ]
}
```
````
