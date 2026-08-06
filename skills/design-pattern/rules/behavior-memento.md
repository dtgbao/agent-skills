---
title: Use Memento to Snapshot Encapsulated State
impact: MEDIUM
impactDescription: "Popularity: 1/3; Complexity: 3/3"
tags: behavioral, memento, undo
---

## Use Memento to Snapshot Encapsulated State

Use Memento when state must be restored without exposing the originator's representation to the history owner.

**Incorrect (caretaker mutates private state directly):**

```typescript
history.push(editor.internalState);
editor.internalState = history.pop();
```

**Correct (originator creates and restores snapshots):**

```typescript
type Snapshot = Readonly<{ text: string }>;
class Editor {
  constructor(private text = "") {}
  save(): Snapshot {
    return { text: this.text };
  }
  restore(snapshot: Snapshot) {
    this.text = snapshot.text;
  }
}
```

**Tradeoff:** Preserves encapsulation, but snapshots may consume memory and require versioning.

References: [main article](https://refactoring.guru/design-patterns/memento), [TypeScript example](https://refactoring.guru/design-patterns/memento/typescript/example)
