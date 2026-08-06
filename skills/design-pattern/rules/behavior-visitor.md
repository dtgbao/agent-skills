---
title: Use Visitor for Operations over a Stable Hierarchy
impact: MEDIUM
impactDescription: "Popularity: 1/3; Complexity: 3/3"
tags: behavioral, visitor, double-dispatch
---

## Use Visitor for Operations over a Stable Hierarchy

Use Visitor when element types are stable but many operations must be added without modifying those elements.

**Incorrect (operation branches on concrete elements):**

```typescript
if (node instanceof TextNode) renderText(node);
else if (node instanceof ImageNode) renderImage(node);
```

**Correct (elements dispatch to visitor overloads):**

```typescript
interface Node {
  accept<T>(visitor: Visitor<T>): T;
}
interface Visitor<T> {
  text(node: TextNode): T;
  image(node: ImageNode): T;
}
class TextNode implements Node {
  accept<T>(visitor: Visitor<T>) {
    return visitor.text(this);
  }
}
```

**Tradeoff:** New operations are easy; adding an element type requires changing every visitor.

References: [main article](https://refactoring.guru/design-patterns/visitor), [TypeScript example](https://refactoring.guru/design-patterns/visitor/typescript/example)
