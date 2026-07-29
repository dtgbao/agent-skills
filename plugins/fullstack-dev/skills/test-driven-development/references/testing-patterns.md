# Testing Patterns Reference (JavaScript/TypeScript)

Quick reference of JavaScript/TypeScript testing patterns — Jest, React Testing Library, Supertest, and Playwright — illustrating the universal principles from the [`test-driven-development`](../SKILL.md) skill. The principles (Arrange-Act-Assert, naming, mock discipline, anti-patterns) apply in any ecosystem; the syntax and tooling shown here are JS/TS-specific. In another stack, follow the same principles with the repository's own test framework and commands.

## Table of Contents

- [Good Tests](#good-tests)
- [Bad Tests](#bad-tests)
- [Test Structure (Arrange-Act-Assert)](#test-structure-arrange-act-assert)
- [Test Naming Conventions](#test-naming-conventions)
- [Common Assertions](#common-assertions)
- [Mocking Patterns](#mocking-patterns)
- [React/Component Testing](#reactcomponent-testing)
- [API / Integration Testing](#api--integration-testing)
- [E2E Testing (Playwright)](#e2e-testing-playwright)
- [Test Anti-Patterns](#test-anti-patterns)

## Good Tests

**Integration-style**: Test through real interfaces, not mocks of internal parts.

```typescript
// GOOD: Tests observable behavior
test("user can checkout with valid cart", async () => {
	const cart = createCart();
	cart.add(product);
	const result = await checkout(cart, paymentMethod);
	expect(result.status).toBe("confirmed");
});
```

Characteristics:

- Tests behavior users/callers care about
- Uses public API only
- Survives internal refactors
- Describes WHAT, not HOW
- One logical assertion per test

## Bad Tests

**Implementation-detail tests**: Coupled to internal structure.

```typescript
// BAD: Tests implementation details
test("checkout calls paymentService.process", async () => {
	const mockPayment = jest.mock(paymentService);
	await checkout(cart, payment);
	expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

Red flags:

- Mocking internal collaborators
- Testing private methods
- Asserting on call counts/order
- Test breaks when refactoring without behavior change
- Test name describes HOW not WHAT
- Verifying through external means instead of interface

```typescript
// BAD: Bypasses interface to verify
test("createUser saves to database", async () => {
	await createUser({ name: "Alice" });
	const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
	expect(row).toBeDefined();
});

// GOOD: Verifies through interface
test("createUser makes user retrievable", async () => {
	const user = await createUser({ name: "Alice" });
	const retrieved = await getUser(user.id);
	expect(retrieved.name).toBe("Alice");
});
```

**Tautological tests**: Expected value restates the implementation, so the test passes by construction.

```typescript
// BAD: Expected value is recomputed the way the code computes it
test("calculateTotal sums line items", () => {
	const items = [{ price: 10 }, { price: 5 }];
	const expected = items.reduce((sum, i) => sum + i.price, 0);
	expect(calculateTotal(items)).toBe(expected);
});

// GOOD: Expected value is an independent, known literal
test("calculateTotal sums line items", () => {
	expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
```

## Test Structure (Arrange-Act-Assert)

```typescript
it("describes expected behavior", () => {
	// Arrange: Set up test data and preconditions
	const input = { title: "Test Task", priority: "high" };

	// Act: Perform the action being tested
	const result = createTask(input);

	// Assert: Verify the outcome
	expect(result.title).toBe("Test Task");
	expect(result.priority).toBe("high");
	expect(result.status).toBe("pending");
});
```

## Test Naming Conventions

```typescript
// Pattern: [unit] [expected behavior] [condition]
describe("TaskService.createTask", () => {
	it("creates a task with default pending status", () => {});
	it("throws ValidationError when title is empty", () => {});
	it("trims whitespace from title", () => {});
	it("generates a unique ID for each task", () => {});
});
```

## Common Assertions

```typescript
// Equality
expect(result).toBe(expected); // Strict equality (===)
expect(result).toEqual(expected); // Deep equality (objects/arrays)
expect(result).toStrictEqual(expected); // Deep equality + type matching

// Truthiness
expect(result).toBeTruthy();
expect(result).toBeFalsy();
expect(result).toBeNull();
expect(result).toBeDefined();
expect(result).toBeUndefined();

// Numbers
expect(result).toBeGreaterThan(5);
expect(result).toBeLessThanOrEqual(10);
expect(result).toBeCloseTo(0.3, 5); // Floating point

// Strings
expect(result).toMatch(/pattern/);
expect(result).toContain("substring");

// Arrays / Objects
expect(array).toContain(item);
expect(array).toHaveLength(3);
expect(object).toHaveProperty("key", "value");

// Errors
expect(() => fn()).toThrow();
expect(() => fn()).toThrow(ValidationError);
expect(() => fn()).toThrow("specific message");

// Async
await expect(asyncFn()).resolves.toBe(value);
await expect(asyncFn()).rejects.toThrow(Error);
```

## Mocking Patterns

### When to Mock

Mock at **system boundaries** only:

- External APIs (payment, email, etc.)
- Databases (sometimes - prefer test DB)
- Time/randomness
- File system (sometimes)

Don't mock:

- Your own classes/modules
- Internal collaborators
- Anything you control

### Designing for Mockability

At system boundaries, design interfaces that are easy to mock:

**1. Use dependency injection**

Pass external dependencies in rather than creating them internally:

```typescript
// Easy to mock
function processPayment(order, paymentClient) {
	return paymentClient.charge(order.total);
}

// Hard to mock
function processPayment(order) {
	const client = new StripeClient(process.env.STRIPE_KEY);
	return client.charge(order.total);
}
```

**2. Prefer SDK-style interfaces over generic fetchers**

Create specific functions for each external operation instead of one generic function with conditional logic:

```typescript
// GOOD: Each function is independently mockable
const api = {
	getUser: (id) => fetch(`/users/${id}`),
	getOrders: (userId) => fetch(`/users/${userId}/orders`),
	createOrder: (data) => fetch("/orders", { method: "POST", body: data }),
};

// BAD: Mocking requires conditional logic inside the mock
const api = {
	fetch: (endpoint, options) => fetch(endpoint, options),
};
```

The SDK approach means:

- Each mock returns one specific shape
- No conditional logic in test setup
- Easier to see which endpoints a test exercises
- Type safety per endpoint

### Mock Functions

```typescript
const mockFn = jest.fn();
mockFn.mockReturnValue(42);
mockFn.mockResolvedValue({ data: "test" });
mockFn.mockImplementation((x) => x * 2);

expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledWith("arg1", "arg2");
expect(mockFn).toHaveBeenCalledTimes(3);
```

### Mock Modules

```typescript
// Mock an entire module
jest.mock("./database", () => ({
	query: jest.fn().mockResolvedValue([{ id: 1, title: "Test" }]),
}));

// Mock specific exports
jest.mock("./utils", () => ({
	...jest.requireActual("./utils"),
	generateId: jest.fn().mockReturnValue("test-id"),
}));
```

## React/Component Testing

```tsx
import { render, screen, fireEvent, waitFor } from "@testing-library/react";

describe("TaskForm", () => {
	it("submits the form with entered data", async () => {
		const onSubmit = jest.fn();
		render(<TaskForm onSubmit={onSubmit} />);

		// Find elements by accessible role/label (not test IDs)
		await screen.findByRole("textbox", { name: /title/i });
		fireEvent.change(screen.getByRole("textbox", { name: /title/i }), {
			target: { value: "New Task" },
		});
		fireEvent.click(screen.getByRole("button", { name: /create/i }));

		await waitFor(() => {
			expect(onSubmit).toHaveBeenCalledWith({ title: "New Task" });
		});
	});

	it("shows validation error for empty title", async () => {
		render(<TaskForm onSubmit={jest.fn()} />);

		fireEvent.click(screen.getByRole("button", { name: /create/i }));

		expect(await screen.findByText(/title is required/i)).toBeInTheDocument();
	});
});
```

## API / Integration Testing

```typescript
import request from "supertest";
import { app } from "../src/app";

describe("POST /api/tasks", () => {
	it("creates a task and returns 201", async () => {
		const response = await request(app)
			.post("/api/tasks")
			.send({ title: "Test Task" })
			.set("Authorization", `Bearer ${testToken}`)
			.expect(201);

		expect(response.body).toMatchObject({
			id: expect.any(String),
			title: "Test Task",
			status: "pending",
		});
	});

	it("returns 422 for invalid input", async () => {
		const response = await request(app)
			.post("/api/tasks")
			.send({ title: "" })
			.set("Authorization", `Bearer ${testToken}`)
			.expect(422);

		expect(response.body.error.code).toBe("VALIDATION_ERROR");
	});

	it("returns 401 without authentication", async () => {
		await request(app).post("/api/tasks").send({ title: "Test" }).expect(401);
	});
});
```

## E2E Testing (Playwright)

```typescript
import { test, expect } from "@playwright/test";

test("user can create and complete a task", async ({ page }) => {
	// Navigate and authenticate
	await page.goto("/");
	await page.getByRole("textbox", { name: /email/i }).fill("test@example.com");
	await page.getByLabel(/password/i).fill("testpass123");
	await page.getByRole("button", { name: /log in/i }).click();

	// Create a task
	await page.getByRole("button", { name: /new task/i }).click();
	await page.getByRole("textbox", { name: /title/i }).fill("Buy groceries");
	await page.getByRole("button", { name: /create/i }).click();

	// Verify task appears
	const task = page.getByRole("listitem", { name: /buy groceries/i });
	await expect(task).toBeVisible();

	// Complete the task
	await task.getByRole("checkbox", { name: /complete buy groceries/i }).check();
	await expect(task).toHaveCSS("text-decoration-line", "line-through");
});
```

## Test Anti-Patterns

| Anti-Pattern                   | Problem                        | Better Approach            |
| ------------------------------ | ------------------------------ | -------------------------- |
| Testing implementation details | Breaks on refactor             | Test inputs/outputs        |
| Snapshot everything            | No one reviews snapshot diffs  | Assert specific values     |
| Shared mutable state           | Tests pollute each other       | Setup/teardown per test    |
| Testing third-party code       | Wastes time, not your bug      | Mock the boundary          |
| Skipping tests to pass CI      | Hides real bugs                | Fix or delete the test     |
| Using `test.skip` permanently  | Dead code                      | Remove or fix it           |
| Overly broad assertions        | Doesn't catch regressions      | Be specific                |
| No async error handling        | Swallowed errors, false passes | Always `await` async tests |
