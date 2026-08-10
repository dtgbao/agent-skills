---
title: Use Adapter to Translate an Incompatible Interface
impact: CRITICAL
impactDescription: "Popularity: 3/3; Complexity: 1/3"
tags: structural, adapter, integration
---

## Use Adapter to Translate an Incompatible Interface

Use Adapter to make a legacy or third-party object satisfy the interface expected by existing clients.

**Incorrect (translation leaks into every client):**

```typescript
function clientCode(adaptee: Adaptee): string {
  return adaptee.specificRequest().split("").reverse().join("");
}
```

**Correct (an adapter translates the target call to the adaptee):**

```typescript
class Target {
  request(): string {
    return "Target behavior";
  }
}

class Adaptee {
  specificRequest(): string {
    return "eetpadA";
  }
}

class Adapter extends Target {
  constructor(private readonly adaptee: Adaptee) {
    super();
  }

  request(): string {
    return this.adaptee.specificRequest().split("").reverse().join("");
  }
}

function clientCode(target: Target): string {
  return target.request();
}

clientCode(new Target());
clientCode(new Adapter(new Adaptee()));
```

**Tradeoff:** Isolates conversion but adds a wrapper. Change the adaptee directly when you own it and compatibility is unnecessary.

References: [main article](https://refactoring.guru/design-patterns/adapter), [TypeScript example](https://refactoring.guru/design-patterns/adapter/typescript/example)
