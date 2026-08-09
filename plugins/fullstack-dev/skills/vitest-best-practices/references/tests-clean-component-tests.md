---
title: Write Clean Component Tests
impact: MEDIUM
impactDescription: keeps tests scoped, behavior-focused, and resilient to harmless UI changes
tags: testing, vitest, component-testing, testing-library, user-event
---

## Write Clean Component Tests

The examples use React, but the rules apply to Vue, Svelte, and other component frameworks. Replace
the renderer, router, and component syntax with the project's equivalents.

**Incorrect:**

```tsx
beforeEach(() => {
	// Page-specific setup leaks into every test in this file.
});

describe("ProductPage", () => {
	it("navigates when the product name is clicked", async () => {
		render(<ProductPage />);

		expect(document.querySelector(".heading")).toHaveTextContent("Product Title");

		await user.click(screen.getByRole("link", { name: "Product Name 1" }));

		expect(mockNavigate).toHaveBeenCalledWith("/products/1");
	});
});
```

**Correct:**

```tsx
const { mockNavigate } = vi.hoisted(() => ({
	mockNavigate: vi.fn(),
}));

vi.mock(import("react-router-dom"), async (importOriginal) => {
	const original = await importOriginal();

	return {
		...original,
		useNavigate: () => mockNavigate,
	};
});

describe("ProductPage", () => {
	beforeEach(() => {
		mockNavigate.mockClear();
	});

	const renderProductPage = () => {
		const user = userEvent.setup();
		const renderHelpers = renderPage("/products");

		const addToCart = async () => {
			const button = await screen.findByRole("button", {
				name: /add to cart/i,
			});
			await user.click(button);
			return button;
		};

		return {
			...renderHelpers,
			user,
			addToCart,
		};
	};

	it("navigates when the product name is clicked", async () => {
		const { user } = renderProductPage();

		expect(await screen.findByRole("heading", { name: "Product Title" })).toBeInTheDocument();

		await user.click(screen.getByRole("link", { name: /^product name 1$/i }));

		expect(mockNavigate).toHaveBeenCalledWith("/products/1");
	});

	it('should show "Added To Cart" dialog when clicking on "Add To Cart" button', async () => {
		const { addToCart } = renderProductPage();

		expect(await screen.findByRole("heading", { name: "Product Title" })).toBeInTheDocument();
		await addToCart();

		expect(await screen.findByRole("dialog", { name: /^added to cart$/i })).toBeInTheDocument();
	});
});
```

Rules:

- Keep page or component setup inside the matching `describe` block.
- Use `vi.hoisted` only for values referenced by a hoisted `vi.mock` factory. Prefer typed dynamic
  import syntax so TypeScript validates the module path and factory shape.
- Put `beforeEach` inside `describe` unless the setup is truly file-wide.
- Put page-specific render helpers inside `describe`. Call `userEvent.setup()` before rendering, then
  return `user`, render helpers, and repeated user actions.
- Keep hard-boundary mocks local to the test file. Avoid global UI library mocks in setup files.
- Use `screen` queries instead of `document` selectors. Prefer roles, labels, and accessible names.
- Use exact strings when the text is the behavior under test. Use case-insensitive regex for copy that can change harmlessly.
- Use `userEvent.setup()` and test the behavior a user performs. Avoid asserting component internals.
- Mock one boundary when the test is about emitted intent. Use the real router or API mocks when route rendering or data loading is the behavior.

## Sources

- [Testing Library query priority](https://testing-library.com/docs/queries/about/#priority)
- [Testing Library user-event setup](https://testing-library.com/docs/user-event/intro/#writing-tests-with-userevent)
- [Vitest module mocking](https://vitest.dev/guide/mocking/modules.html)
- [Vitest mock hoisting](https://vitest.dev/guide/mocking.html)
