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
function clientCode(collection: WordsCollection): void {
  for (let position = 0; position < collection.getCount(); position++) {
    console.log(collection.getItems()[position]);
  }
}
```

**Correct (collection and iterator contracts support forward and reverse traversal):**

```typescript
interface Iterator<T> {
  current(): T;
  key(): number;
  next(): T;
  valid(): boolean;
  rewind(): void;
}

interface Aggregator<T> {
  getIterator(): Iterator<T>;
}

class AlphabeticalOrderIterator implements Iterator<string> {
  private position = 0;

  constructor(
    private readonly collection: WordsCollection,
    private readonly reverse = false,
  ) {
    this.rewind();
  }

  rewind(): void {
    this.position = this.reverse ? this.collection.getCount() - 1 : 0;
  }

  current(): string {
    return this.collection.getItems()[this.position];
  }

  key(): number {
    return this.position;
  }

  next(): string {
    const item = this.current();
    this.position += this.reverse ? -1 : 1;
    return item;
  }

  valid(): boolean {
    return this.reverse ? this.position >= 0 : this.position < this.collection.getCount();
  }
}

class WordsCollection implements Aggregator<string> {
  private readonly items: string[] = [];

  getItems(): string[] {
    return this.items;
  }

  getCount(): number {
    return this.items.length;
  }

  addItem(item: string): void {
    this.items.push(item);
  }

  getIterator(): Iterator<string> {
    return new AlphabeticalOrderIterator(this);
  }

  getReverseIterator(): Iterator<string> {
    return new AlphabeticalOrderIterator(this, true);
  }
}

const collection = new WordsCollection();
collection.addItem("First");
collection.addItem("Second");
const iterator = collection.getIterator();
while (iterator.valid()) console.log(iterator.next());
```

**Tradeoff:** Supports interchangeable traversals, but wrapping a simple array can be needless overhead.

References: [main article](https://refactoring.guru/design-patterns/iterator), [TypeScript example](https://refactoring.guru/design-patterns/iterator/typescript/example)
