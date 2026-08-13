---
name: fastapi-best-practices
description: Source-verified Python 3.11+ and FastAPI practices for production APIs. Use when writing, reviewing, debugging, or refactoring FastAPI code involving application structure, typing, dependency injection, errors, security, async execution, databases, API contracts, or deployment.
---

# FastAPI Best Practices

Apply 36 production rules across 9 categories. Treat FastAPI as the primary framework and use
general Python guidance only where it materially affects API correctness or maintainability.

## Start With Versions

Before selecting a rule or writing code:

1. Read `pyproject.toml`, requirements files, lockfiles, and runtime configuration.
2. Identify the Python, FastAPI, Pydantic, ASGI server, ORM, migration, and deployment versions.
3. Prefer the repository's installed stack and conventions when they remain supported.
4. Verify version-sensitive APIs against the official source linked by the rule.
5. Surface conflicts between current documentation and existing code; do not silently mix versions.
6. Cite the relevant primary sources in the final response for every version-sensitive decision;
   label project-derived or undocumented conventions explicitly.

Examples target Python 3.11+, FastAPI 0.139.x, and Pydantic 2. Apply SQLAlchemy, Alembic, or
deployment-specific rules only when the project uses those tools.

## Rule Categories

| Priority | Category             | Impact      | Prefix            |
| -------- | -------------------- | ----------- | ----------------- |
| 1        | Architecture         | CRITICAL    | `arch-`           |
| 2        | Python Design        | CRITICAL    | `python-`         |
| 3        | Dependency Injection | CRITICAL    | `di-`             |
| 4        | Error Handling       | HIGH        | `error-`          |
| 5        | Security             | HIGH        | `security-`       |
| 6        | Async & Performance  | HIGH        | `async-`, `perf-` |
| 7        | Database             | MEDIUM-HIGH | `db-`             |
| 8        | API Design           | MEDIUM      | `api-`            |
| 9        | Operations           | MEDIUM      | `ops-`            |

## Quick Reference

### Architecture

- `arch-feature-packages-and-routers` - Compose larger applications from feature routers.
- `arch-keep-path-operations-thin` - Keep transport handlers focused on HTTP concerns.
- `arch-avoid-circular-imports` - Keep dependency direction acyclic and imports predictable.
- `arch-use-lifespan-for-resources` - Own process resources with the FastAPI lifespan.

### Python Design

- `python-type-public-boundaries` - Type public functions and application boundaries.
- `python-use-protocols-for-ports` - Express narrow structural contracts with protocols.
- `python-avoid-mutable-defaults` - Never share mutable default argument state.
- `python-use-context-managers` - Make resource acquisition and cleanup lexical.

### Dependency Injection

- `di-use-request-scoped-unit-of-work` - Commit one shared Unit of Work at the request boundary.
- `di-use-yield-for-cleanup` - Use generator dependencies for request-scoped cleanup.
- `di-understand-cache-and-scope` - Choose dependency cache and teardown scope deliberately.

### Error Handling

- `error-raise-not-return` - Raise HTTP exceptions directly from FastAPI-specific services.
- `error-centralize-exception-handlers` - Map domain, validation, and unexpected errors globally.
- `error-catch-narrow-and-chain` - Catch expected failures narrowly and preserve causes.
- `error-supervise-background-failures` - Observe and handle every background failure.

### Security

- `security-validate-all-input` - Validate every untrusted request boundary.
- `security-filter-response-data` - Filter output through declared response models.
- `security-centralize-authorization` - Enforce authentication and authorization in dependencies.
- `security-hash-passwords-and-verify-jwts` - Use modern password hashing and strict JWT validation.
- `security-restrict-cors-and-hosts` - Allow only intended browser origins and host headers.

### Async & Performance

- `async-match-def-to-workload` - Match `def` or `async def` to the called libraries.
- `async-avoid-blocking-event-loop` - Keep blocking work out of async path operations.
- `async-use-structured-concurrency` - Supervise related tasks as one lifetime.
- `async-bound-timeouts-and-cancellation` - Bound waits and preserve cancellation.
- `perf-offload-heavy-background-work` - Move durable or CPU-heavy work outside requests.

### Database

- `db-scope-sessions-and-transactions` - Keep one session and transaction owner per unit of work.
- `db-avoid-n-plus-one-and-implicit-io` - Load required relationships explicitly.
- `db-use-migrations` - Version production schema changes with migrations.

### API Design

- `api-separate-input-output-models` - Use distinct command and response schemas.
- `api-declare-status-and-error-contracts` - Document success and failure responses.
- `api-version-with-router-prefixes` - Isolate breaking API versions with routers.

### Operations

- `ops-validate-settings-at-startup` - Parse and validate configuration before serving.
- `ops-use-structured-logging` - Emit contextual logs through `logging`.
- `ops-handle-graceful-shutdown` - Stop intake and release resources cleanly.
- `ops-size-worker-model` - Choose worker count from deployment topology and measurements.
- `ops-provide-liveness-and-readiness` - Separate process health from traffic readiness.

## Load Rules Progressively

Read `references/_sections.md` to choose a category, then load only the rule files relevant to the
task. Each rule contains the rationale, incorrect and correct examples, compatibility notes, and
primary sources. When a source does not cover a project-specific convention, label the convention
as repository-derived instead of presenting it as framework policy.

For Python, pytest, or FastAPI testing work, use the sibling `python-testing-best-practices` skill.
