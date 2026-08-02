# Fullstack Dev Plugin

Guide full-stack application development from decision discovery, requirements, and planning through
architecture, data, APIs, source-verified implementation, frontend delivery, operations, migration,
review, and launch.

## Install

Add this repository as a Codex marketplace, then install the plugin:

```bash
codex plugin marketplace add dtgbao/agent-skills
codex plugin add fullstack-dev@bao-plugins
```

Start a new Codex task after installation so all bundled skills are available.

## Lifecycle

| Stage         | Skill                                                                                  | Purpose                                                         |
| ------------- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Route         | [`using-fullstack-dev`](skills/using-fullstack-dev/SKILL.md)                           | Discover and sequence every applicable skill.                   |
| Clarification | [`grilling`](skills/grilling/SKILL.md)                                                 | Stress-test ideas and resolve decisions one question at a time.  |
| Definition    | [`spec-driven-development`](skills/spec-driven-development/SKILL.md)                   | Define approved requirements, boundaries, and success criteria. |
| Planning      | [`planning-and-task-breakdown`](skills/planning-and-task-breakdown/SKILL.md)           | Create dependency-ordered, verifiable implementation tasks.     |
| Architecture | [`codebase-design`](skills/codebase-design/SKILL.md)                                   | Choose deep modules, small interfaces, seams, and adapters.  |
| Database     | [`supabase-postgres-best-practices`](skills/supabase-postgres-best-practices/SKILL.md) | Apply specialized database guidance when its engine matches. |
| Backend      | [`api-and-interface-design`](skills/api-and-interface-design/SKILL.md)                 | Define service boundaries and typed API contracts.           |
| Sources      | [`source-driven-development`](skills/source-driven-development/SKILL.md)               | Verify version-sensitive work against official sources.      |
| Testing      | [`test-driven-development`](skills/test-driven-development/SKILL.md)                   | Drive every behavior change through a failing test.          |
| Frontend     | [`frontend-ui-engineering`](skills/frontend-ui-engineering/SKILL.md)                   | Build accessible, responsive interfaces against contracts.   |
| ↳ React      | [`react-best-practices`](skills/react-best-practices/SKILL.md)                        | Apply React architecture guidance within frontend work.       |
| Automation   | [`ci-cd-and-automation`](skills/ci-cd-and-automation/SKILL.md)                         | Automate repository quality and deployment gates.            |
| Launch       | [`shipping-and-launch`](skills/shipping-and-launch/SKILL.md)                           | Plan authorized rollout, verification, and recovery.         |
| Versioning   | [`git-workflow-and-versioning`](skills/git-workflow-and-versioning/SKILL.md)           | Guide authorized Git, version, changelog, and release work.  |

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
- [`code-simplification`](skills/code-simplification/SKILL.md) for focused,
  behavior-preserving clarity improvements.
- [`code-review-and-quality`](skills/code-review-and-quality/SKILL.md) before merge or release.

Use the bundled database skill when it matches the project's engine. Otherwise, follow the
repository's native database conventions and continue the lifecycle at backend contract design.
