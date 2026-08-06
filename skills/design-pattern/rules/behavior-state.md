---
title: Use State for State-Dependent Behavior
impact: HIGH
impactDescription: "Popularity: 2/3; Complexity: 1/3"
tags: behavioral, state, transitions
---

## Use State for State-Dependent Behavior

Use State when behavior changes with internal state and large conditionals obscure transitions.

**Incorrect (conditionals spread across methods):**

```typescript
if (order.status === "paid") refund();
else if (order.status === "draft") cancel();
```

**Correct (delegate to the current state):**

```typescript
interface OrderState {
  cancel(order: Order): void;
}
class PaidState implements OrderState {
  cancel(order: Order) {
    order.transition(new RefundState());
  }
}
class Order {
  constructor(private state: OrderState) {}
  cancel() {
    this.state.cancel(this);
  }
  transition(s: OrderState) {
    this.state = s;
  }
}
```

**Tradeoff:** Localizes transitions but creates more types; use a discriminated union for a small stable machine.

References: [main article](https://refactoring.guru/design-patterns/state), [TypeScript example](https://refactoring.guru/design-patterns/state/typescript/example)
