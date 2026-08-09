---
title: Test Boundary Behavior
impact: MEDIUM
impactDescription: catches regressions without broad mocks or brittle internals
tags: testing, vitest, msw, testing-library, component-testing
---

## Test Boundary Behavior

- Write tests against observable behavior at the smallest useful boundary.
- Use the real router when route matching, navigation, loaders, or URL state are behavior under test.
- Use MSW when request and response behavior matters; mock the API client only when emitted intent is
  the complete contract under test.
- Use local mocks for hard boundaries such as animation, browser APIs, clocks, or third-party SDKs.
- Keep shared helper tests direct: context helpers test provider contracts, gateway contract tests can
  assert constructed `Request` details, and page tests assert user-visible behavior.

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

Do not mock an entire UI library or assert that an internal controller hook ran. Those tests can pass
while the user-visible behavior is broken.

Read `setup-vitest.md` for test environment setup and `setup-msw-api.md` for network setup.

## Sources

- [Testing Library guiding principles](https://testing-library.com/docs/guiding-principles)
- [Testing Library query priority](https://testing-library.com/docs/queries/about/#priority)
- [MSW guidance against request assertions](https://mswjs.io/docs/best-practices/avoid-request-assertions)
