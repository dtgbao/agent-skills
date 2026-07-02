# Setup Vitest for React Tests

Use this when adding or checking project-level Vitest setup for React tests.
Keep setup in three places: Vite/Vitest config, `tests/setup.ts`, and
`tsconfig.test.json`.

## `vite.config.ts`

Put test configuration under `test`. In this repo, `vite-plus` reads the same
shape as Vitest:

```ts
test: {
  environment: "jsdom",
  globals: true,
  setupFiles: ["tests/setup.ts"],
  coverage: {
    include: ["src/**/*.{ts,tsx}"],
    thresholds: {
      statements: 80,
      lines: 80,
      functions: 85, // Slightly higher because making sure a function fires at least once is easy
      branches: 80,
    },
  },
},
```

Use `jsdom` for React DOM tests. Keep `globals: true` only when tests and setup
files use global `vi`, `describe`, `it`, or `expect`.

## `tests/setup.ts`

Load DOM matchers and global test fixtures once:

```ts
import "@testing-library/jest-dom/vitest";

import { server } from "@tests/mocks/api";

vi.stubEnv("VITE_PUBLIC_THE_DOG_API_BASE_URL", "https://api.thedogapi.com/v1");
vi.stubEnv("VITE_PUBLIC_THE_DOG_API_KEY", "test-dog-api-key");

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

Put browser polyfills here only when many tests need them. Put one-off mocks in
the test file.

## `tsconfig.test.json`

Extend the app config, include tests and source, and add Vitest globals:

```json
{
  "extends": "./tsconfig.app.json",
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.test.tsbuildinfo",
    "types": ["vite-plus/client", "vitest/globals"]
  },
  "include": ["tests", "src"]
}
```

Add package-specific types only when setup or tests need them globally.
