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
class ConcreteSubject {
  someBusinessLogic(): void {
    new ConcreteObserverA().update(this);
    new ConcreteObserverB().update(this);
  }
}
```

**Correct (a subject manages subscribers and concrete observers react to updates):**

```typescript
interface Subject {
  attach(observer: Observer): void;
  detach(observer: Observer): void;
  notify(): void;
}

interface Observer {
  update(subject: Subject): void;
}

class ConcreteSubject implements Subject {
  state = 0;
  private readonly observers = new Set<Observer>();

  attach(observer: Observer): void {
    this.observers.add(observer);
  }

  detach(observer: Observer): void {
    this.observers.delete(observer);
  }

  notify(): void {
    this.observers.forEach((observer) => observer.update(this));
  }

  someBusinessLogic(): void {
    this.state = Math.floor(Math.random() * 10);
    this.notify();
  }
}

class ConcreteObserverA implements Observer {
  update(subject: Subject): void {
    if (subject instanceof ConcreteSubject && subject.state < 3) {
      console.log("Observer A reacted");
    }
  }
}

class ConcreteObserverB implements Observer {
  update(subject: Subject): void {
    if (subject instanceof ConcreteSubject && subject.state >= 2) {
      console.log("Observer B reacted");
    }
  }
}

const subject = new ConcreteSubject();
const observerA = new ConcreteObserverA();
const observerB = new ConcreteObserverB();
subject.attach(observerA);
subject.attach(observerB);
subject.someBusinessLogic();
subject.detach(observerB);
```

**Tradeoff:** Decouples publishers and subscribers, but notification order and failure semantics can become unclear.

References: [main article](https://refactoring.guru/design-patterns/observer), [TypeScript example](https://refactoring.guru/design-patterns/observer/typescript/example)
