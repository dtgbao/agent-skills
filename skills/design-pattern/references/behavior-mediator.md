---
title: Use Mediator to Centralize Component Collaboration
impact: LOW
impactDescription: "Popularity: 0/3; Complexity: 2/3"
tags: behavioral, mediator, coupling
---

## Use Mediator to Centralize Component Collaboration

Use Mediator when peer components are tightly coupled and their collaboration rules should live in one object.

**Incorrect (components call each other directly):**

```typescript
class Component1 {
  constructor(private readonly component2: Component2) {}
  doA(): void {
    this.component2.doC();
  }
}
```

**Correct (a mediator owns component collaboration and wires itself into peers):**

```typescript
interface Mediator {
  notify(sender: object, event: string): void;
}

class ConcreteMediator implements Mediator {
  constructor(
    private readonly component1: Component1,
    private readonly component2: Component2,
  ) {
    component1.setMediator(this);
    component2.setMediator(this);
  }

  notify(_sender: object, event: string): void {
    if (event === "A") {
      this.component2.doC();
    }
    if (event === "D") {
      this.component1.doB();
      this.component2.doC();
    }
  }
}

class BaseComponent {
  protected mediator?: Mediator;

  setMediator(mediator: Mediator): void {
    this.mediator = mediator;
  }
}

class Component1 extends BaseComponent {
  doA(): void {
    console.log("Component 1 does A");
    this.mediator?.notify(this, "A");
  }

  doB(): void {
    console.log("Component 1 does B");
  }
}

class Component2 extends BaseComponent {
  doC(): void {
    console.log("Component 2 does C");
  }

  doD(): void {
    console.log("Component 2 does D");
    this.mediator?.notify(this, "D");
  }
}

const component1 = new Component1();
const component2 = new Component2();
new ConcreteMediator(component1, component2);
component1.doA();
component2.doD();
```

**Tradeoff:** Reduces peer coupling, but a mediator can accumulate too many unrelated rules.

References: [main article](https://refactoring.guru/design-patterns/mediator), [TypeScript example](https://refactoring.guru/design-patterns/mediator/typescript/example)
