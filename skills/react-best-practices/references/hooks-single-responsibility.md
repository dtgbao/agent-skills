---
title: Keep Custom Hooks Focused
impact: HIGH
impactDescription: separates cohesive stateful behavior from presentation without creating monolithic hooks
tags: hooks, state, architecture, composition
---

## Keep Custom Hooks Focused

Extract stateful behavior from UI when it forms a cohesive workflow or domain
concept. Keep markup, styling, accessibility, and one-off visual state in the
component. Move calculations, validation, parsing, and API clients that do not
use React into plain functions.

A custom hook should have one clear responsibility. Do not turn a component
into one large hook that owns every concern except JSX.

**Incorrect:**

```tsx
function useCheckoutPage() {
	// Cart items and totals
	// Shipping form and validation
	// Coupon application
	// Payment submission
	// Analytics, navigation, and modal state
}
```

**Correct:**

```tsx
function useCheckout() {
	const cart = useCart();
	const shipping = useShippingAddress();
	const coupon = useCoupon();
	const payment = useCheckoutPayment({
		items: cart.items,
		address: shipping.address,
		discount: coupon.discount,
	});

	return { cart, shipping, coupon, payment };
}
```

The feature-level hook is a thin orchestrator: it composes focused hooks and
passes only the dependencies needed between them. It should not reimplement
their state transitions or domain rules.

Split a hook when it returns unrelated values, contains independent workflows,
or requires unrelated setup in tests. Do not split by state-variable count:
values that change together as one behavior, such as the fields and validation
of a registration form, belong in one hook.

Prefer this responsibility boundary:

- Component: presentation, accessibility, and local visual state.
- Custom hook: related React state, transitions, and side-effect coordination.
- Plain function or service: framework-independent domain logic and I/O.
