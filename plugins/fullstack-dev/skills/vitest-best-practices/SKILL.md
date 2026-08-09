---
name: vitest-best-practices
description: Vitest testing reference for reliable unit, component, and integration tests. Use when configuring or upgrading Vitest, writing or reviewing tests for React, Vue, Svelte, or framework-neutral TypeScript and JavaScript, using Testing Library-style queries, mocking modules, timers, environments, or network requests, defining coverage or snapshot policy, or diagnosing flaky test isolation.
---

# Vitest Best Practices

Apply focused, behavior-oriented testing rules for Vitest, component testing tools, and MSW. Preserve
repository conventions when they align with these rules, and make the smallest change that restores
reliable behavior when they do not.

Examples use React where a concrete UI framework is necessary, but the rules are framework-neutral.
Replace React renderers, routers, component syntax, and helper imports with the project's equivalents
while preserving the behavioral boundary, query, isolation, and cleanup principles.

## Version Check

Before using version-sensitive Vitest APIs, read the project's dependency manifest and lockfile to
identify the installed Vitest major version. Use the matching official documentation. Treat these
references as a Vitest 4.1 baseline and adapt APIs when the project intentionally remains on an older
major version.

## Rule Categories by Priority

| Priority | Category                  | Impact      | Prefix                    |
| -------- | ------------------------- | ----------- | ------------------------- |
| 1        | Correctness and isolation | HIGH        | `tests-`                  |
| 2        | Mocking boundaries        | HIGH        | `mocks-`                  |
| 3        | Async behavior and time   | HIGH-MEDIUM | `tests-`, `timers-`       |
| 4        | Component behavior        | MEDIUM      | `tests-`                  |
| 5        | Environment and setup     | MEDIUM      | `setup-`                  |
| 6        | Coverage and snapshots    | LOW-MEDIUM  | `coverage-`, `snapshots-` |

Use impact to resolve conflicts:

- `HIGH` prevents false positives, cross-test leakage, or tests of implementation details.
- `MEDIUM` improves determinism, realistic behavior, or maintainability.
- `LOW` is incremental and should not displace clearer behavioral assertions.

## Quick Reference

### 1. Correctness and Isolation

- `tests-isolate-state-and-mocks` - Give every test fresh state and restore mutated test runtime state.
- `tests-await-async-behavior` - Await user actions, promises, and retrying assertions.
- `tests-boundary-behavior` - Assert observable behavior at the smallest useful boundary.

### 2. Mocking Boundaries

- `mocks-minimize-boundaries` - Mock only hard boundaries and use typed Vitest module factories.
- `setup-msw-api` - Model network behavior with MSW and reject unknown requests.

### 3. Async Behavior and Time

- `timers-control-time` - Use fake time locally and always restore real timers.

### 4. Component Behavior

- `tests-clean-component-tests` - Use accessible queries and per-test user interactions.

### 5. Environment and Setup

- `setup-vitest` - Keep shared Vitest configuration and setup explicit and minimal.
- `setup-choose-environment` - Use Node by default and opt into DOM or browser execution by need.

### 6. Coverage and Snapshots

- `coverage-measure-behavior` - Include untested source and set thresholds from project risk.
- `snapshots-keep-focused` - Snapshot stable contracts and review every update.

## How to Use

Read only the reference files that match the current testing concern. Each file in `references/`
contains its impact, incorrect and correct examples, tradeoffs, and authoritative sources. Combine
rules when concerns overlap; for example, an async component request test may require the async,
boundary, MSW, and clean component rules.

Do not copy configuration blindly. Reuse the project's existing config location, aliases, render
helpers, and package scripts when they already satisfy the selected rules.
