---
title: Measure Coverage Without Chasing Percentages
impact: LOW-MEDIUM
impactDescription: exposes untested source without rewarding low-value assertions
tags: testing, vitest, coverage, ci
---

## Measure Coverage Without Chasing Percentages

Include relevant source files so never-imported files appear in the report. Use coverage to find
missing behavior, then set thresholds from the project's risk, baseline, and agreed ratchet policy.

**Incorrect (a universal target disconnected from risk):**

```ts
coverage: {
  thresholds: {
    lines: 100,
    branches: 100,
    functions: 100,
    statements: 100,
  },
},
```

**Correct (measure all relevant source first):**

```ts
coverage: {
  provider: "v8",
  include: ["src/**/*.{js,jsx,ts,tsx,vue,svelte}"],
  exclude: ["src/**/*.d.ts", "src/**/generated/**"],
  reporter: ["text", "html"],
},
```

Add thresholds only after the team chooses a baseline and enforcement policy. Prefer higher scrutiny
for authorization, money movement, data integrity, and complex branching over tests written solely
to increase a global number. Exclude generated or declarative files only for a documented reason.

Use V8 as the default provider on supported runtimes. Select Istanbul when runtime compatibility or
measured project behavior requires it.

## Sources

- [Vitest coverage providers](https://vitest.dev/guide/coverage.html#coverage-providers)
- [Vitest including and excluding files](https://vitest.dev/guide/coverage.html#including-and-excluding-files-from-coverage-report)
