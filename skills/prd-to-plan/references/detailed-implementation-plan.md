# Detailed Implementation Plan Reference

Create a plan that a capable engineer with little repo context can execute task by task.

The plan must include all sections required by `writing-plans`, plus these sections before the task checklist:

```markdown
## Requirement Traceability
| PRD item | Implementation tasks | Tests |
|---|---|---|

## Component Design
| Component | File path | Responsibility | Dependencies | Interface |
|---|---|---|---|---|

## Implementation Map
| File | Create/Modify | Detailed changes |
|---|---|---|

## Data Flow
[Complete flow from entry points through validation, state changes, transformations, persistence/API calls, and outputs.]

## API Contracts
[Routes, methods, payloads, responses, error formats, auth requirements, and backward compatibility notes.]

## Schema Changes
[Database, config, validation, generated types, migrations, or "None".]

## Architectural Decisions
[Approved decisions and rejected alternatives.]

## Technical Clarifications
[Assumptions, developer questions already resolved, and remaining questions.]

## Critical Details
[Error handling, state management, testing, performance, security, observability, accessibility, and rollout.]
```

If a section does not apply, write `None because [specific reason]`. Do not write `TBD`, `TODO`, or placeholders.

Use the test pyramid as the default allocation:

- Unit tests: about 80%, small, single-process, no I/O, no network, no database.
- Integration tests: about 15%, medium, local boundaries such as API, database, file system, or component interactions.
- E2E tests: about 5%, large, only critical user flows in a real browser or equivalent full stack.

For each user story and acceptance criterion:

1. List happy-path scenarios.
2. List realistic alternate flows.
3. List edge cases.
4. List validation and error cases.
5. Map each scenario to unit, integration, or E2E tests.
6. Prefer the smallest test that gives confidence.
7. Show concrete test names and representative test code or pseudocode in the relevant task.

Apply the Beyonce Rule: any behavior the plan depends on should have a test. Infrastructure, refactoring, and migrations do not substitute for tests.

Classify test size explicitly:

- Small: no I/O, no network, no database.
- Medium: localhost or local test database only.
- Large: external services, browser E2E, staging, or performance benchmark.

Follow `writing-plans` task structure:

- Each task should be independently reviewable.
- Each task starts with a failing test or a verification step when no test is possible.
- Each task includes exact file paths.
- Each code-changing step includes concrete code, not vague instructions.
- Each task includes exact commands and expected results.
- Include frequent commits.

If exact code cannot be responsibly written without more local context, do more codebase exploration before writing the plan.

Before presenting the plan:

- Check every PRD user story and acceptance criterion maps to at least one task and one test.
- Check every approved architecture decision appears in the plan.
- Check there are no placeholders such as `TBD`, `TODO`, `implement later`, or "add appropriate error handling".
- Check test distribution follows the pyramid unless there is a stated reason to differ.
- Check file paths, function names, types, routes, and component interfaces are consistent.
- Check the mermaid diagram and detailed plan describe the same architecture.

End with the execution handoff from `writing-plans`, offering subagent-driven or inline execution.
