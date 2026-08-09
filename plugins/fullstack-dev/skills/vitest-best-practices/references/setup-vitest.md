---
title: Setup Vitest for Component Tests
impact: MEDIUM
impactDescription: keeps component test environment setup predictable
tags: setup, testing, vitest
---

# Setup Vitest for Component Tests

Use this when adding or checking project-level Vitest setup for component tests. Preserve the
repository's existing Vite/Vitest config and TypeScript project layout. Add only the settings the
test suite actually needs.

## Vitest Configuration

Put test configuration under `test` in the existing `vite.config.ts` or `vitest.config.ts`:

```ts
test: {
  environment: "jsdom",
  setupFiles: ["tests/setup.ts"],
  coverage: {
    include: ["src/**/*.{js,jsx,ts,tsx,vue,svelte}"],
  },
},
```

Use `jsdom` only for files that need an emulated DOM. Keep Vitest's default explicit imports unless
the repository already uses `globals: true`; when globals are enabled, include `vitest/globals` in
the test TypeScript config. Define coverage thresholds only from an agreed project baseline and risk
policy. See `setup-choose-environment.md` and `coverage-measure-behavior.md` for those decisions.

## `tests/setup.ts`

Load shared matchers and register repeatable hooks:

```ts
import "@testing-library/jest-dom/vitest";
import { afterEach, vi } from "vitest";

afterEach(() => {
  vi.unstubAllEnvs();
  vi.unstubAllGlobals();
});
```

Vitest executes setup files before each test file in the same worker. Keep setup idempotent, put
shared cleanup in hooks, and avoid starting the same heavy process repeatedly. Put one-off mocks,
environment values, and polyfills in the test file that needs them.

## `tsconfig.test.json`

Extend the app config and include tests and source:

```json
{
  "extends": "./tsconfig.app.json",
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.test.tsbuildinfo",
    "types": ["vite/client"]
  },
  "include": ["tests", "src"]
}
```

Add `vitest/globals` only when `globals: true` is enabled. Add other package-specific types only
when setup or tests need them globally.

## Sources

- [Vitest setup files](https://vitest.dev/config/setupfiles.html)
- [Vitest globals](https://vitest.dev/guide/learn/writing-tests.html#using-global-imports)
- [Vitest test environments](https://vitest.dev/guide/environment.html)
- [Vitest coverage](https://vitest.dev/guide/coverage.html)
