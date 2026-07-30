---
name: using-fullstack-dev
description: Discovers and coordinates full-stack development skills. Use when starting full-stack engineering work or deciding which bundled workflow applies and in what order.
---

# Using Fullstack Dev

## Overview

Fullstack Dev is a collection of engineering workflows spanning definition, design, implementation,
verification, operations, and delivery. This meta-skill selects every applicable sibling skill,
orders dependencies, and maps concerns outside the bundle to repository-native processes.

## Skill Discovery

When a task arrives, identify its phase and concerns, then read every matching sibling skill before
acting:

```text
Task arrives
│
├── Need requirements and design for a feature or complex bug? ──→ spec-driven-development
├── Designing architecture, modules, interfaces, or seams? ──────→ codebase-design
├── Working with PostgreSQL schemas, queries, or configuration? ─→ supabase-postgres-best-practices
├── Designing backend services, APIs, or public contracts? ──────→ api-and-interface-design
├── Writing framework- or library-specific code? ────────────────→ source-driven-development
├── Building pages, components, state, or responsive behavior? ──→ frontend-ui-engineering
│   └── React TypeScript architecture or tests? ─────────────────→ react-best-practices
├── Adding or changing behavior, including a bug fix? ───────────→ test-driven-development
├── Something failed or behaves unexpectedly? ───────────────────→ debugging-and-error-recovery
├── Reviewing completed code? ───────────────────────────────────→ code-review-and-quality
│   └── Unnecessary complexity? ─────────────────────────────────→ code-simplification
├── Handling trust boundaries, auth, or untrusted data? ─────────→ security-and-hardening
├── Meeting a performance target or investigating a regression? ─→ performance-optimization
├── Adding production logs, metrics, traces, or alerts? ─────────→ observability-and-instrumentation
├── Recording decisions, public behavior, or setup? ─────────────→ documentation-and-adrs
├── Replacing, removing, or migrating a system? ─────────────────→ deprecation-and-migration
├── Automating quality or deployment gates? ─────────────────────→ ci-cd-and-automation
├── Branching, committing, versioning, or writing a changelog? ──→ git-workflow-and-versioning
└── Deploying, rolling out, monitoring, or rolling back? ────────→ shipping-and-launch
```

Use `supabase-postgres-best-practices` only when the project's database matches. For another engine,
follow the repository's native database guidance and continue routing the remaining concerns.

## Core Operating Behaviors

These behaviors apply throughout every selected workflow.

### 1. Surface Assumptions

Before non-trivial work, state the assumptions that affect requirements, architecture, or scope.
Do not silently resolve ambiguity that could materially change the result.

```text
ASSUMPTIONS:
1. [requirement assumption]
2. [architecture assumption]
3. [scope assumption]

Correct any that are wrong; otherwise I will proceed.
```

### 2. Manage Confusion

When requirements, repository evidence, or selected skills conflict:

1. Stop before making the affected decision.
2. Name the exact inconsistency.
3. Explain the relevant tradeoff or ask one focused question.
4. Resume only after the conflict is resolved.

### 3. Push Back When Warranted

Call out concrete technical problems, explain their cost, and propose a simpler or safer alternative.
If the user proceeds with the original approach after seeing the tradeoff, follow that decision.

### 4. Enforce Simplicity

Prefer the smallest clear solution that meets the verified requirements. Reuse repository patterns,
standard-library features, installed dependencies, and native platform capabilities before adding
new abstractions or code.

### 5. Maintain Scope Discipline

Touch only what the task requires. Do not refactor adjacent systems, remove unfamiliar code or
comments, or add speculative features. Remove only the orphaned code created by the current change.

### 6. Verify, Do Not Assume

Every selected skill's verification must pass. A task is complete only when its acceptance criteria
and the project-wide
[`Definition of Done`](../shipping-and-launch/references/definition-of-done.md) are satisfied with
evidence such as tests, builds, runtime checks, or production signals.

## Failure Modes to Avoid

1. Starting implementation with material assumptions left unstated.
2. Continuing through contradictory requirements or repository evidence.
3. Loading one obvious skill while ignoring another concern in the same task.
4. Treating a skill's ordered workflow or verification as optional.
5. Writing version-sensitive framework code from memory when official sources are required.
6. Forcing a bundled database workflow onto an unsupported engine.
7. Adding abstractions, features, or refactors outside the requested scope.
8. Declaring completion from inspection alone without verification evidence.

## Skill Rules

1. Check this routing map before starting full-stack engineering work.
2. **Skills are workflows, not suggestions.** Read every selected sibling skill completely, follow
   its steps in order, and do not skip its verification.
3. Select multiple skills when the task spans multiple concerns; do not collapse distinct
   verification gates into one.
4. Start with `spec-driven-development` when a non-trivial feature or complex defect lacks approved,
   repository-grounded requirements and design. Do not force a full spec onto a trivial local edit.
5. Apply security, performance, observability, source verification, and documentation alongside the
   implementation phase whenever their triggers match.
6. On failure, switch to `debugging-and-error-recovery`; resume the interrupted workflow only after
   its verification passes.
7. Map concerns not covered by a sibling skill to an explicitly named repository-native process.

## Lifecycle Sequence

For a complete feature, use the applicable parts of this sequence:

```text
1. spec-driven-development
   Define approved behavior and a repository-grounded design when the task warrants a spec.
2. codebase-design
   Establish modules and seams.
3. supabase-postgres-best-practices
   Design or change PostgreSQL data concerns when the engine matches.
4. api-and-interface-design
   Establish backend and public contracts.
5. source-driven-development
   Verify version-sensitive implementation decisions against official documentation.
6. affected domain skills + test-driven-development
   Implement dependency-ready database, service, and UI slices and prove each behavior change.
   For React TypeScript UI work, apply react-best-practices under frontend-ui-engineering.
7. security-and-hardening + performance-optimization
   Apply matched safety and measured performance constraints during implementation and review.
8. observability-and-instrumentation + documentation-and-adrs
   Instrument production behavior and record decisions as the implementation evolves.
9. ci-cd-and-automation
   Enforce the applicable repository checks.
10. code-review-and-quality
    Review the completed change across quality dimensions.
11. code-simplification
    Remove warranted complexity without changing verified behavior, then review again.
12. git-workflow-and-versioning
    Prepare authorized commits, versions, tags, or changelogs.
13. shipping-and-launch
    Complete authorized rollout, monitoring, and recovery work.
```

Use `deprecation-and-migration` before affected design and implementation skills when replacing or
removing a system. Invoke `debugging-and-error-recovery` wherever failure interrupts the sequence.
Not every task needs every skill: a focused bug fix may need only
`debugging-and-error-recovery` → `test-driven-development` → `code-review-and-quality`.

## Quick Reference

| Phase    | Skill                                                                                | Use it to                                                                      |
| -------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| Define   | [`spec-driven-development`](../spec-driven-development/SKILL.md)                     | Establish approved requirements, design, and traceability for non-trivial work |
| Design   | [`codebase-design`](../codebase-design/SKILL.md)                                     | Choose deep modules, small interfaces, and clear seams                         |
| Design   | [`supabase-postgres-best-practices`](../supabase-postgres-best-practices/SKILL.md)   | Design or optimize matching PostgreSQL data concerns                           |
| Design   | [`api-and-interface-design`](../api-and-interface-design/SKILL.md)                   | Define stable service, API, and module contracts                               |
| Build    | [`source-driven-development`](../source-driven-development/SKILL.md)                 | Ground version-sensitive code in official documentation                        |
| Build    | [`frontend-ui-engineering`](../frontend-ui-engineering/SKILL.md)                     | Build accessible, responsive, production-quality interfaces                    |
| ↳ React  | [`react-best-practices`](../react-best-practices/SKILL.md)                          | Apply React architecture guidance within frontend implementation and review    |
| Verify   | [`test-driven-development`](../test-driven-development/SKILL.md)                     | Prove behavior changes with a failing test first                               |
| Recover  | [`debugging-and-error-recovery`](../debugging-and-error-recovery/SKILL.md)           | Reproduce, localize, fix, and guard unexpected failures                        |
| Review   | [`code-review-and-quality`](../code-review-and-quality/SKILL.md)                     | Review completed changes before merge or release                               |
| Review   | [`code-simplification`](../code-simplification/SKILL.md)                             | Reduce unnecessary complexity while preserving behavior                        |
| Guard    | [`security-and-hardening`](../security-and-hardening/SKILL.md)                       | Protect trust boundaries, identities, and sensitive data                       |
| Guard    | [`performance-optimization`](../performance-optimization/SKILL.md)                   | Measure and improve material performance bottlenecks                           |
| Operate  | [`observability-and-instrumentation`](../observability-and-instrumentation/SKILL.md) | Add actionable logs, metrics, traces, and alerts                               |
| Document | [`documentation-and-adrs`](../documentation-and-adrs/SKILL.md)                       | Preserve decisions, public behavior, and setup knowledge                       |
| Evolve   | [`deprecation-and-migration`](../deprecation-and-migration/SKILL.md)                 | Replace or retire systems without stranding consumers                          |
| Automate | [`ci-cd-and-automation`](../ci-cd-and-automation/SKILL.md)                           | Enforce quality and deployment gates                                           |
| Ship     | [`git-workflow-and-versioning`](../git-workflow-and-versioning/SKILL.md)             | Structure authorized Git and release-history work                              |
| Ship     | [`shipping-and-launch`](../shipping-and-launch/SKILL.md)                             | Plan and execute authorized rollout, monitoring, and rollback                  |

Routing is complete when every task concern maps to a sibling skill or a named repository-native
process. The task is complete only after every selected workflow's verification and the Definition
of Done pass.
