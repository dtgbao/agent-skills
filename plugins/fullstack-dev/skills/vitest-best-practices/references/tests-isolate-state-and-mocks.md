---
title: Isolate Test State and Mocks
impact: HIGH
impactDescription: prevents order-dependent failures and cross-test leakage
tags: testing, vitest, isolation, mocks, cleanup
---

## Isolate Test State and Mocks

Create mutable fixtures inside each test or `beforeEach`. Restore spies, stubbed globals,
environment variables, and fake timers in the scope that changed them. A test must pass alone, in a
suite, and in a different execution order.

**Incorrect (shared state and leaked runtime changes):**

```ts
const cart = createCart();

test("adds an item", () => {
  vi.stubEnv("CURRENCY", "USD");
  cart.add({ id: "book" });
  expect(cart.size).toBe(1);
});

test("starts empty", () => {
  expect(cart.size).toBe(0);
});
```

**Correct (fresh state and local cleanup):**

```ts
import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";

describe("cart", () => {
  let cart: ReturnType<typeof createCart>;

  beforeEach(() => {
    cart = createCart();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
    vi.useRealTimers();
  });

  test("starts empty", () => {
    expect(cart.size).toBe(0);
  });
});
```

Keep Vitest's file isolation enabled by default. Disable it only after profiling proves startup is a
material bottleneck and the selected files have no module or global side effects.

Do not use `test.concurrent` for tests that mutate shared mocks, globals, environment variables, or
timers. Global cleanup from one concurrent test can alter another test while it is still running.

## Sources

- [Vitest parallelism and isolation](https://vitest.dev/guide/parallelism)
- [Vitest mocking cleanup](https://vitest.dev/guide/mocking.html)
- [Vitest isolation configuration](https://vitest.dev/config/isolate.html)
- [Vitest clear-mocks concurrency warning](https://vitest.dev/config/clearmocks.html)
