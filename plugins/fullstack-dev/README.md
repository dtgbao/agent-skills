# Fullstack Dev Plugin

Guide full-stack application development from codebase architecture and Supabase/Postgres design
through backend services, APIs, frontend delivery, review, and release.

## Install

Add this repository as a Codex marketplace, then install the plugin:

```bash
codex plugin marketplace add dtgbao/agent-skills
codex plugin add fullstack-dev@bao-plugins
```

Start a new Codex task after installation so all bundled skills are available.

## Lifecycle

| Stage | Skill | Purpose |
| --- | --- | --- |
| Route | [`using-fullstack-dev`](skills/using-fullstack-dev/SKILL.md) | Select and sequence every applicable skill. |
| Architecture | [`codebase-design`](skills/codebase-design/SKILL.md) | Choose deep modules, small interfaces, seams, and adapters. |
| Database | [`supabase-postgres-best-practices`](skills/supabase-postgres-best-practices/SKILL.md) | Design and optimize Supabase/Postgres schemas, queries, connections, and RLS. |
| Backend | [`api-and-interface-design`](skills/api-and-interface-design/SKILL.md) | Define service boundaries and typed API contracts. |
| Frontend | [`frontend-ui-engineering`](skills/frontend-ui-engineering/SKILL.md) | Build accessible, responsive interfaces against those contracts. |
| Delivery | [`git-workflow-and-versioning`](skills/git-workflow-and-versioning/SKILL.md) | Keep changes reviewable and prepare versions and releases. |

Apply these skills wherever their concern appears:

- [`security-and-hardening`](skills/security-and-hardening/SKILL.md) for trust boundaries,
  authentication, sensitive data, and external integrations.
- [`performance-optimization`](skills/performance-optimization/SKILL.md) for measurable performance
  requirements or regressions.
- [`code-simplification`](skills/code-simplification/SKILL.md) for focused,
  behavior-preserving clarity improvements.
- [`code-review-and-quality`](skills/code-review-and-quality/SKILL.md) before merge or release.

For database engines other than Postgres, follow the repository's native database conventions and
continue the lifecycle at backend contract design.

## Example Prompts

- Guide this app from database design to backend APIs and frontend.
- Design the modules, Supabase schema, services, and UI for this feature.
- Review, harden, and prepare this full-stack change for release.
