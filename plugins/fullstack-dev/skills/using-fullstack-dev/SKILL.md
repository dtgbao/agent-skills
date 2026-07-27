---
name: using-fullstack-dev
description: Routes full-stack app development from codebase architecture and database design through backend contracts to frontend delivery. Use at the start of a full-stack build or when coordinating modules, seams, database schemas, services, APIs, UI, security, performance, review, Git, or releases.
---

# Using Fullstack Dev

## Purpose

Use this meta-skill to guide an app from its data model and persistence boundary through backend
services and API contracts to the frontend. Treat each selected skill as the source of truth for
its domain.

Use repository-native requirements, implementation, testing, debugging, and deployment processes;
this plugin contributes the end-to-end design sequence and engineering lenses listed below.

## Route the Task

Identify every branch that matches the work:

```text
Full-stack app
│
├── Choosing modules, interfaces, or seams? ──────→ codebase-design
├── Designing a data model or database schema? -──→ supabase-postgres-best-practices
├── Designing backend services or API contracts? ─→ api-and-interface-design
├── Building the user interface? ─────────────────→ frontend-ui-engineering
│
├── Crossing a trust boundary? ───────────────────→ security-and-hardening
├── Meeting or diagnosing a performance target? ──→ performance-optimization
├── Reviewing a completed change? ────────────────→ code-review-and-quality
│   └── Behavior is correct but code is complex? ─→ code-simplification
└── Branching, committing, resolving, releasing? ─→ git-workflow-and-versioning
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

4. **Build the frontend against those contracts.**
   - Use [`frontend-ui-engineering`](../frontend-ui-engineering/SKILL.md) for pages, components, state, responsive behavior,
     accessibility, and integration with the typed contracts.
   - Completion criterion: every user flow is represented in the UI and the skill's accessibility,
     responsive, and runtime checks pass.

5. **Add cross-cutting constraints while designing and implementing.**
   - Use [`security-and-hardening`](../security-and-hardening/SKILL.md) when untrusted input, authentication, authorization, sensitive
     data, uploads, webhooks, external services, or model output crosses a boundary.
   - Use [`performance-optimization`](../performance-optimization/SKILL.md) when the task has a measurable target, reported regression,
     scale risk, or profiled bottleneck.
   - Completion criterion: every trust boundary and stated performance concern is covered by its
     skill, and each selected skill's verification passes.

6. **Close the change.**
   - Use [`code-review-and-quality`](../code-review-and-quality/SKILL.md) after implementation or refactoring and before merge.
   - Use [`code-simplification`](../code-simplification/SKILL.md) only when behavior is already verified and complexity warrants a
     focused, behavior-preserving pass; review again after changing the code.
   - Use [`git-workflow-and-versioning`](../git-workflow-and-versioning/SKILL.md) for change hygiene and for user-authorized branch, commit,
     conflict, version, tag, changelog, and release work.
   - Completion criterion: review blockers are resolved, all selected verification checklists
     pass, and requested Git or release operations are complete.

## Common Sequences

```text
Full-stack feature
codebase-design (modules, interfaces, and seams)
→ supabase-postgres-best-practices (data and schema)
→ api-and-interface-design (services and API) → frontend-ui-engineering
→ security-and-hardening (if a boundary exists)
→ performance-optimization (if measured) → code-review-and-quality

Backend change
codebase-design (if module shape changes)
→ supabase-postgres-best-practices (if persistence changes) → api-and-interface-design
→ security-and-hardening (if a boundary exists) → code-review-and-quality

UI change
codebase-design (if module shape changes) → frontend-ui-engineering
→ security-and-hardening (if a boundary exists)
→ performance-optimization (if measured) → code-review-and-quality

Behavior-preserving refactor
codebase-design (if seams or interfaces change) → code-simplification
→ code-review-and-quality

Release
code-review-and-quality → git-workflow-and-versioning
```

Apply [`git-workflow-and-versioning`](../git-workflow-and-versioning/SKILL.md) throughout code-changing sequences when Git operations are in
scope.

Routing is complete when every concern in the task maps to a listed skill or a named
repository-native process. The task is complete only when the criteria above and every selected
skill's verification checklist pass.
