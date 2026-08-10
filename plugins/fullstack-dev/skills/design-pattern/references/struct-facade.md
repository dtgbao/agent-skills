---
title: Use Facade for a Simple Subsystem Entry Point
impact: HIGH
impactDescription: "Popularity: 2/3; Complexity: 1/3"
tags: structural, facade, subsystem
---

## Use Facade for a Simple Subsystem Entry Point

Use Facade to expose common operations without making clients coordinate a complex subsystem.

**Incorrect (every client repeats orchestration):**

```typescript
function clientCode(subsystem1: Subsystem1, subsystem2: Subsystem2): string {
  return `${subsystem1.operation1()}; ${subsystem2.operation1()}; ` +
    `${subsystem1.operationN()}; ${subsystem2.operationZ()}`;
}
```

**Correct (the facade coordinates multiple subsystem objects):**

```typescript
class Subsystem1 {
  operation1(): string {
    return "Subsystem1 ready";
  }

  operationN(): string {
    return "Subsystem1 go";
  }
}

class Subsystem2 {
  operation1(): string {
    return "Subsystem2 ready";
  }

  operationZ(): string {
    return "Subsystem2 fire";
  }
}

class Facade {
  constructor(
    protected subsystem1 = new Subsystem1(),
    protected subsystem2 = new Subsystem2(),
  ) {}

  operation(): string {
    return [
      this.subsystem1.operation1(),
      this.subsystem2.operation1(),
      this.subsystem1.operationN(),
      this.subsystem2.operationZ(),
    ].join("; ");
  }
}

function clientCode(facade: Facade): string {
  return facade.operation();
}

clientCode(new Facade(new Subsystem1(), new Subsystem2()));
```

**Tradeoff:** Reduces client coupling, but an oversized facade can become a god object.

References: [main article](https://refactoring.guru/design-patterns/facade), [TypeScript example](https://refactoring.guru/design-patterns/facade/typescript/example)
