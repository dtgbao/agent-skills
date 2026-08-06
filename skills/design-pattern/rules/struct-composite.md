---
title: Use Composite for Uniform Object Trees
impact: HIGH
impactDescription: "Popularity: 2/3; Complexity: 2/3"
tags: structural, composite, trees
---

## Use Composite for Uniform Object Trees

Use Composite when leaves and containers form a tree and clients should treat both through one contract.

**Incorrect (clients branch on node shape):**

```typescript
if ("children" in node) node.children.forEach(run);
else node.run();
```

**Correct (each component implements the operation):**

```typescript
interface Task {
  run(): void;
}
class TaskGroup implements Task {
  constructor(private children: Task[]) {}
  run() {
    this.children.forEach((child) => child.run());
  }
}
```

**Tradeoff:** Simplifies recursive clients but can force unrelated leaves into an overly broad interface.

References: [main article](https://refactoring.guru/design-patterns/composite), [TypeScript example](https://refactoring.guru/design-patterns/composite/typescript/example)
