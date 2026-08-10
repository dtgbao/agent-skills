---
title: Use Singleton Only for One Required Instance
impact: HIGH
impactDescription: "Popularity: 2/3; Complexity: 1/3"
tags: creational, singleton, lifecycle
---

## Use Singleton Only for One Required Instance

Use Singleton only when the domain requires exactly one instance and clients need a controlled access point. Prefer dependency injection when available.

**Incorrect (clients can create multiple instances):**

```typescript
class Singleton {}
const first = new Singleton();
const second = new Singleton();
first === second; // false
```

**Correct (a static accessor controls the single cached instance):**

```typescript
class Singleton {
  private static cached?: Singleton;

  private constructor() {}

  static get instance(): Singleton {
    return (this.cached ??= new Singleton());
  }

  someBusinessLogic(): string {
    return "shared result";
  }
}

function clientCode(): boolean {
  const first = Singleton.instance;
  const second = Singleton.instance;
  first.someBusinessLogic();
  return first === second;
}

clientCode();
```

**Tradeoff:** Guarantees identity but hides dependencies, couples tests to global state, and combines lifecycle with business responsibility.

References: [main article](https://refactoring.guru/design-patterns/singleton), [TypeScript example](https://refactoring.guru/design-patterns/singleton/typescript/example)
