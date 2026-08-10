---
title: Use Factory Method to Decouple Product Creation
impact: CRITICAL
impactDescription: "Popularity: 3/3; Complexity: 1/3"
tags: creational, factory-method, polymorphism
---

## Use Factory Method to Decouple Product Creation

Use Factory Method when creator logic should work with a product interface while subclasses decide which concrete product to supply.

**Incorrect (creator branches on concrete types):**

```typescript
function clientCode(type: "one" | "two"): string {
  const product = type === "one" ? new ConcreteProduct1() : new ConcreteProduct2();
  return `Creator works with ${product.operation()}`;
}
```

**Correct (creators vary products while preserving creator business logic):**

```typescript
abstract class Creator {
  abstract factoryMethod(): Product;

  someOperation(): string {
    const product = this.factoryMethod();
    return `Creator works with ${product.operation()}`;
  }
}

class ConcreteCreator1 extends Creator {
  factoryMethod(): Product {
    return new ConcreteProduct1();
  }
}

class ConcreteCreator2 extends Creator {
  factoryMethod(): Product {
    return new ConcreteProduct2();
  }
}

interface Product {
  operation(): string;
}

class ConcreteProduct1 implements Product {
  operation(): string {
    return "ConcreteProduct1";
  }
}

class ConcreteProduct2 implements Product {
  operation(): string {
    return "ConcreteProduct2";
  }
}

function clientCode(creator: Creator): string {
  return creator.someOperation();
}

clientCode(new ConcreteCreator1());
clientCode(new ConcreteCreator2());
```

**Tradeoff:** Product coupling falls, but subclass count grows. Prefer a simple factory function when inheritance adds no value.

References: [main article](https://refactoring.guru/design-patterns/factory-method), [TypeScript example](https://refactoring.guru/design-patterns/factory-method/typescript/example)
