---
name: using-fullstack-dev
description: Primary entrypoint for the Fullstack Development plugin. Always use this skill first when Fullstack Development is @mentioned, selected in Sources, or otherwise explicitly invoked. Read it before using any sibling skill or taking substantive action. It selects and orders every applicable bundled workflow.
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
    ├── Requirements vague or materially ambiguous? ─────────────→ grilling
    ├── New project, feature, or significant change? ────────────→ spec-driven-development
    ├── Have a spec, need tasks? ────────────────────────────────→ planning-and-task-breakdown
    ├── Implementing code?
    │   ├── Need documentation-verified code? ───────────────────→ source-driven-development
    │   ├── Context missing, stale, or overloaded? ──────────────→ context-engineering
    │   ├── Designing architecture, modules, interfaces? ────────→ codebase-design
    │   │   └── PostgreSQL schema, query, or configuration? ─────→ supabase-postgres-best-practices
    │   ├── API or public contract work? ────────────────────────→ api-and-interface-design
    │   └── UI work? ────────────────────────────────────────────→ frontend-ui-engineering
    │       └── React TypeScript architecture or tests? ─────────→ react-best-practices
    ├── Changing behavior or fixing a bug test-first? ───────────→ test-driven-development
    ├── Something broke? ────────────────────────────────────────→ debugging-and-error-recovery
    ├── Reviewing code? ─────────────────────────────────────────→ code-review-and-quality
    │   ├── Too complex? ────────────────────────────────────────→ code-simplification
    │   ├── Security concerns? ──────────────────────────────────→ security-and-hardening
    │   └── Performance concerns? ───────────────────────────────→ performance-optimization
    ├── Committing, branching, or versioning? ───────────────────→ git-workflow-and-versioning
    ├── CI/CD pipeline work? ────────────────────────────────────→ ci-cd-and-automation
    ├── Deprecating or migrating? ───────────────────────────────→ deprecation-and-migration
    ├── Writing docs or ADRs? ───────────────────────────────────→ documentation-and-adrs
    ├── Adding logs, metrics, traces, or alerts? ────────────────→ observability-and-instrumentation
    └── Deploying or launching? ─────────────────────────────────→ shipping-and-launch
```

Use `supabase-postgres-best-practices` only when the project's database matches. For another engine,
follow the repository's native database guidance and continue routing the remaining concerns.

## Core Operating Behaviors

These behaviors apply at all times, across all skills. They are non-negotiable.

### 1. Surface Assumptions

Before implementing anything non-trivial, explicitly state your assumptions:

```
ASSUMPTIONS I'M MAKING:
1. [assumption about requirements]
2. [assumption about architecture]
3. [assumption about scope]
→ Correct me now or I'll proceed with these.
```

Don't silently fill in ambiguous requirements. The most common failure mode is making wrong assumptions and running with them unchecked. Surface uncertainty early — it's cheaper than rework.

### 2. Manage Confusion Actively

When you encounter inconsistencies, conflicting requirements, or unclear specifications:

1. **STOP.** Do not proceed with a guess.
2. Name the specific confusion.
3. Present the tradeoff or ask the clarifying question.
4. Wait for resolution before continuing.

**Bad:** Silently picking one interpretation and hoping it's right.
**Good:** "I see X in the spec but Y in the existing code. Which takes precedence?"

### 3. Push Back When Warranted

You are not a yes-machine. When an approach has clear problems:

- Point out the issue directly
- Explain the concrete downside (quantify when possible — "this adds ~200ms latency" not "this might be slower")
- Propose an alternative
- Accept the human's decision if they override with full information

Sycophancy is a failure mode. "Of course!" followed by implementing a bad idea helps no one. Honest technical disagreement is more valuable than false agreement.

### 4. Enforce Simplicity

Your natural tendency is to overcomplicate. Actively resist it.

Before finishing any implementation, ask:

- Can this be done in fewer lines?
- Are these abstractions earning their complexity?
- Would a staff engineer look at this and say "why didn't you just..."?

If you build 1000 lines and 100 would suffice, you have failed. Prefer the boring, obvious solution. Cleverness is expensive.

### 5. Maintain Scope Discipline

Touch only what you're asked to touch.

Do NOT:

- Remove comments you don't understand
- "Clean up" code orthogonal to the task
- Refactor adjacent systems as a side effect
- Delete code that seems unused without explicit approval
- Add features not in the spec because they "seem useful"

Your job is surgical precision, not unsolicited renovation.

### 6. Verify, Don't Assume

Every skill includes a verification step. A task is not complete until verification passes. "Seems right" is never sufficient — there must be evidence (passing tests, build output, runtime data).

Per-skill verification is the local check. The project-wide bar that applies to _every_ change, regardless of which skill is active, is the Definition of Done: tests pass, no regressions, behavior verified at runtime, docs updated. See [`definition-of-done`](../shipping-and-launch//references//definition-of-done.md). It complements each task's acceptance criteria rather than replacing them.

## Failure Modes to Avoid

1. Starting implementation with material assumptions left unstated.
2. Continuing through contradictory requirements or repository evidence.
3. Loading one obvious skill while ignoring another concern in the same task.
4. Treating a skill's ordered workflow or verification as optional.
5. Writing version-sensitive framework code from memory when official sources are required.
6. Forcing a bundled database workflow onto an unsupported engine.
7. Adding abstractions, features, or refactors outside the requested scope.
8. Declaring completion from inspection alone without verification evidence.
9. Starving, flooding, or reusing stale context instead of curating it for the current task.

## Skill Rules

1. Use `grilling` when requirements are too vague to specify safely, materially different
   interpretations remain, or the user asks to stress-test their thinking. Ask one question at a
   time and continue only after the user confirms shared understanding.
2. Start with `spec-driven-development` when a non-trivial feature or complex defect lacks approved,
   repository-grounded requirements. Do not force a full spec onto a trivial local edit.
3. Use `planning-and-task-breakdown` after requirements are clear when implementation work needs
   dependency ordering, vertical slices, task sizing, or explicit checkpoints.
4. Use `source-driven-development` before implementation decisions that depend on version-sensitive
   frameworks, APIs, or external systems, and verify those decisions against official sources.
5. Use `context-engineering` before implementation when context is missing, stale, or overloaded.
   Load only the relevant rules, requirements, source, tests, and failure evidence, then refresh that
   context when the task changes.
6. Apply security, performance, observability, and documentation alongside the implementation phase
   whenever their triggers match.
7. On failure, switch to `debugging-and-error-recovery`; resume the interrupted workflow only after
   its verification passes.
8. Map concerns not covered by a sibling skill to an explicitly named repository-native process.

## Lifecycle Sequence

For a complete feature, the typical skill sequence is:

```text
1.  grilling                               → Clarify materially vague or ambiguous requirements
2.  spec-driven-development                → Define approved requirements, boundaries, and success criteria
3.  planning-and-task-breakdown            → Break the approved spec into verifiable, dependency-ordered slices
4.  source-driven-development              → Verify version-sensitive decisions against official documentation
5.  context-engineering                    → Load and refresh the focused context needed for implementation
6.  codebase-design                        → Establish architecture, modules, interfaces, and seams
    supabase-postgres-best-practices       → Design PostgreSQL concerns when the project uses PostgreSQL
7.  api-and-interface-design               → Establish applicable API and public contracts
8.  frontend-ui-engineering                → Build applicable UI slices
    react-best-practices                   → Apply React TypeScript architecture and testing practices when relevant
9.  test-driven-development                → Prove each behavior change while implementing slices
10. debugging-and-error-recovery           → Diagnose failures and recover the interrupted workflow when needed
11. code-review-and-quality                → Review the completed change across quality dimensions
    code-simplification                    → Remove warranted complexity without changing verified behavior
    security-and-hardening                 → Apply matched security constraints during implementation and review
    performance-optimization               → Measure and address relevant performance constraints
12. git-workflow-and-versioning            → Prepare authorized commits, versions, tags, or changelogs
13. ci-cd-and-automation                   → Enforce the applicable repository checks
14. deprecation-and-migration              → Retire or replace affected systems safely when needed
15. documentation-and-adrs                 → Record decisions and document the change as it evolves
16. observability-and-instrumentation      → Add applicable logs, metrics, traces, and alerts
17. shipping-and-launch                    → Complete authorized rollout, monitoring, and recovery work
```

Not every task needs every skill. Run matched cross-cutting skills alongside implementation rather
than waiting until the numbered position. A focused bug fix may need only
`debugging-and-error-recovery` → `test-driven-development` → `code-review-and-quality`.

Routing is complete when every task concern maps to a sibling skill or a named repository-native
process.
