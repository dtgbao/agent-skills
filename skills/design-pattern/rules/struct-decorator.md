---
title: Use Decorator to Stack Optional Behavior
impact: HIGH
impactDescription: "Popularity: 2/3; Complexity: 2/3"
tags: structural, decorator, composition
---

## Use Decorator to Stack Optional Behavior

Use Decorator to add responsibilities dynamically while preserving the wrapped component contract.

**Incorrect (subclass per behavior combination):**

```typescript
class LoggedCachedCompressedStore extends Store {}
```

**Correct (compose wrappers):**

```typescript
interface Store {
  save(value: string): void;
}
class LoggedStore implements Store {
  constructor(private inner: Store) {}
  save(value: string) {
    console.log("save");
    this.inner.save(value);
  }
}
```

**Tradeoff:** Behaviors compose freely, but wrapper order matters and a deep stack is harder to debug.

References: [main article](https://refactoring.guru/design-patterns/decorator), [TypeScript example](https://refactoring.guru/design-patterns/decorator/typescript/example)
