---
title: Use Decorator to Stack Optional Behavior
impact: HIGH
impactDescription: "Popularity: 2/3; Complexity: 2/3"
tags: structural, decorator, composition
---

## Use Decorator to Stack Optional Behavior

Use Decorator to add responsibilities dynamically while preserving the wrapped component contract.

**Incorrect (subclass per behavior combination):**

```typescript
class ConcreteComponentWithDecoratorAAndB extends ConcreteComponent {
  operation(): string {
    return `DecoratorB(DecoratorA(${super.operation()}))`;
  }
}
```

**Correct (base and concrete decorators preserve the component contract):**

```typescript
interface Component {
  operation(): string;
}

class ConcreteComponent implements Component {
  operation(): string {
    return "ConcreteComponent";
  }
}

class Decorator implements Component {
  constructor(protected component: Component) {}

  operation(): string {
    return this.component.operation();
  }
}

class ConcreteDecoratorA extends Decorator {
  operation(): string {
    return `DecoratorA(${super.operation()})`;
  }
}

class ConcreteDecoratorB extends Decorator {
  operation(): string {
    return `DecoratorB(${super.operation()})`;
  }
}

function clientCode(component: Component): string {
  return component.operation();
}

const decorated = new ConcreteDecoratorB(
  new ConcreteDecoratorA(new ConcreteComponent()),
);
clientCode(decorated);
```

**Tradeoff:** Behaviors compose freely, but wrapper order matters and a deep stack is harder to debug.

References: [main article](https://refactoring.guru/design-patterns/decorator), [TypeScript example](https://refactoring.guru/design-patterns/decorator/typescript/example)
