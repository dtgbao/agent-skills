---
title: Choose the Smallest Test Environment
impact: MEDIUM
impactDescription: avoids unnecessary runtime cost and environment-only false confidence
tags: setup, testing, vitest, jsdom, browser-mode
---

## Choose the Smallest Test Environment

Use Vitest's default Node environment for pure logic and server code. Use `jsdom` for component DOM
tests. Use Browser Mode only when behavior depends on native browser execution rather than an
emulated DOM.

**Incorrect (forcing every test through a DOM emulator):**

```ts
export default defineConfig({
  test: {
    environment: "jsdom",
  },
});
```

**Correct (opt in the files that need a DOM):**

```ts
// @vitest-environment jsdom

import { render, screen } from "@testing-library/react";
```

The example uses React, but the environment decision is the same for Vue, Svelte, and other DOM
component frameworks. When most tests are DOM tests, a project-wide `jsdom` default is reasonable. Split Node, DOM,
and Browser Mode tests into Vitest projects when each group needs materially different plugins,
aliases, setup, or execution environments.

Do not treat `jsdom` or `happy-dom` as proof of browser layout, navigation, rendering, or other APIs
they do not implement faithfully. Use Browser Mode with a CI-capable provider for behavior that
requires a real browser.

## Sources

- [Vitest test environments](https://vitest.dev/guide/environment.html)
- [Vitest test projects](https://vitest.dev/guide/projects.html)
- [Vitest Browser Mode](https://vitest.dev/guide/browser/)
