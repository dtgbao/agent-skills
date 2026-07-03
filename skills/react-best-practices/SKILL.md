---
name: react-best-practices
description: React architecture reference. Use when implementing, refactoring, or reviewing React TypeScript code that touches component composition, feature/shared boundaries, scoped state/providers, API/data hooks, React 19 refs/context, unit tests, or behavior-focused tests.
---

# React Best Practices

Reusable React rules for modern TypeScript apps. Treat existing app patterns as context: keep them when they align with these rules, and use the smallest corrective change when they do not.

## Routing

Read only the rows that match the current change. Read helper source only when
copying or adapting that helper.

Use impact to prioritize conflicts: `CRITICAL` blocks architecture drift, `HIGH`
affects architecture or data flow, `MEDIUM` affects maintainability or test
quality, and `LOW` is incremental.

| Branch                                          | Impact   | Reference                                                   |
| ----------------------------------------------- | -------- | ----------------------------------------------------------- |
| Boolean or mode props                           | CRITICAL | `references/architecture-avoid-boolean-props.md`            |
| Shared UI surface composition                   | CRITICAL | `references/composition-compound-components.md`             |
| Render props for static slots                   | CRITICAL | `references/patterns-children-over-render-props.md`         |
| Feature/shared placement                        | HIGH     | `references/boundaries-feature-shared-split.md`             |
| Provider scope or state ownership               | HIGH     | `references/state-scope-providers-to-owners.md`             |
| API functions, loaders, query hooks             | HIGH     | `references/data-plain-api-functions.md`                    |
| Reused gestures, keyboard behavior, motion glue | HIGH     | `references/composition-shared-interaction-primitives.md`   |
| React 19 refs or context reads                  | MEDIUM   | `references/react19-no-forwardref.md`                       |
| Unit test setup or API mocks                    | MEDIUM   | `references/setup-vitest.md`, `references/setup-msw-api.md` |
| Clean React unit tests                          | MEDIUM   | `references/tests-clean-react-unit-tests.md`                |
| Behavior-focused tests                          | MEDIUM   | `references/tests-boundary-behavior.md`                     |
