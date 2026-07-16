---
name: spec-driven-development
description: Spec-driven development for feature ideas, design-led work, and complex bug fixes. Use when creating, reviewing, synchronizing, or executing requirements.md/bugfix.md, design.md, and tasks.md under docs/specs.
---

# Spec-Driven Development

Turn an idea, technical direction, or defect into reviewed artifacts, then implement the approved tasks with traceable verification.

## Brainstorm Feature Ideas Before Choosing a Workflow

For every new feature spec, read [brainstorming](references/brainstorming.md) before presenting workflow choices. Explore the repository, confirm one focused scope, clarify intent one question at a time, compare two or three approaches, and obtain approval for a concise decision brief.

Complete this preflight only when the brief states the goal, success criteria, boundaries, constraints, and chosen approach clearly enough to recommend a workflow. For a defect, begin with the Bugfix workflow choice and evidence flow; reproduction and behavioral boundaries provide its discovery process.

## Choose Workflow Before Creating Files

After the feature preflight, present Requirements-First, Design-First, and Quick Plan. State the recommendation and one-sentence reason, then ask the user to choose:

| Workflow | Recommend when |
| --- | --- |
| Requirements-First | User behavior, scope, or acceptance boundaries should lead; use this by default. |
| Design-First | Existing architecture, a fixed stack, or strict technical constraints should lead. |
| Quick Plan | The work is well understood and the user wants all artifacts without intermediate approvals. |

For a defect, present Bugfix and Quick Plan, recommending Bugfix for complex, critical, or regression-prone behavior. Wait for the user's choice before calling the initializer, creating a spec directory, or drafting any artifact.

## Start or Resume a Spec

Work from the repository root and read its agent instructions before writing artifacts. After the user chooses a workflow, create only the artifact for the current phase:

```bash
python <skill-directory>/scripts/init_spec.py <slug> \
  --title "<human title>" \
  --artifact <artifact>
```

Use `requirements`, `bugfix`, `design`, or `tasks` as the artifact. Run the initializer again only when the workflow reaches the next phase; it creates the spec directory when needed and refuses to overwrite an existing artifact. Use `--spec-root <path>` only when the repository explicitly overrides `docs/specs`.

For an existing spec, read every present artifact under `docs/specs/<slug>/` before editing it. Preserve approved decisions and edit the existing files.

Replace every scaffold placeholder before presenting an artifact for approval. Keep one focused capability or defect per spec; create another spec when work can evolve independently.

## Load Phase References

- Before drafting or revising `design.md` or `tasks.md`, read [design and task planning](references/design-and-task-planning.md). Apply its repository mapping, interface, task-sizing, dependency, and self-review guidance to the relevant artifact.
- Before drafting or revising `tasks.md`, also read [test-driven development](references/test-driven-development.md). Give every behavior task a complete ordered RED, Verify RED, GREEN, Verify GREEN, and REFACTOR cycle.
- When planned tests introduce mocks, test utilities, or production interfaces used only by tests, also read [testing anti-patterns](references/testing-anti-patterns.md) before finalizing the design or tasks.

Use `[TDD Exception]` only for throwaway exploration, generated output, configuration-only work, or another case the user explicitly approves. Record the reason, approval, and exact check in the task. In Quick Plan, obtain that approval while resolving material questions before generating `tasks.md`.

## Apply Shared Standards

- Store artifacts at `docs/specs/<slug>/`.
- Use the scaffolded headings and formatting as the output contract.
- Keep requirements behavioral and testable. Treat fixed technology or architecture as constraints, not invented requirements.
- Inspect the codebase before claiming a design, root cause, interface, dependency, or test command.
- Trace design decisions, correctness properties, and tasks to requirement identifiers such as `1.2`; trace bugfix work to identifiers such as `EB1` and `UB1`.
- Include universal correctness properties only when they express meaningful invariants. Prefer the repository's installed test tools; add a property-testing dependency only when the property materially justifies it.
- Keep `requirements.md` or `bugfix.md`, `design.md`, and `tasks.md` synchronized whenever an upstream decision changes.

Analyze requirements as a set when behaviors interact, the domain is high-risk or unfamiliar, or Quick Plan skipped staged review. Find contradictions, ambiguity, conflicting constraints, unstated assumptions, missing boundaries, concurrency cases, and failure behavior. Complete analysis only when every finding is resolved in the artifact or explicitly accepted by the user.

## Validate Each Artifact

Immediately after writing or changing an artifact, run:

```bash
python <skill-directory>/scripts/validate_spec.py docs/specs/<slug>/<artifact>
```

Use these phase gates:

| Workflow                                 | Validation order                                                        |
| ---------------------------------------- | ----------------------------------------------------------------------- |
| Requirements-First or feature Quick Plan | `requirements.md` → `design.md` → `tasks.md`                            |
| Design-First                             | `design.md` → `requirements.md` → synchronized `design.md` → `tasks.md` |
| Bugfix or bugfix Quick Plan              | `bugfix.md` → `design.md` → `tasks.md`                                  |

Stop when validation fails. Repair the artifact and rerun the validator before continuing. Request approval only after validation passes. When an upstream artifact changes, validate it and every changed downstream artifact in workflow order.

For `tasks.md`, validation requires each numbered required or optional task to use one accepted form: an ordered TDD cycle, an approved `[TDD Exception]` with Reason, Approval, and Check entries, or a `Checkpoint` with Check and Expected entries.

## Requirements-First

1. Fill `requirements.md` from the user intent. Include only glossary terms reused by the spec, numbered user stories, and measurable EARS acceptance criteria. Complete the phase when every requested behavior and boundary is represented, every criterion is testable, analysis findings are resolved, and the user explicitly approves the artifact.
2. Explore the relevant code and fill `design.md` using the design-planning reference. Account for every acceptance criterion across architecture, interfaces, data, failure handling, and tests. Complete the phase when every requirement is traceable to a concrete design decision and the user explicitly approves the artifact.
3. Fill `tasks.md` from the approved design using the task-planning and TDD references. Represent the same acyclic dependencies as JSON execution waves, an ASCII dependency tree, and a task-to-dependencies table. Keep tasks discrete and verifiable, give every behavior task its complete TDD cycle, and reference every requirement from at least one required task. Complete the phase when all three dependency views agree, every task uses an accepted form, the plan covers implementation and validation, and the user explicitly approves it.
4. Continue with **Implement Approved Tasks**.

## Design-First

1. Explore the codebase and fill `design.md` from the supplied architecture or constraints using the design-planning reference. State interfaces, data flow, non-functional constraints, risks, and validation strategy. Complete the phase when the design is feasible and the user explicitly approves it.
2. Derive `requirements.md` from the approved design, then review it for missing user value and edge behavior. Synchronize requirement identifiers back into `design.md`. Complete the phase when requirements remain feasible, the two artifacts agree, and the user explicitly approves them.
3. Fill `tasks.md` using the task-planning and TDD references, with synchronized JSON waves, an ASCII dependency tree, and a task-to-dependencies table. Prove complete requirement coverage, accepted task forms, and acyclic dependencies, then obtain explicit approval.
4. Continue with **Implement Approved Tasks**.

## Bugfix

1. Reproduce or otherwise establish evidence for the defect. Fill `bugfix.md` with reproduction evidence, current behavior, expected behavior, unchanged behavior, constraints, and regression boundaries. Complete the phase when the behavioral change is unambiguous and the user explicitly approves it.
2. Trace every relevant caller and investigate the root cause. Fill `design.md` using the design-planning reference, with the evidence-backed root cause, smallest shared fix, affected components, failure handling, and regression strategy. Complete the phase when the fix preserves every unchanged behavior and the user explicitly approves it.
3. Fill `tasks.md` using the task-planning and TDD references, with synchronized JSON waves, an ASCII dependency tree, and a task-to-dependencies table. Make the first behavior task reproduce the original defect in RED, pass after GREEN, and protect unchanged behavior through related verification. Complete the phase when every expected and unchanged behavior is referenced, every task uses an accepted form, and the user explicitly approves it.
4. Continue with **Implement Approved Tasks**.

## Quick Plan

Ask all material questions about scope, constraints, edge cases, and success criteria before generation. Then create, fill, and validate each artifact sequentially in workflow order without intermediate approval gates. Do not pre-create downstream artifacts.

Cross-check that requirements are testable, design covers every requirement, tasks cover the design, all three dependency views agree, and dependencies are acyclic. Present the completed set together. Begin implementation only when the original request authorizes it or the user subsequently approves it.

## Synchronize Existing Specs

Propagate changes in this order:

| Workflow           | Synchronization order                        |
| ------------------ | -------------------------------------------- |
| Requirements-First | `requirements.md` → `design.md` → `tasks.md` |
| Design-First       | `design.md` → `requirements.md` → `tasks.md` |
| Bugfix             | `bugfix.md` → `design.md` → `tasks.md`       |

Preserve completed task evidence. Reopen a task only when the changed artifact invalidates its implementation or verification.

## Implement Approved Tasks

1. Read the approved artifacts and repository instructions. Select incomplete required tasks whose dependencies are satisfied; include a requested task's incomplete prerequisites.
2. Execute dependency waves sequentially. Run tasks within one wave concurrently only when they do not share files, mutable state, or unresolved decisions. Keep starred optional tasks incomplete unless the user requests them.
3. For each behavior task, execute RED, Verify RED, GREEN, Verify GREEN, and REFACTOR in order, preserving the observed failure and passing evidence. For an approved exception or checkpoint, run its stated check and confirm the expected result. Mark the checkbox `[x]` only after the complete task form passes; otherwise leave it incomplete and report the evidence.
4. After each wave, run the smallest integration check that covers its combined changes. Synchronize artifacts if implementation reveals a material requirement or design correction, and obtain approval again when user intent changes.
5. Complete the spec only when every required task is checked, the final repository checks pass, and the implementation still matches the approved requirements or bugfix boundaries.
