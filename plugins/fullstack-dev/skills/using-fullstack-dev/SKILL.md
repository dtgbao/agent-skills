---
name: using-fullstack-dev
description: Routes full-stack app development from architecture and database design through test-driven implementation, operations, migration, and launch. Use at the start of a full-stack build or when coordinating modules, data, APIs, UI, testing, security, performance, debugging, observability, documentation, CI/CD, deprecation, review, Git, or releases.
---

# Using Fullstack Dev

## Purpose

Use this meta-skill to guide an app from codebase and data design through test-driven backend and
frontend delivery, production operations, and launch. Treat each selected skill as the source of
truth for its domain.

Use repository-native requirements, planning, implementation, and testing processes; this plugin
contributes the design, test-driven development, operational, migration, quality, and delivery
workflows below.

## Route the Task

Identify every branch that matches the work:

```text
Full-stack app
│
├── Choosing modules, interfaces, or seams? ──────────→ codebase-design
├── Designing a data model or database schema? ───────→ supabase-postgres-best-practices
├── Designing backend services or API contracts? ─────→ api-and-interface-design
├── Building the user interface? ─────────────────────→ frontend-ui-engineering
├── Adding or changing behavior, or fixing a bug? ─────→ test-driven-development
│
├── Crossing a trust boundary? ───────────────────────→ security-and-hardening
├── Meeting or diagnosing a performance target? ──────→ performance-optimization
├── Adding production logs, metrics, traces, alerts? ─→ observability-and-instrumentation
├── Recording a decision, API, or behavior change? ───→ documentation-and-adrs
│
├── Tests, builds, or runtime behavior failing? ──────→ debugging-and-error-recovery
├── Replacing or removing an existing system? ────────→ deprecation-and-migration
│
├── Automating quality or deployment gates? ──────────→ ci-cd-and-automation
├── Reviewing completed work? ────────────────────────→ code-review-and-quality
│   └── Behavior is correct but code is complex? ─────→ code-simplification
├── Branching, committing, resolving, versioning? ────→ git-workflow-and-versioning
└── Deploying, rolling out, or launching? ────────────→ shipping-and-launch
```

Load and follow every matching sibling skill before making its corresponding design or code
change; the branches are cumulative.

## Apply the Skills

1. **Design the codebase shape.**
   - Use [`codebase-design`](../codebase-design/SKILL.md) to choose deep modules, small interfaces, clean seams, and adapters
     before committing to detailed database, backend, or frontend structure.
   - Completion criterion: every major responsibility has one module, each interface hides
     meaningful implementation complexity, seams sit where behavior really varies, and callers
     and tests use the same interface.

2. **Model the data and persistence boundary.**
   - Use [`supabase-postgres-best-practices`](../supabase-postgres-best-practices/SKILL.md) for Postgres schemas, data types, keys, constraints,
     indexes, RLS, queries, connections, transactions, locking, and database diagnostics.
   - Follow repository-native database conventions when the project uses another database engine.
   - Use [`api-and-interface-design`](../api-and-interface-design/SKILL.md) to keep the database schema, domain types, and service contract
     aligned without leaking persistence details.
   - Completion criterion: every required datum has one owner, relationships and invariants are
     enforced by the schema, applicable Postgres rules pass, and the service layer can expose the
     model without coupling consumers to storage details.

3. **Design backend services and API contracts.**
   - Use [`api-and-interface-design`](../api-and-interface-design/SKILL.md) for service boundaries, endpoints, request and response schemas,
     error contracts, compatibility, and the interface between backend and frontend.
   - Completion criterion: every frontend use case maps to a typed service or API contract, and the
     skill's verification passes.

4. **Drive behavioral work test-first.**
   - Use [`test-driven-development`](../test-driven-development/SKILL.md) before implementing new logic, fixing a bug, modifying
     existing behavior, or adding edge-case handling. It wraps the matching domain skill rather
     than running after implementation.
   - Work one public seam at a time: write and confirm the failing test, add the minimum code
     needed to pass, then refactor only while the tests stay green.
   - Completion criterion: every new behavior has a corresponding test, every bug fix has a
     reproduction test that failed before the fix, no tests are skipped or disabled, and the
     repository's focused and full-suite verification passes.

5. **Build the frontend against those contracts.**
   - Use [`frontend-ui-engineering`](../frontend-ui-engineering/SKILL.md) for pages, components, state, responsive behavior,
     accessibility, and integration with the typed contracts.
   - Completion criterion: every user flow is represented in the UI and the skill's accessibility,
     responsive, and runtime checks pass.

6. **Build operational guardrails alongside the feature.**
   - Use [`security-and-hardening`](../security-and-hardening/SKILL.md) when untrusted input, authentication, authorization, sensitive
     data, uploads, webhooks, external services, or model output crosses a boundary.
   - Use [`performance-optimization`](../performance-optimization/SKILL.md) when the task has a measurable target, reported regression,
     scale risk, or profiled bottleneck.
   - Use [`observability-and-instrumentation`](../observability-and-instrumentation/SKILL.md) while building production endpoints, jobs,
     integrations, retries, queues, or cross-service calls so their behavior is diagnosable.
   - Use [`documentation-and-adrs`](../documentation-and-adrs/SKILL.md) when architecture, a public interface, setup, or user-visible
     behavior changes.
   - Completion criterion: every trust boundary is hardened, performance claims are measured,
     production behavior is observable, and significant decisions and public behavior are current
     in the repository's documentation.

7. **Interrupt the sequence for failures or migrations.**
   - Use [`debugging-and-error-recovery`](../debugging-and-error-recovery/SKILL.md) immediately when a test, build, runtime path, or
     expectation fails. Resume the lifecycle only after the root cause and regression guard are
     verified.
   - Use [`deprecation-and-migration`](../deprecation-and-migration/SKILL.md) when replacing or removing a system, API, schema, or
     feature. Inventory consumers, provide a proven replacement, migrate incrementally, and verify
     zero active usage before removal.
   - Completion criterion: each failure is fixed at its root and guarded against recurrence; each
     migration preserves compatibility through cutover and removes the old path only after its
     consumers are gone.

8. **Automate and review the change.**
   - Use [`ci-cd-and-automation`](../ci-cd-and-automation/SKILL.md) to enforce the repository's lint, type, test, build, security, and
     deployment gates.
   - Use [`code-review-and-quality`](../code-review-and-quality/SKILL.md) after implementation or refactoring and before merge.
   - Use [`code-simplification`](../code-simplification/SKILL.md) only when behavior is already verified and complexity warrants a
     focused, behavior-preserving pass; review again after changing the code.
   - Use [`git-workflow-and-versioning`](../git-workflow-and-versioning/SKILL.md) for change hygiene and for user-authorized branch, commit,
     conflict, version, tag, changelog, and release work.
   - Completion criterion: automated gates pass, review blockers are resolved, all selected
     verification checklists pass, and requested Git operations are complete.

9. **Ship and verify the launch.**
   - Use [`shipping-and-launch`](../shipping-and-launch/SKILL.md) for user-authorized production deployments, staged rollouts, launch monitoring, and rollback planning.
   - Use [`ci-cd-and-automation`](../ci-cd-and-automation/SKILL.md) for the deployment mechanism, [`observability-and-instrumentation`](../observability-and-instrumentation/SKILL.md) for health evidence, [`documentation-and-adrs`](../documentation-and-adrs/SKILL.md) for release documentation, and [`git-workflow-and-versioning`](../git-workflow-and-versioning/SKILL.md) for versions and tags.
   - Completion criterion: the pre-launch gate passes, rollout and rollback thresholds are explicit, and post-launch health checks confirm the release is operating normally.

## Common Sequences

```text
Full-stack feature
codebase-design (modules, interfaces, and seams)
→ supabase-postgres-best-practices (data and schema)
→ api-and-interface-design (services and API)
→ test-driven-development (wrap each behavioral implementation slice)
→ frontend-ui-engineering
→ security-and-hardening (if a boundary exists) + observability-and-instrumentation
→ performance-optimization (if measured) + documentation-and-adrs (if a decision changes)
→ ci-cd-and-automation → code-review-and-quality → shipping-and-launch

Bug fix
test-driven-development (reproduction and regression guard) + debugging-and-error-recovery
→ affected domain skill
→ observability-and-instrumentation (if telemetry was missing)
→ ci-cd-and-automation → code-review-and-quality

Deprecation or migration
deprecation-and-migration → test-driven-development
→ affected architecture, database, API, or UI skills
→ observability-and-instrumentation + documentation-and-adrs
→ ci-cd-and-automation → code-review-and-quality → shipping-and-launch

Behavior-preserving refactor
test-driven-development (refactor phase with tests green)
→ codebase-design (if seams or interfaces change) → code-simplification
→ ci-cd-and-automation → code-review-and-quality

Release
documentation-and-adrs + observability-and-instrumentation
→ ci-cd-and-automation → code-review-and-quality
→ git-workflow-and-versioning → shipping-and-launch
```

Apply [`test-driven-development`](../test-driven-development/SKILL.md) throughout behavior-changing sequences so each implementation
step follows its test-first cycle.

Apply [`git-workflow-and-versioning`](../git-workflow-and-versioning/SKILL.md) throughout code-changing sequences when Git operations are in scope.

Routing is complete when every concern in the task maps to a listed skill or a named
repository-native process. The task is complete only when the criteria above and every selected
skill's verification checklist pass; production work also clears the launch and post-launch gates.
