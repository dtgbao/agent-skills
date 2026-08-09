---
title: Await Async Behavior
impact: HIGH
impactDescription: prevents false positives and timing-dependent assertions
tags: testing, vitest, async, testing-library, component-testing
---

## Await Async Behavior

Await every promise, user interaction, and retrying assertion that contributes to the result. Assert
the final observable state instead of sleeping for an assumed duration.

**Incorrect (the test finishes before the assertion):**

```ts
test("rejects an invalid order", () => {
  expect(createOrder({ quantity: 0 })).rejects.toThrow("quantity");
});
```

**Correct (Vitest observes the rejection):**

```ts
test("rejects an invalid order", async () => {
  await expect(createOrder({ quantity: 0 })).rejects.toThrow("quantity");
});
```

For component tests, use query semantics that match the behavior. This example uses React, but the
query and interaction rules apply across DOM component frameworks:

```tsx
test("shows the saved order", async () => {
  const user = userEvent.setup();
  render(<OrderForm />);

  await user.click(screen.getByRole("button", { name: "Save order" }));

  expect(await screen.findByRole("status")).toHaveTextContent("Order saved");
});
```

- Use `getBy*` for elements that must exist now.
- Use `findBy*` for one element that appears asynchronously.
- Use `waitFor` for an assertion that must be retried, not as a generic delay.
- Use `expect.hasAssertions()` or `expect.assertions(n)` when assertions run inside callbacks,
  conditions, or loops and could otherwise be skipped.
- Increase a timeout only for a known slow boundary. First investigate a missing await, unresolved
  promise, or accidental real request.

## Sources

- [Vitest testing asynchronous code](https://vitest.dev/guide/learn/async)
- [Vitest async assertions](https://vitest.dev/api/expect#resolves)
- [Testing Library async methods](https://testing-library.com/docs/dom-testing-library/api-async)
- [Testing Library query types](https://testing-library.com/docs/queries/about/)
