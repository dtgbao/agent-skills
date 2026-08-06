---
title: Use Prototype to Copy Configured Objects
impact: HIGH
impactDescription: "Popularity: 2/3; Complexity: 1/3"
tags: creational, prototype, cloning
---

## Use Prototype to Copy Configured Objects

Use Prototype when clients must copy configured objects without depending on their concrete classes. Define whether nested state is copied or shared.

**Incorrect (shallow copy aliases mutable state):**

```typescript
const copy = { ...template }; // nested rules remain shared
```

**Correct (the prototype owns copy semantics):**

```typescript
interface Prototype<T> {
  clone(): T;
}

class Plan implements Prototype<Plan> {
  constructor(readonly rules: Rule[]) {}
  clone() {
    return new Plan(this.rules.map((rule) => rule.clone()));
  }
}
```

**Tradeoff:** Reuses expensive configuration, but cyclic graphs and external resources make cloning difficult.

References: [main article](https://refactoring.guru/design-patterns/prototype), [TypeScript example](https://refactoring.guru/design-patterns/prototype/typescript/example)
