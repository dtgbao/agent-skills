---
title: Use State for State-Dependent Behavior
impact: HIGH
impactDescription: "Popularity: 2/3; Complexity: 1/3"
tags: behavioral, state, transitions
---

## Use State for State-Dependent Behavior

Use State when behavior changes with internal state and large conditionals obscure transitions.

**Incorrect (conditionals spread across methods):**

```typescript
class Context {
  state: "A" | "B" = "A";
  request1(): void {
    if (this.state === "A") this.state = "B";
    else console.log("State B handles request 1");
  }
}
```

**Correct (context and concrete states manage behavior and transitions):**

```typescript
class Context {
  private state!: State;

  constructor(state: State) {
    this.transitionTo(state);
  }

  transitionTo(state: State): void {
    this.state = state;
    this.state.context = this;
  }

  request1(): void {
    this.state.handle1();
  }

  request2(): void {
    this.state.handle2();
  }
}

abstract class State {
  protected currentContext!: Context;

  set context(context: Context) {
    this.currentContext = context;
  }

  abstract handle1(): void;
  abstract handle2(): void;
}

class ConcreteStateA extends State {
  handle1(): void {
    console.log("State A handles request 1 and moves to B");
    this.currentContext.transitionTo(new ConcreteStateB());
  }

  handle2(): void {
    console.log("State A handles request 2");
  }
}

class ConcreteStateB extends State {
  handle1(): void {
    console.log("State B handles request 1");
  }

  handle2(): void {
    console.log("State B handles request 2 and moves to A");
    this.currentContext.transitionTo(new ConcreteStateA());
  }
}

const context = new Context(new ConcreteStateA());
context.request1();
context.request2();
```

**Tradeoff:** Localizes transitions but creates more types; use a discriminated union for a small stable machine.

References: [main article](https://refactoring.guru/design-patterns/state), [TypeScript example](https://refactoring.guru/design-patterns/state/typescript/example)
