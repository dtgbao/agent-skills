# tasks.md

## Leaf

Two levels: `- [ ] N. <group>` → `  - [ ] N.M <leaf>`. Leaf = unit of work, one subagent. Marks: `[ ]` todo, `[-]` running, `[x]` done. Group = layer.

Leaf fields, in order:

```markdown
  - [ ] 2.1 <imperative title>
    - Files: `src/a.ts`, `tests/a.test.ts`
    - Kind: setup | code | test | pin
    - Size: S | M | L
    - Do: <1–3 bullets: what to create, export, change; exact command for setup>
    - Verify: <test cases or command that proves it>
    - _Requirements: 1.1, 1.2_
```

- `Size` picks the runner model (`spec-run` step 5). S = setup, or one file with exact `Do` and `Verify`. M = normal code or test leaf. L = crosses modules, new algorithm, concurrency, or security.
- `_Requirements: none (setup)_` for setup leaf with no criterion.
- Optional `- [ ]*` (running `[-]*`, done `[x]*`): `Kind: test` only. Notes line: `*` = optional, skip for faster MVP.
- Test leaf holding properties adds `**Property N: <title>**` + `**Validates: Requirements x.y**` per property (`${CLAUDE_PLUGIN_ROOT}/shared/correctness.md`).
- Pin leaf (bugfix) adds `Expect: red` (exploration: fails on unfixed code) or `Expect: green` (preservation: passes on unfixed code). Pins are never `*`.

## Checkpoint

Top-level task, never in graph: `- [ ] N. Checkpoint — run <test cmd>; <typecheck cmd | typecheck: none>`. Commands from manifest scripts or README. One after each layer with code, one final. Last top-level task = checkpoint. A checkpoint checks the suite at that point; parallel waves can land later-layer code first (`check-tasks` prints `WARN`).

## Wave rules

- Graph = last section `## Task Dependency Graph`: JSON `waves` + `deps` (leaf → leaves it needs).
- Wave ids from `0`. Leaves only. Leaf in exactly one wave, strictly after waves of its `deps`.
- Same-wave leaves: disjoint `Files`. Leaf that reads or imports a file another leaf writes → `deps` on it.
- Setup leaf first. Test leaf `deps` on code leaves it covers.
- Bugfix: pins before fix. Fix leaf `deps` on every pin. Leaves cite Expected `2.n` and Unchanged `3.n`; citing Current `1.n` is optional.

## Bugfix order

1. Exploration pin, `Expect: red`: reproduces bug.
2. Preservation pins, `Expect: green`: pin Unchanged items.
3. Fix (`Kind: code`).
4. Checkpoint: all pins green.

Done when: `python3 ${CLAUDE_PLUGIN_ROOT}/shared/scripts/spec.py check-tasks <dir>` prints `RESULT: PASS` (covers: graph parses, one wave per leaf, deps order, disjoint files, `Files` / `Kind` / `Size` / `Do` / `Verify` / `_Requirements:_`, `*` rule, pins, every criterion cited, every property in a leaf, final checkpoint).

Skeleton:

````markdown
# Implementation Plan: <feature>

## Overview

<approach, order of work, 1 paragraph>

## Tasks

- [ ] 1. <group>
  - [ ] 1.1 <leaf>
    - Files: `<path>`
    - Kind: code
    - Size: M
    - Do: <what>
    - Verify: <how>
    - _Requirements: 1.1_
  - [ ]* 1.2 <test leaf>
    - Files: `<test path>`
    - Kind: test
    - Size: S
    - **Property 1: <title>**
    - **Validates: Requirements 1.1**
    - Verify: `<test cmd> <test path>`
    - _Requirements: 1.1_

- [ ] 2. Checkpoint — run `<test cmd>`; typecheck: none

## Notes

- `*` = optional, skip for faster MVP
- <constraint worth remembering>

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2"] }
  ],
  "deps": { "1.2": ["1.1"] }
}
```
````
