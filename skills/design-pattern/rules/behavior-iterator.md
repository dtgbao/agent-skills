---
title: Use Iterator to Encapsulate Traversal
impact: CRITICAL
impactDescription: "Popularity: 3/3; Complexity: 2/3"
tags: behavioral, iterator, traversal
---

## Use Iterator to Encapsulate Traversal

Use Iterator when clients need uniform, stateful, lazy, or specialized traversal without seeing collection internals.

**Incorrect (client depends on representation):**

```typescript
for (let node = tree.root; node; node = node.left) visit(node.value);
```

**Correct (expose the language iterator protocol):**

```typescript
class Words implements Iterable<string> {
  constructor(private items: string[]) {}
  *[Symbol.iterator]() {
    yield* this.items;
  }
}
```

**Tradeoff:** Supports interchangeable traversals, but wrapping a simple array can be needless overhead.

References: [main article](https://refactoring.guru/design-patterns/iterator), [TypeScript example](https://refactoring.guru/design-patterns/iterator/typescript/example)
