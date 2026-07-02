---
title: Test Boundary Behavior
impact: MEDIUM
impactDescription: catches regressions without broad mocks or brittle internals
tags: testing, vitest, msw, react-testing-library
---

## Test Boundary Behavior

Write tests against observable behavior at the smallest useful boundary. Use the
real router and network mocks for pages when routing or data loading matters.
Use local mocks only for focused primitives such as animation or browser APIs.

**Incorrect:**

```ts
vi.mock("@heroui/react", () => fakeEveryComponent);

it("renders checkout", () => {
  render(<CheckoutPage />);
  expect(useCheckoutController).toHaveBeenCalled();
});
```

**Correct:**

```ts
it("keeps the cart item after moving from shipping to payment", async () => {
  const user = userEvent.setup();

  renderPage("/checkout/shipping");
  await user.type(screen.getByLabelText("Address"), "1 Main St");
  await user.click(screen.getByRole("button", { name: "Continue" }));

  expect(await screen.findByRole("heading", { name: "Payment" })).toBeInTheDocument();
  expect(screen.getByText("1 Main St")).toBeInTheDocument();
});
```

Keep shared helper tests direct: context helpers test provider contracts, API
tests assert `Request` details, and page tests assert user-visible behavior.

When testing data-backed pages, set up MSW once in test setup with
`beforeAll(() => server.listen())`, `afterEach(() => server.resetHandlers())`,
and `afterAll(() => server.close())`. Prefer shared render helpers:
`renderWithProviders` for component tests needing app providers and `renderPage`
for router-level tests. Read `references/helper-test-utils.md` only when copying
those helper implementations.

For test environment setup, read `references/setup-vitest.md`. For API mock
server setup, read `references/setup-msw-api.md`.
