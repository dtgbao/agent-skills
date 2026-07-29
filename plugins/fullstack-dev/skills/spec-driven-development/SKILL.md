---
name: spec-driven-development
description: Spec-driven development for feature ideas, design-led work, and complex bug fixes. Use when creating, reviewing, synchronizing, or implementing from requirements.md, bugfix.md, and design.md under docs/specs.
---

# Spec-Driven Development

Turn an idea, technical direction, or defect into approved requirements and design, then implement
directly from those artifacts with traceable verification.

## Choose the Workflow First

Use the request and only enough clarification to distinguish a feature from a defect and decide
whether behavior, technical constraints, or speed should lead. Before deep repository inspection or
file creation, present the applicable workflows, recommend one with a one-sentence reason, and wait
for the user's choice.

| Workflow           | Use when                                                                                      |
| ------------------ | --------------------------------------------------------------------------------------------- |
| Requirements-First | User behavior, scope, or acceptance boundaries should lead; use by default.                   |
| Design-First       | Existing architecture, a fixed stack, or strict technical constraints should lead.            |
| Quick Plan         | The work is well understood and the user wants both artifacts without intermediate approvals. |
| Bugfix             | A complex, critical, or regression-prone defect needs evidence and preserved boundaries.      |

For a defect, offer Bugfix and Quick Plan. Wait for the choice before creating an artifact.

## Complete Discovery Before Files

For a feature, inspect relevant repository context, confirm one independently evolvable capability,
clarify intent one focused question at a time, and compare two or three viable approaches. Obtain
approval for a concise decision brief covering the goal, success criteria, boundaries, constraints,
and chosen approach before creating specification files.

For a defect, reproduce it or establish equivalent evidence. Use current, expected, and unchanged
behavior as the discovery boundary.

If discovery invalidates the selected workflow, explain why and ask the user to choose again before
creating files.

## Start or Resume a Spec

Work from the repository root and read its agent instructions. Store each spec under
`docs/specs/<slug>/`. Read the applicable bundled template, use its headings as the output
contract, and create only the artifact required by the current phase:

| Artifact            | Template                                                    |
| ------------------- | ----------------------------------------------------------- |
| `requirements.md`   | [Requirements template](assets/templates/requirements.md)   |
| `bugfix.md`         | [Bugfix template](assets/templates/bugfix.md)               |
| Feature `design.md` | [Feature design template](assets/templates/design.md)       |
| Bugfix `design.md`  | [Bugfix design template](assets/templates/design-bugfix.md) |

For an existing spec, read every present artifact before editing it. Preserve approved decisions
and completed evidence. Replace every scaffold placeholder before presenting an artifact.

## Ground the Design

Before writing `design.md`, inspect affected code, tests, configuration, dependency versions,
generated types, and repository conventions.

- For features, show the relevant repository structure and runtime component hierarchy. Define
  stack-native interfaces, schemas, operations, errors, and nontrivial flows.
- For bugfixes, show only the affected caller and ownership hierarchy, evidence-backed root cause,
  smallest shared fix, changed contracts, regression evidence, and preserved `UB` boundaries.
- Use Mermaid for nontrivial request, state, authorization, persistence, retry, concurrency, cache,
  or background flows. Use tables for operation, error, test, and traceability inventories.
- Verify APIs against current official documentation when the requested stack is not installed.
  Use explicitly labeled pseudocode instead of guessed syntax.

The design is ready only when an implementer can proceed without inventing a path, contract,
behavior, error shape, or verification method.

## Apply Shared Standards

- Keep requirements behavioral and testable. Treat fixed technology and architecture as
  constraints, not invented user behavior.
- Trace every design element and verification method to acceptance identifiers such as `1.2`, or
  to bugfix identifiers such as `EB1` and `UB1`.
- Analyze interacting or high-risk requirements together. Resolve contradictions, ambiguity,
  conflicting constraints, unstated assumptions, missing boundaries, concurrency, and failure
  behavior before approval.
- Keep upstream and downstream artifacts synchronized whenever an approved decision changes.
- Use correctness properties only for meaningful universal invariants.
- Keep one independently evolvable capability or defect per spec.

## Validate Each Artifact

Run any repository-provided spec validator and the smallest relevant Markdown or documentation
check immediately after writing or changing an artifact. When no validator exists, self-review the
artifact against its required content and the shared standards above.

| Workflow                                 | Validation order                                           |
| ---------------------------------------- | ---------------------------------------------------------- |
| Requirements-First or feature Quick Plan | `requirements.md` → `design.md`                            |
| Design-First                             | `design.md` → `requirements.md` → synchronized `design.md` |
| Bugfix or bugfix Quick Plan              | `bugfix.md` → `design.md`                                  |

Stop on failure, repair the artifact, and validate again. Request approval only after validation
passes. When an upstream artifact changes, validate it and every changed downstream artifact in
order.

## Execute the Chosen Workflow

### Requirements-First

1. Fill and obtain approval for behavioral `requirements.md` with numbered user stories and
   measurable EARS criteria.
2. Inspect the repository, fill concrete `design.md`, prove every requirement maps to design and
   verification, then obtain approval.
3. Continue with **Implement from the Approved Design**.

### Design-First

1. Inspect the repository, fill `design.md` from supplied constraints, validate its structure, and
   obtain approval.
2. Derive and approve `requirements.md`, then synchronize its identifiers into `design.md` and
   validate the design again.
3. Continue with **Implement from the Approved Design**.

### Bugfix

1. Fill and approve `bugfix.md` with evidence, current behavior, expected behavior, unchanged
   behavior, and constraints.
2. Trace callers and root cause, fill the focused bugfix `design.md`, preserve every unchanged
   boundary, and obtain approval.
3. Continue with **Implement from the Approved Design**.

### Quick Plan

Resolve every material product and technical question, then create, fill, and validate the two
applicable artifacts sequentially without intermediate approval. Present the synchronized set
together. Begin implementation only when already authorized or subsequently approved.

## Synchronize Existing Specs

Propagate changes in workflow order: Requirements-First from requirements to design; Design-First
from design to requirements to synchronized design; Bugfix from bugfix analysis to design. Preserve
completed evidence, and reverify implementation only where the changed contract invalidates it.

## Implement from the Approved Design

1. Read the approved artifacts and repository instructions. Select the smallest dependency-ready
   vertical slice directly from the design.
2. For each behavior-changing slice, follow
   [`test-driven-development`](../test-driven-development/SKILL.md): establish failing evidence,
   implement the minimum change, then refactor only while verification stays green.
3. Verify the slice against its requirement or bugfix identifiers and run the smallest integration
   check that covers its interaction with completed work.
4. If implementation reveals a material correction, synchronize the artifacts first. Obtain
   approval again when user intent or an approved boundary changes.
5. Complete the spec only when every acceptance criterion or expected and unchanged behavior has
   evidence, final repository checks pass, and implementation matches the approved artifacts.

## Keep the Spec Alive

- Update the upstream artifact first when behavior or scope changes, then synchronize the design.
- Update `design.md` first when an implementation detail changes without changing behavior, then
  confirm upstream requirements remain accurate.
- Keep the spec in version control with the implementation and reference its identifiers in review
  or pull-request evidence.

## Common Rationalizations

| Rationalization                                                   | Reality                                                                                                                           |
| ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| "This is simple, so it does not need a spec"                      | Simple work may need only a short requirement and design, but observable completion still needs to be written down.               |
| "I will write the spec after coding"                              | That is documentation, not specification. The value comes from resolving misunderstandings before implementation.                 |
| "Requirements and design will slow us down"                       | Concise, approved artifacts focus effort on unresolved decisions and prevent rework during implementation.                        |
| "Requirements will change anyway"                                 | That is why upstream artifacts stay synchronized with design and implementation.                                                  |
| "The design can stay high level because the code will clarify it" | If implementation must invent contracts or error behavior, the design has not resolved the risky decisions.                       |

## Red Flags

- Starting implementation without approved requirements or bugfix boundaries and an approved design
- Asking to start building before success criteria and material boundaries are resolved
- Naming paths, APIs, or contracts in the design without repository or official-source evidence
- Making architectural or behavioral decisions only in code
- Failing to synchronize requirement identifiers into a Design-First design
- Implementing behavior that cannot be traced to an upstream identifier
- Treating a stale spec as complete after scope or design changes

## Verification

Before implementation, confirm:

- [ ] The user selected the workflow, or explicitly authorized the applicable Quick Plan.
- [ ] Feature discovery produced an approved decision brief, or defect discovery established evidence.
- [ ] `requirements.md` or `bugfix.md` is complete, validated, and approved.
- [ ] `design.md` is repository-grounded, complete, validated, approved, and traceable upstream.
- [ ] No material decision, placeholder, contradiction, or ambiguous boundary remains.
- [ ] Both artifacts are saved under the same `docs/specs/<slug>/` directory.

After implementation, confirm:

- [ ] Every acceptance criterion, or every `EB` and `UB` behavior, has verification evidence.
- [ ] Final repository checks pass.
- [ ] The artifacts and implementation remain synchronized.
