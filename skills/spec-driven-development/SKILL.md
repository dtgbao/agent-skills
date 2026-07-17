---
name: spec-driven-development
description: Spec-driven development for feature ideas, design-led work, and complex bug fixes. Use when creating, reviewing, synchronizing, or executing requirements.md/bugfix.md, design.md, and tasks.md under docs/specs.
---

# Spec-Driven Development

Turn an idea, technical direction, or defect into reviewed artifacts, then implement approved dependency-ordered tasks with traceable verification.

## Choose the Workflow First

Use only the request and minimal routing clarification to distinguish a feature from a defect and identify whether behavior, technical constraints, or speed should lead. Before deep repository inspection or file creation, present the applicable workflows, recommend one with a one-sentence reason, and wait for the user's choice.

| Workflow | Use when |
| --- | --- |
| Requirements-First | User behavior, scope, or acceptance boundaries should lead; use by default. |
| Design-First | Existing architecture, a fixed stack, or strict technical constraints should lead. |
| Quick Plan | Work is well understood and the user wants all artifacts without intermediate approvals. |
| Bugfix | A complex, critical, or regression-prone defect needs evidence and preserved boundaries. |

For a defect, offer Bugfix and Quick Plan. Wait for the choice before scaffolding an artifact.

## Complete Discovery Before Files

For a feature, read [brainstorming](references/brainstorming.md) after workflow selection. Explore the repository, confirm one focused scope, clarify intent one question at a time, compare two or three approaches, and obtain approval for a decision brief. Complete discovery when the brief states the goal, success criteria, boundaries, constraints, and chosen approach.

For a defect, reproduce or otherwise establish evidence. Use current, expected, and unchanged behavior as its discovery boundary.

If discovery invalidates the selected workflow, explain why and ask the user to choose again before creating files.

## Start or Resume a Spec

Work from the repository root and read its agent instructions. After discovery, create only the current artifact:

```bash
python <skill-directory>/scripts/init_spec.py <slug> \
  --title "<human title>" \
  --artifact <requirements|bugfix|design|tasks>
```

The initializer creates `docs/specs/<slug>/` when needed, refuses to overwrite artifacts, and selects the focused bugfix design template when `bugfix.md` exists. Use `--spec-root` only when the repository overrides `docs/specs`.

For an existing spec, read every present artifact before editing it. Preserve approved decisions and completed evidence. Replace every scaffold placeholder before presenting an artifact.

## Load the Phase Reference

- Before `design.md`, read [design planning](references/design-planning.md). For feature designs, produce repository and component hierarchies, stack-native contracts, operation tables, and Mermaid flows. For bugfixes, produce the focused affected hierarchy and root-cause/fix flow.
- Before `tasks.md`, read [task planning](references/task-planning.md) and [test-driven development](references/test-driven-development.md). Build concise parent groups with paired RED and GREEN leaves plus one canonical JSON dependency graph.
- When tests introduce mocks, test utilities, or production seams used only by tests, also read [testing anti-patterns](references/testing-anti-patterns.md).

Ground paths and native code in inspected repository versions. When a requested stack is not installed, verify its concrete API against current official documentation. Use explicit pseudocode rather than guessed syntax.

## Apply Shared Standards

- Store artifacts at `docs/specs/<slug>/` and use their scaffolded headings as the output contract.
- Keep requirements behavioral and testable. Treat fixed technology and architecture as constraints, not invented user behavior.
- Trace design and required tasks to acceptance identifiers such as `1.2`; trace bugfix work to `EB1` and `UB1`.
- Keep upstream and downstream artifacts synchronized whenever an approved decision changes.
- Use correctness properties only for meaningful universal invariants.
- Keep one independently evolvable capability or defect per spec.

Analyze interacting or high-risk requirements as a set. Resolve contradictions, ambiguity, conflicting constraints, unstated assumptions, missing boundaries, concurrency, and failure behavior before approval.

## Validate Each Artifact

Immediately after writing or changing an artifact, run:

```bash
python <skill-directory>/scripts/validate_spec.py docs/specs/<slug>/<artifact>
```

Use this order:

| Workflow | Validation order |
| --- | --- |
| Requirements-First or feature Quick Plan | `requirements.md` → `design.md` → `tasks.md` |
| Design-First | `design.md` → `requirements.md` → synchronized `design.md` → `tasks.md` |
| Bugfix or bugfix Quick Plan | `bugfix.md` → `design.md` → `tasks.md` |

Stop on failure, repair the artifact, and rerun validation. Request approval only after validation passes. When an upstream artifact changes, validate it and every changed downstream artifact in order.

## Execute the Chosen Workflow

### Requirements-First

1. Fill and obtain approval for behavioral `requirements.md` with numbered user stories and measurable EARS criteria.
2. Inspect the repository, fill concrete `design.md`, prove every requirement maps to design and verification, then obtain approval.
3. Fill hierarchical `tasks.md`, prove paired TDD, traceability, and dependency validity, then obtain approval.
4. Continue with **Implement Approved Tasks**.

### Design-First

1. Inspect the repository, fill feature `design.md` from supplied constraints, validate its structure, and obtain approval.
2. Derive and approve `requirements.md`, then synchronize requirement identifiers into `design.md` and validate it again.
3. Fill and approve hierarchical `tasks.md` with complete coverage and valid dependencies.
4. Continue with **Implement Approved Tasks**.

### Bugfix

1. Fill and approve `bugfix.md` with evidence, current behavior, expected behavior, unchanged behavior, and constraints.
2. Trace callers and root cause, fill the focused bugfix `design.md`, preserve every unchanged boundary, and obtain approval.
3. Fill and approve hierarchical `tasks.md`. Make the first RED leaf reproduce the defect and pair it with the smallest shared fix.
4. Continue with **Implement Approved Tasks**.

### Quick Plan

Resolve every material product and technical question, then create, fill, and validate artifacts sequentially without intermediate approval. Present the complete synchronized set together. Begin implementation only when already authorized or subsequently approved.

## Synchronize Existing Specs

Propagate changes in workflow order: Requirements-First from requirements to design to tasks; Design-First from design to requirements to synchronized design to tasks; Bugfix from bugfix to design to tasks. Preserve completed evidence and reopen a leaf only when the changed contract invalidates its implementation or verification.

## Implement Approved Tasks

1. Read approved artifacts and repository instructions. Select incomplete executable leaves whose `dependsOn` entries are complete; include an explicitly requested leaf's incomplete prerequisites.
2. Execute waves sequentially. Run leaves within one wave concurrently only when they do not share files, mutable state, or unresolved decisions. Leave starred optional work incomplete unless requested.
3. For each pair, complete RED and Verify RED before its dependent GREEN, Verify GREEN, and REFACTOR leaf. For checkpoints or approved exceptions, run the stated evidence. Mark a leaf `[x]` only after its complete form passes.
4. Mark a parent `[x]` only when every required child is complete. After each wave, run the smallest integration check covering its combined changes.
5. Synchronize artifacts when implementation reveals a material correction; obtain approval again when user intent changes.
6. Complete the spec only when every required executable task and parent is checked, final repository checks pass, and implementation matches the approved upstream artifacts.
