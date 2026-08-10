---
title: Use Command to Represent Requests as Objects
impact: CRITICAL
impactDescription: "Popularity: 3/3; Complexity: 1/3"
tags: behavioral, command, queueing
---

## Use Command to Represent Requests as Objects

Use Command when an operation must be queued, logged, scheduled, sent remotely, composed, or undone.

**Incorrect (invoker knows receiver details):**

```typescript
class Invoker {
  doSomethingImportant(receiver: Receiver): void {
    receiver.doSomething("Send email");
    receiver.doSomethingElse("Save report");
  }
}
```

**Correct (commands connect an invoker to simple or receiver-backed work):**

```typescript
interface Command {
  execute(): void;
}

class SimpleCommand implements Command {
  constructor(private readonly payload: string) {}

  execute(): void {
    console.log(`Simple command: ${this.payload}`);
  }
}

class ComplexCommand implements Command {
  constructor(
    private readonly receiver: Receiver,
    private readonly a: string,
    private readonly b: string,
  ) {}

  execute(): void {
    this.receiver.doSomething(this.a);
    this.receiver.doSomethingElse(this.b);
  }
}

class Receiver {
  doSomething(value: string): void {
    console.log(`Receiver working on ${value}`);
  }

  doSomethingElse(value: string): void {
    console.log(`Receiver also working on ${value}`);
  }
}

class Invoker {
  private onStart?: Command;
  private onFinish?: Command;

  setOnStart(command: Command): void {
    this.onStart = command;
  }

  setOnFinish(command: Command): void {
    this.onFinish = command;
  }

  doSomethingImportant(): void {
    this.onStart?.execute();
    console.log("Invoker performing its own operation");
    this.onFinish?.execute();
  }
}

const invoker = new Invoker();
invoker.setOnStart(new SimpleCommand("Say Hi!"));
invoker.setOnFinish(new ComplexCommand(new Receiver(), "Send email", "Save report"));
invoker.doSomethingImportant();
```

**Tradeoff:** Enables deferred execution and history but adds an object layer between sender and receiver.

References: [main article](https://refactoring.guru/design-patterns/command), [TypeScript example](https://refactoring.guru/design-patterns/command/typescript/example)
