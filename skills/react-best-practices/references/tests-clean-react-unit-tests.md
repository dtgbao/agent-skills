---
title: Write Clean React Unit Tests
impact: MEDIUM
impactDescription: keeps tests scoped, behavior-focused, and resilient to harmless UI changes
tags: testing, vitest, react-testing-library, user-event
---

## Write Clean React Unit Tests

Keep page or component setup inside the matching `describe` block. Use
module-level `vi.hoisted` mocks only when Vitest needs the mock before imports
run.

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
const mockNavigate = vi.hoisted(() => vi.fn());

vi.mock("react-router-dom", async () => ({
  ...(await vi.importActual<typeof import("react-router-dom")>("react-router-dom")),
  useNavigate: () => mockNavigate,
}));

describe("ProductPage", () => {
  beforeEach(() => {
    mockNavigate.mockClear();

    return () => {
      // Page-specific cleanup, if this page needs it.
    };
  });

  const renderProductPage = () => {
    const user = userEvent.setup();
    const renderHelpers = renderPage("/");

    const addToCart = async () => {
      const button = await screen.findByRole("button", { name: /add to cart/i });
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
});
```

Rules:

- Put `beforeEach` inside `describe` unless the setup is truly file-wide.
- Put page-specific render helpers inside `describe`; return `user`, render
  helpers, and repeated user actions.
- Use `screen` queries instead of `document` selectors. Prefer roles, labels,
  and accessible names.
- Use exact strings when the text is the behavior under test. Use case-insensitive
  regex for copy that can change harmlessly.
- Use `userEvent.setup()` and test the behavior a user performs. Avoid asserting
  component internals.
- Mock one boundary when the test is about emitted intent. Use the real router or
  API mocks when route rendering or data loading is the behavior.
