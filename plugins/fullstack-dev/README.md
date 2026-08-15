# Fullstack Dev Plugin

Guide full-stack application development from focused context, decision discovery, requirements,
and planning through architecture, design patterns, data, APIs, NestJS and FastAPI services,
source-verified implementation, Python and frontend testing, behavior-preserving refactoring,
operations, migration, review, and launch.

## Install with Codex

Add this repository as a Codex marketplace, then install the plugin:

```bash
codex plugin marketplace add dtgbao/agent-skills
codex plugin add fullstack-dev@bao-plugins
```

Start a new Codex task after installation so all bundled skills are available.

## Install with Claude Code

Add this repository as a Claude Code marketplace, then install the plugin:

```text
/plugin marketplace add dtgbao/agent-skills
/plugin install fullstack-dev@bao-plugins
```

## Use

Invoke the manual full-stack router with a task:

```text
/fullstack-dev <task>
```

The command reads the bundled [`index`](skills/index/SKILL.md) and follows its routing instructions.

## Lifecycle

| Stage         | Skill                                                                                  | Purpose                                                                                       |
| ------------- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Route         | [`index`](skills/index/SKILL.md)                                                       | Discover and sequence every applicable skill.                                                 |
| Context       | [`context-engineering`](skills/context-engineering/SKILL.md)                           | Curate project rules and focused context for each task.                                       |
| Sources       | [`source-driven-development`](skills/source-driven-development/SKILL.md)               | Verify version-sensitive work against official sources.                                       |
| Clarification | [`grilling`](skills/grilling/SKILL.md)                                                 | Stress-test ideas by resolving each unblocked decision frontier in rounds.                    |
| Definition    | [`spec-driven-development`](skills/spec-driven-development/SKILL.md)                   | Define approved requirements, boundaries, and success criteria with the smallest useful view. |
| Planning      | [`planning-and-task-breakdown`](skills/planning-and-task-breakdown/SKILL.md)           | Create dependency-ordered, verifiable implementation tasks.                                   |
| Architecture  | [`codebase-design`](skills/codebase-design/SKILL.md)                                   | Choose deep modules, small interfaces, seams, and adapters.                                   |
| ↳ Patterns    | [`design-pattern`](skills/design-pattern/SKILL.md)                                     | Apply GoF patterns to object-oriented TypeScript when warranted.                              |
| Database      | [`supabase-postgres-best-practices`](skills/supabase-postgres-best-practices/SKILL.md) | Apply specialized database guidance when its engine matches.                                  |
| Interfaces    | [`api-and-interface-design`](skills/api-and-interface-design/SKILL.md)                 | Define service boundaries and typed API contracts.                                            |
| Backend       | [`nestjs-best-practices`](skills/nestjs-best-practices/SKILL.md)                       | Apply production-ready NestJS architecture and practices.                                     |
| ↳ FastAPI     | [`fastapi-best-practices`](skills/fastapi-best-practices/SKILL.md)                     | Apply source-verified Python and FastAPI production practices.                                |
| Testing       | [`test-driven-development`](skills/test-driven-development/SKILL.md)                   | Drive every behavior change through a failing test.                                           |
| ↳ Python      | [`python-testing-best-practices`](skills/python-testing-best-practices/SKILL.md)       | Apply reliable Python, pytest, and FastAPI testing patterns.                                  |
| ↳ Vitest API  | [`vitest`](skills/vitest/SKILL.md)                                                     | Look up current Vitest APIs, configuration, and CLI behavior.                                 |
| ↳ Practices   | [`vitest-best-practices`](skills/vitest-best-practices/SKILL.md)                       | Write reliable Vitest and component tests.                                                    |
| Refactoring   | [`refactoring`](skills/refactoring/SKILL.md)                                           | Diagnose code smells and apply behavior-preserving techniques.                                |
| Frontend      | [`frontend-ui-engineering`](skills/frontend-ui-engineering/SKILL.md)                   | Build accessible, responsive interfaces against contracts.                                    |
| ↳ React       | [`react-best-practices`](skills/react-best-practices/SKILL.md)                         | Apply React architecture guidance within frontend work.                                       |
| Automation    | [`ci-cd-and-automation`](skills/ci-cd-and-automation/SKILL.md)                         | Automate repository quality and deployment gates.                                             |
| Launch        | [`shipping-and-launch`](skills/shipping-and-launch/SKILL.md)                           | Plan authorized rollout, verification, and recovery.                                          |
| Versioning    | [`git-workflow-and-versioning`](skills/git-workflow-and-versioning/SKILL.md)           | Guide authorized Git, version, changelog, and release work.                                   |

Apply these skills wherever their concern appears:

- [`security-and-hardening`](skills/security-and-hardening/SKILL.md) for trust boundaries,
  authentication, sensitive data, and external integrations.
- [`performance-optimization`](skills/performance-optimization/SKILL.md) for measurable performance
  requirements or regressions.
- [`observability-and-instrumentation`](skills/observability-and-instrumentation/SKILL.md) for
  logs, metrics, traces, and alerts.
- [`documentation-and-adrs`](skills/documentation-and-adrs/SKILL.md) for decisions and public
  behavior.
- [`debugging-and-error-recovery`](skills/debugging-and-error-recovery/SKILL.md) for failing tests,
  builds, and runtime behavior.
- [`deprecation-and-migration`](skills/deprecation-and-migration/SKILL.md) for replacing or removing
  existing systems safely.
- [`refactoring`](skills/refactoring/SKILL.md) for diagnosing code smells and selecting named,
  behavior-preserving transformations.
- [`code-simplification`](skills/code-simplification/SKILL.md) for focused,
  behavior-preserving clarity improvements; use it with `refactoring` when both concerns apply.
- [`code-review-and-quality`](skills/code-review-and-quality/SKILL.md) before merge or release.

Use the bundled database skill when it matches the project's engine. Otherwise, follow the
repository's native database conventions and continue the lifecycle at backend contract design.
