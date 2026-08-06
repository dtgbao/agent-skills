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
function deliver(mode: string) {
  return mode === "sea" ? new Ship() : new Truck();
}
```

**Correct (subclasses override creation):**

```typescript
abstract class Logistics {
  protected abstract createTransport(): Transport;
  plan() {
    return this.createTransport().deliver();
  }
}
class SeaLogistics extends Logistics {
  protected createTransport() {
    return new Ship();
  }
}
```

**Tradeoff:** Product coupling falls, but subclass count grows. Prefer a simple factory function when inheritance adds no value.

References: [main article](https://refactoring.guru/design-patterns/factory-method), [TypeScript example](https://refactoring.guru/design-patterns/factory-method/typescript/example)
