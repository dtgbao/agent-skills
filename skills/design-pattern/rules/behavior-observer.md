---
title: Use Observer for Dynamic Subscriptions
impact: CRITICAL
impactDescription: "Popularity: 3/3; Complexity: 2/3"
tags: behavioral, observer, events
---

## Use Observer for Dynamic Subscriptions

Use Observer when a subject must notify a changing set of subscribers without depending on their concrete classes.

**Incorrect (publisher calls concrete consumers):**

```typescript
inventory.update();
email.send();
analytics.track();
```

**Correct (manage subscribers through a contract):**

```typescript
interface Observer {
  update(value: number): void;
}
class Subject {
  private observers = new Set<Observer>();
  attach(observer: Observer) {
    this.observers.add(observer);
  }
  notify(value: number) {
    this.observers.forEach((observer) => observer.update(value));
  }
}
```

**Tradeoff:** Decouples publishers and subscribers, but notification order and failure semantics can become unclear.

References: [main article](https://refactoring.guru/design-patterns/observer), [TypeScript example](https://refactoring.guru/design-patterns/observer/typescript/example)
