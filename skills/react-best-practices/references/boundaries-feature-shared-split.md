---
title: Keep Feature Code and Shared Primitives Separate
impact: HIGH
impactDescription: keeps imports predictable and prevents shared from becoming a junk drawer
tags: boundaries, modules, shared, tests
---

## Keep Feature Code and Shared Primitives Separate

Keep product-specific code in a feature folder. Move code to `shared`, `common`,
or `ui` only when it is reusable outside that feature: HTTP clients, route
fallbacks, storage-key helpers, context helpers, and generic UI primitives.

**Incorrect:**

```tsx
// src/shared/components/OrderSummaryCard.tsx
export function OrderSummaryCard({ order, onPay }: Props) {
  return <Card>{order.total}</Card>;
}
```

**Correct:**

```tsx
// src/modules/orders/components/OrderSummaryCard.tsx
export function OrderSummaryCard({ order, children }: OrderSummaryCardProps) {
  return <OrderSummaryContext value={{ order }}>{children}</OrderSummaryContext>;
}

// src/shared/components/InteractiveCard.tsx
export function InteractiveCard({ children, onPress }: InteractiveCardProps) {
  return <button onClick={onPress}>{children}</button>;
}
```

Tests should mirror the same boundary: feature tests for feature behavior,
shared tests for reusable utilities and primitives, and app tests for app
wiring.
