---
name: python-testing-best-practices
description: Source-verified Python testing practices for pytest, mocks, retries, controlled state, property tests, database integration, and FastAPI applications. Use when writing, reviewing, configuring, or stabilizing Python test suites.
---

# Python Testing Best Practices

Apply 12 focused rules across general Python testing and FastAPI-specific application testing.
Prefer observable behavior, controlled state, explicit teardown, and the narrowest useful test level.

## Start With the Project

Before selecting a rule or writing tests:

1. Read `pyproject.toml`, pytest configuration, dependency files, and the existing test tree.
2. Detect the supported Python, pytest, AnyIO, HTTPX, FastAPI, ORM, and optional testing-tool versions.
3. Preserve the repository's test organization, marker taxonomy, commands, and coverage policy when
   they remain valid.
4. Apply Freezegun, Hypothesis, pytest-cov, SQLAlchemy, or FastAPI rules only when the project uses
   that tool or explicitly requests it.
5. Verify version-sensitive APIs against the primary documentation linked by each rule.

## Rule Categories

| Priority | Category                  | Impact      | Prefix     |
| -------- | ------------------------- | ----------- | ---------- |
| 1        | Organization & Behavior   | HIGH        | `test-`    |
| 2        | Fixtures & Isolation      | HIGH        | `test-`    |
| 3        | FastAPI Application Tests | HIGH        | `fastapi-` |
| 4        | Advanced Techniques       | MEDIUM-HIGH | `test-`    |
| 5        | Configuration & CI        | MEDIUM      | `test-`    |

## Quick Reference

### Organization & Behavior

- `test-organize-suites-and-name-behaviors` - Organize tests by level and name observable behavior.
- `test-use-fixtures-and-parametrization` - Own setup with fixtures and table-drive equivalent cases.

### Fixtures & Isolation

- `test-mock-boundaries-and-retries` - Mock hard boundaries and prove retry policies completely.
- `test-control-time-environment-and-files` - Control clocks, environment, and filesystem state.

### FastAPI Application Tests

- `fastapi-use-testclient-for-sync` - Test synchronous API behavior with `TestClient`.
- `fastapi-use-asgi-transport-for-async` - Use HTTPX `ASGITransport` in async tests.
- `fastapi-override-and-reset-dependencies` - Override dependencies without leaking test state.
- `fastapi-run-lifespan-and-isolate-io` - Exercise lifespan and replace external I/O.

### Advanced Techniques

- `test-register-markers-and-enforce-coverage` - Register suite markers and enforce owned coverage gates.
- `test-use-property-based-testing` - Generate and shrink invariant-breaking inputs conditionally.
- `test-isolate-database-integration` - Test the production database engine in isolated transactions.

### Configuration & CI

- `test-configure-pytest-and-ci` - Keep pytest discovery strict and hand verified commands to CI.

## Load Rules Progressively

Read `references/_sections.md` to choose a category, then load only the rule files relevant to the
task. Each rule contains the rationale, incorrect and correct examples, compatibility notes, and
primary sources. Use `fastapi-` rules only when the application uses FastAPI. Route behavior-first
implementation to `test-driven-development` and workflow mechanics to `ci-cd-and-automation`.
