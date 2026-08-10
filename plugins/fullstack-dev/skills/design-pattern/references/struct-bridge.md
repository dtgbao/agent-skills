---
title: Use Bridge for Independent Dimensions
impact: MEDIUM
impactDescription: "Popularity: 1/3; Complexity: 3/3"
tags: structural, bridge, composition
---

## Use Bridge for Independent Dimensions

Use Bridge when two dimensions must evolve independently without creating a subclass for every combination.

**Incorrect (class explosion):**

```typescript
class AbstractionWithConcreteImplementationA {}
class AbstractionWithConcreteImplementationB {}
class ExtendedAbstractionWithConcreteImplementationA {}
class ExtendedAbstractionWithConcreteImplementationB {}
```

**Correct (abstractions delegate to interchangeable implementations):**

```typescript
class Abstraction {
  constructor(protected implementation: Implementation) {}

  operation(): string {
    return `Abstraction: ${this.implementation.operationImplementation()}`;
  }
}

class ExtendedAbstraction extends Abstraction {
  operation(): string {
    return `Extended: ${this.implementation.operationImplementation()}`;
  }
}

interface Implementation {
  operationImplementation(): string;
}

class ConcreteImplementationA implements Implementation {
  operationImplementation(): string {
    return "Platform A";
  }
}

class ConcreteImplementationB implements Implementation {
  operationImplementation(): string {
    return "Platform B";
  }
}

function clientCode(abstraction: Abstraction): string {
  return abstraction.operation();
}

clientCode(new Abstraction(new ConcreteImplementationA()));
clientCode(new ExtendedAbstraction(new ConcreteImplementationB()));
```

**Tradeoff:** Prevents combinatorial inheritance but adds indirection; avoid it when the dimensions are not independently variable.

References: [main article](https://refactoring.guru/design-patterns/bridge), [TypeScript example](https://refactoring.guru/design-patterns/bridge/typescript/example)
