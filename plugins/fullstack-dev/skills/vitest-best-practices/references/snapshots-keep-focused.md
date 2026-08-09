---
title: Keep Snapshots Focused and Reviewable
impact: LOW-MEDIUM
impactDescription: protects stable output contracts without hiding behavior in noisy diffs
tags: testing, vitest, snapshots, assertions
---

## Keep Snapshots Focused and Reviewable

Snapshot a stable, meaningful output contract when enumerating every field would be tedious. Prefer
direct assertions when only a few properties or user-visible outcomes matter.

**Incorrect (a broad DOM snapshot with unclear intent):**

```tsx
const { container } = render(<CheckoutPage />);
expect(container).toMatchSnapshot();
```

**Correct (a focused structured contract):**

```ts
expect(formatOrder(order)).toMatchInlineSnapshot(
  {
    createdAt: expect.any(String),
    id: expect.any(String),
  },
  `
    {
      "createdAt": Any<String>,
      "id": Any<String>,
      "status": "pending",
      "total": "$42.00",
    }
  `,
);
```

Use inline snapshots for small outputs that are easier to understand beside the test. Commit external
snapshot files with the test and review snapshot updates like production code. Never accept updates
blindly with `-u`; confirm each changed value represents intended behavior.

For concurrent snapshot tests, use the `expect` bound to the test context so Vitest associates the
snapshot with the correct test.

## Sources

- [Vitest snapshot testing](https://vitest.dev/guide/learn/snapshots.html)
- [Vitest snapshot API and concurrent tests](https://vitest.dev/guide/snapshot.html)
