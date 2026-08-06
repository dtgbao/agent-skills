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
button.onClick = () => editor.save(path, format);
```

**Correct (capture receiver and parameters):**

```typescript
interface Command {
  execute(): void;
}
class SaveCommand implements Command {
  constructor(
    private editor: Editor,
    private path: string,
  ) {}
  execute() {
    this.editor.save(this.path);
  }
}
```

**Tradeoff:** Enables deferred execution and history but adds an object layer between sender and receiver.

References: [main article](https://refactoring.guru/design-patterns/command), [TypeScript example](https://refactoring.guru/design-patterns/command/typescript/example)
