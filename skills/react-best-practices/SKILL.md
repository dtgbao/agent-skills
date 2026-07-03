---
name: react-best-practices
description: React architecture reference. Use when implementing, refactoring, or reviewing React TypeScript code that touches component composition, feature/shared boundaries, scoped state/providers, API/data hooks, React 19 refs/context, unit tests, or behavior-focused tests.
---

# React Best Practices

Reusable React rules for modern TypeScript apps. Treat existing app patterns as context: keep them when they align with these rules, and use the smallest corrective change when they do not.

## Routing

Read only the rows that match the current change. Read helper source only when
copying or adapting that helper.

| Branch                                          | Reference                                                   |
| ----------------------------------------------- | ----------------------------------------------------------- |
| Feature/shared placement                        | `references/boundaries-feature-shared-split.md`             |
| Boolean or mode props                           | `references/architecture-avoid-boolean-props.md`            |
| Shared UI surface composition                   | `references/composition-compound-components.md`             |
| Provider scope or state ownership               | `references/state-scope-providers-to-owners.md`             |
| API functions, loaders, query hooks             | `references/data-plain-api-functions.md`                    |
| Reused gestures, keyboard behavior, motion glue | `references/composition-shared-interaction-primitives.md`   |
| Render props for static slots                   | `references/patterns-children-over-render-props.md`         |
| React 19 refs or context reads                  | `references/react19-no-forwardref.md`                       |
| Unit test setup or API mocks                    | `references/setup-vitest.md`, `references/setup-msw-api.md` |
| Clean React unit tests                          | `references/tests-clean-react-unit-tests.md`                |
| Behavior-focused tests                          | `references/tests-boundary-behavior.md`                     |
