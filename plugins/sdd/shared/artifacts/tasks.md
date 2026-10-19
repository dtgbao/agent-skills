# tasks.md

## Vertical slices

Work in vertical slices: one test → one implementation → repeat. Each slice delivers one behavior a user or caller observes, through every layer it needs, and leaves the suite green. Horizontal slicing (all tests first, then all code; or one layer at a time) gives brittle tests that check the shape of the code, not its behavior.

- Group = one capability, usually one requirement. Its slices build on each other.
- First slice of the plan = **tracer bullet**: the thinnest end-to-end path through every layer the feature touches. Riskiest slice next (fail fast).
- Slice size: ≤3 criteria, ≤5 `Files`, a title with no "and". Bigger → split by behavior, never by layer.
- A slice's `Do` and `Verify` use only the behavior that its own criteria and earlier slices give. The tracer bullet is one path with no later branches: no clamps, no error cases, no fields that a later slice adds.
- Every value in `Do` and `Verify` must be reachable through the `Seam` with the code that exists at that point. Example: use a price that the catalog can hold.
- Every test drives a seam from design.md `## Testing Strategy` (public interface). No test reaches into internals.

## Leaf

Two levels: `- [ ] N. <group>` → `  - [ ] N.M <leaf>`. Leaf = unit of work, one subagent. Marks: `[ ]` todo, `[-]` running, `[x]` done.

Leaf fields, in order:

```markdown
  - [ ] 2.1 <behavior, as the caller sees it>
    - Files: `tests/test_a.py`, `src/a.py`
    - Kind: setup | slice | test | pin | fix
    - Size: S | M | L
    - Seam: <public interface the tests drive>
    - Do: <1–3 bullets: per cited criterion, the test, then the minimal code; exact command for setup>
    - Verify: <test command that proves it>
    - _Requirements: 1.1, 1.2_
```

| Kind | Holds | Runner does |
|---|---|---|
| `setup` | scaffolding, config, deps; no criterion | runs the exact `Do` |
| `slice` | test file(s) + code file(s) for ≤3 criteria | per criterion: one failing test (red) → minimal code (green) → next |
| `test` | extra tests on a finished slice, always `*` | adds tests only; never the first test of a behavior |
| `pin` | bugfix test, `Expect: red` or `Expect: green` | writes the test, runs it on unfixed code |
| `fix` | bugfix code | minimal change that turns the red pin green; pins unchanged |

- `Seam` on `slice`, `test`, `pin`. Setup and fix leaves omit it.
- `Size` picks the runner model (`spec-run` step 5). S = setup, or a one-criterion slice with exact `Do` and `Verify`. M = normal slice. L = crosses modules, new algorithm, concurrency, or security.
- `_Requirements: none (setup)_` for setup leaf with no criterion.
- Optional `- [ ]*` (running `[-]*`, done `[x]*`): `Kind: test` only. Notes line: `*` = optional, skip for faster MVP.
- Leaf holding properties adds `**Property N: <title>**` + `**Validates: Requirements x.y**` per property (`${CLAUDE_PLUGIN_ROOT}/shared/correctness.md`). A property sits in the slice that implements its criteria.
- Pin leaf adds `Expect: red` (exploration: fails on unfixed code) or `Expect: green` (preservation: passes on unfixed code). Pins are never `*`.

## Checkpoint

Top-level task, never in graph: `- [ ] N. Checkpoint — run <test cmd>; <typecheck cmd | typecheck: none>`. Commands from manifest scripts or README. One after each group, one final. Last top-level task = checkpoint. A checkpoint checks the suite at that point; parallel waves can land later-group leaves first (`check-tasks` prints `WARN`).

## Wave rules

- Graph = last section `## Task Dependency Graph`: JSON `waves` + `deps` (leaf → leaves it needs).
- Wave ids from `0`. Leaves only. Leaf in exactly one wave, strictly after waves of its `deps`.
- Same-wave leaves: disjoint `Files`. Leaf that reads or imports a file another leaf writes → `deps` on it.
- Setup leaf first. Tracer-bullet slice next. Slice that extends another slice's code → `deps` on it. Test leaf `deps` on the slices it covers.
- Bugfix: pins before fix. Fix leaf `deps` on every pin. Leaves cite Expected `2.n` and Unchanged `3.n`; citing Current `1.n` is optional.

## Bugfix order

1. Exploration pin, `Expect: red`: reproduces bug. Holds Property 1 (fix check).
2. Preservation pins, `Expect: green`: pin Unchanged items. One holds Property 2 (preservation).
3. Fix (`Kind: fix`).
4. Checkpoint: all pins green.

Done when: `python3 ${CLAUDE_PLUGIN_ROOT}/shared/scripts/spec.py check-tasks <dir>` prints `RESULT: PASS` (covers: graph parses, one wave per leaf, deps order, disjoint files, `Files` / `Kind` / `Size` / `Seam` / `Do` / `Verify` / `_Requirements:_`, slice holds test + code files, slice ≤3 criteria and ≤5 files, `*` rule, pins, every criterion cited, every property in a leaf, final checkpoint).

Skeleton:

````markdown
# Implementation Plan: <feature>

## Overview

<tracer bullet, then slice order, 1 paragraph>

## Tasks

- [ ] 1. <capability>
  - [ ] 1.1 <tracer-bullet behavior>
    - Files: `<test path>`, `<code path>`
    - Kind: slice
    - Size: M
    - Seam: `<public interface>`
    - Do: 1.1: test <case> → code <minimal change>
    - **Property 1: <title>**
    - **Validates: Requirements 1.1**
    - Verify: `<test cmd> <test path>`
    - _Requirements: 1.1_
  - [ ]* 1.2 <extra tests for 1.1>
    - Files: `<extra test path>`
    - Kind: test
    - Size: S
    - Seam: `<public interface>`
    - Verify: `<test cmd> <extra test path>`
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
