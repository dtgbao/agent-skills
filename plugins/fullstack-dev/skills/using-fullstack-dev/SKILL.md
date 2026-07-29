---
name: using-fullstack-dev
description: Routes cross-domain full-stack work through specialist skills in dependency order. Use for builds or changes spanning architecture, data, APIs, UI, operations, or delivery.
---

# Using Fullstack Dev

Load every matching sibling skill before acting; map uncovered concerns to repository-native
processes.

## Route

| Concern | Skill |
| --- | --- |
| Architecture, modules, interfaces, or seams | [`codebase-design`](../codebase-design/SKILL.md) |
| Database schemas, queries, or configuration | [`supabase-postgres-best-practices`](../supabase-postgres-best-practices/SKILL.md) |
| Backend services, APIs, or public contracts | [`api-and-interface-design`](../api-and-interface-design/SKILL.md) |
| Pages, components, state, accessibility, or responsive behavior | [`frontend-ui-engineering`](../frontend-ui-engineering/SKILL.md) |
| New or changed behavior, including bug fixes | [`test-driven-development`](../test-driven-development/SKILL.md) |
| Trust boundaries or untrusted data | [`security-and-hardening`](../security-and-hardening/SKILL.md) |
| Performance targets, regressions, or bottlenecks | [`performance-optimization`](../performance-optimization/SKILL.md) |
| Production logs, metrics, traces, or alerts | [`observability-and-instrumentation`](../observability-and-instrumentation/SKILL.md) |
| Decisions, public APIs, setup, or user-visible behavior | [`documentation-and-adrs`](../documentation-and-adrs/SKILL.md) |
| Failing tests, builds, runtime behavior, or expectations | [`debugging-and-error-recovery`](../debugging-and-error-recovery/SKILL.md) |
| Replacing, removing, or migrating a system | [`deprecation-and-migration`](../deprecation-and-migration/SKILL.md) |
| Automated quality or deployment gates | [`ci-cd-and-automation`](../ci-cd-and-automation/SKILL.md) |
| Completed work before merge | [`code-review-and-quality`](../code-review-and-quality/SKILL.md) |
| Verified behavior with unnecessary complexity | [`code-simplification`](../code-simplification/SKILL.md) |
| Branches, commits, conflicts, versions, tags, or changelogs | [`git-workflow-and-versioning`](../git-workflow-and-versioning/SKILL.md) |
| Production deployment, rollout, monitoring, or rollback | [`shipping-and-launch`](../shipping-and-launch/SKILL.md) |

## Coordinate

- Order design dependencies: `codebase-design` → `supabase-postgres-best-practices` →
  `api-and-interface-design` → affected implementation skills.
- Pair `test-driven-development` with every behavior-changing implementation slice.
- Apply matched security, performance, observability, and documentation skills alongside
  implementation.
- On failure, run `debugging-and-error-recovery`; resume after its verification passes.
- For replacement or removal, start with `deprecation-and-migration`, then run the affected domain
  skills.
- After implementation, run `ci-cd-and-automation`, then `code-review-and-quality`. When
  simplification is warranted, simplify verified behavior and review again.
- Finish with `git-workflow-and-versioning` and `shipping-and-launch` when their routed concerns are
  in scope.

Routing is complete when every concern maps to a sibling skill or named repository-native process.
Complete the task after every selected skill's verification passes.
