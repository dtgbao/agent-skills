---
title: Minimize Mock Boundaries
impact: HIGH
impactDescription: preserves meaningful behavior while keeping tests controllable
tags: testing, vitest, mocking, modules, boundaries
---

## Minimize Mock Boundaries

Mock the narrowest hard boundary that makes the behavior deterministic: network, clock, browser
API, filesystem, or third-party SDK. Keep domain logic, state transitions, and component composition
real whenever practical.

**Incorrect (replacing the behavior under test):**

```ts
vi.mock(import("./checkout-controller"), () => ({
  useCheckoutController: () => ({ submit: vi.fn(), status: "success" }),
}));

expect(screen.getByText("Order complete")).toBeInTheDocument();
```

**Correct (mocking one external boundary):**

```ts
const { sendOrder } = vi.hoisted(() => ({
  sendOrder: vi.fn(),
}));

vi.mock(import("./order-gateway"), async (importOriginal) => ({
  ...(await importOriginal()),
  sendOrder,
}));

test("shows completion after submitting", async () => {
  sendOrder.mockResolvedValue({ id: "order-1" });

  const user = userEvent.setup();
  render(<Checkout />);
  await user.click(screen.getByRole("button", { name: "Place order" }));

  expect(await screen.findByText("Order complete")).toBeInTheDocument();
});
```

Use typed dynamic imports in `vi.mock(import("..."))` so TypeScript validates the path and factory.
Use `vi.hoisted` only for values referenced by a hoisted mock factory. Prefer a spy when the real
implementation should remain active and the execution environment supports spying on that export.

Vitest cannot replace a function's internal call to another function in the same module. Split the
hard boundary into another module or inject the dependency instead of adding a test-runner
workaround. Browser Mode uses native ESM and has different spying constraints; verify the installed
Vitest version before choosing its mocking API.

## Sources

- [Vitest module mocking](https://vitest.dev/guide/mocking/modules.html)
- [Vitest mocking guide](https://vitest.dev/guide/mocking.html)
