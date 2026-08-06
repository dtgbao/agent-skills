---
title: Use Flyweight to Share Intrinsic State
impact: LOW
impactDescription: "Popularity: 0/3; Complexity: 3/3"
tags: structural, flyweight, memory
---

## Use Flyweight to Share Intrinsic State

Use Flyweight only when profiling shows that many objects duplicate large immutable intrinsic state.

**Incorrect (duplicate shared data per object):**

```typescript
cars.push({ owner, plate, make, model, color });
```

**Correct (cache intrinsic state and pass extrinsic state):**

```typescript
class CarType {
  constructor(
    readonly make: string,
    readonly model: string,
    readonly color: string,
  ) {}
}
const types = new Map<string, CarType>();
const type = types.get(key) ?? new CarType(make, model, color);
types.set(key, type);
```

**Tradeoff:** Saves memory at scale but adds lookup cost, state separation, and cache-lifecycle complexity.

References: [main article](https://refactoring.guru/design-patterns/flyweight), [TypeScript example](https://refactoring.guru/design-patterns/flyweight/typescript/example)
