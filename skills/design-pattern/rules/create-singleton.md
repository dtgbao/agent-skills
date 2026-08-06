---
title: Use Singleton Only for One Required Instance
impact: HIGH
impactDescription: "Popularity: 2/3; Complexity: 1/3"
tags: creational, singleton, lifecycle
---

## Use Singleton Only for One Required Instance

Use Singleton only when the domain requires exactly one instance and clients need a controlled access point. Prefer dependency injection when available.

**Incorrect (uncontrolled global mutable state):**

```typescript
export const settings: any = {};
```

**Correct (construction is restricted):**

```typescript
class Registry {
  private static value?: Registry;
  private constructor() {}
  static instance() {
    return (this.value ??= new Registry());
  }
}
```

**Tradeoff:** Guarantees identity but hides dependencies, couples tests to global state, and combines lifecycle with business responsibility.

References: [main article](https://refactoring.guru/design-patterns/singleton), [TypeScript example](https://refactoring.guru/design-patterns/singleton/typescript/example)
