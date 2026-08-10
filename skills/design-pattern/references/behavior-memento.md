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
class Caretaker {
  private readonly history: string[] = [];
  backup(originator: Originator): void {
    this.history.push(originator.state); // reaches into private originator state
  }
}
```

**Correct (originator, memento, and caretaker keep responsibilities separate):**

```typescript
class Originator {
  constructor(private state: string) {}

  changeState(state: string): void {
    this.state = state;
  }

  save(): Memento {
    return new ConcreteMemento(this.state);
  }

  restore(memento: Memento): void {
    this.state = memento.getState();
  }
}

interface Memento {
  getState(): string;
  getName(): string;
  getDate(): Date;
}

class ConcreteMemento implements Memento {
  private readonly date = new Date();

  constructor(private readonly state: string) {}

  getState(): string {
    return this.state;
  }

  getName(): string {
    return `${this.date.toISOString()} / ${this.state.slice(0, 9)}`;
  }

  getDate(): Date {
    return this.date;
  }
}

class Caretaker {
  private readonly mementos: Memento[] = [];

  constructor(private readonly originator: Originator) {}

  backup(): void {
    this.mementos.push(this.originator.save());
  }

  undo(): void {
    const memento = this.mementos.pop();
    if (memento) this.originator.restore(memento);
  }

  showHistory(): string[] {
    return this.mementos.map((memento) => memento.getName());
  }
}

const originator = new Originator("Initial state");
const caretaker = new Caretaker(originator);
caretaker.backup();
originator.changeState("Changed state");
caretaker.undo();
```

**Tradeoff:** Preserves encapsulation, but snapshots may consume memory and require versioning.

References: [main article](https://refactoring.guru/design-patterns/memento), [TypeScript example](https://refactoring.guru/design-patterns/memento/typescript/example)
