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
class Context {
  doSomeBusinessLogic(values: string[], mode: "ascending" | "descending"): string[] {
    return mode === "ascending" ? [...values].sort() : [...values].sort().reverse();
  }
}
```

**Correct (a context delegates to replaceable concrete strategies):**

```typescript
class Context {
  constructor(private strategy: Strategy) {}

  setStrategy(strategy: Strategy): void {
    this.strategy = strategy;
  }

  doSomeBusinessLogic(values: string[]): string[] {
    return this.strategy.doAlgorithm(values);
  }
}

interface Strategy {
  doAlgorithm(data: string[]): string[];
}

class ConcreteStrategyA implements Strategy {
  doAlgorithm(data: string[]): string[] {
    return [...data].sort();
  }
}

class ConcreteStrategyB implements Strategy {
  doAlgorithm(data: string[]): string[] {
    return [...data].sort().reverse();
  }
}

const context = new Context(new ConcreteStrategyA());
context.doSomeBusinessLogic(["a", "b", "c"]);
context.setStrategy(new ConcreteStrategyB());
context.doSomeBusinessLogic(["a", "b", "c"]);
```

**Tradeoff:** Algorithms vary independently, but clients must understand which strategy to choose. Functions may replace classes for simple algorithms.

References: [main article](https://refactoring.guru/design-patterns/strategy), [TypeScript example](https://refactoring.guru/design-patterns/strategy/typescript/example)
