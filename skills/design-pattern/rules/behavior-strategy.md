---
title: Use Strategy for Interchangeable Algorithms
impact: CRITICAL
impactDescription: "Popularity: 3/3; Complexity: 1/3"
tags: behavioral, strategy, algorithms
---

## Use Strategy for Interchangeable Algorithms

Use Strategy when clients need to select among algorithms that perform the same responsibility.

**Incorrect (context owns every algorithm branch):**

```typescript
return mode === "fast" ? fastSort(data) : stableSort(data);
```

**Correct (inject an algorithm contract):**

```typescript
interface SortStrategy {
  sort(values: string[]): string[];
}
class Context {
  constructor(private strategy: SortStrategy) {}
  sort(values: string[]) {
    return this.strategy.sort(values);
  }
}
```

**Tradeoff:** Algorithms vary independently, but clients must understand which strategy to choose. Functions may replace classes for simple algorithms.

References: [main article](https://refactoring.guru/design-patterns/strategy), [TypeScript example](https://refactoring.guru/design-patterns/strategy/typescript/example)
