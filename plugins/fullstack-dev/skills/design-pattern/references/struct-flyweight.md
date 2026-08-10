---
title: Use Flyweight to Share Intrinsic State
impact: LOW
impactDescription: "Popularity: 0/3; Complexity: 3/3"
tags: structural, flyweight, memory
---

## Use Flyweight to Share Intrinsic State

Use Flyweight only when profiling shows that many objects duplicate large immutable intrinsic state.

**Incorrect (duplicate shared data per object):**

```typescript
const first = new Flyweight(["BMW", "M5", "red"]);
const second = new Flyweight(["BMW", "M5", "red"]); // duplicates intrinsic state
```

**Correct (a factory caches flyweights by intrinsic state):**

```typescript
class Flyweight {
  constructor(private readonly sharedState: readonly string[]) {}

  operation(uniqueState: readonly string[]): string {
    return JSON.stringify({ shared: this.sharedState, unique: uniqueState });
  }
}

class FlyweightFactory {
  private readonly flyweights = new Map<string, Flyweight>();

  constructor(initialStates: readonly string[][]) {
    initialStates.forEach((state) => this.flyweights.set(this.getKey(state), new Flyweight(state)));
  }

  private getKey(state: readonly string[]): string {
    return [...state].sort().join("_");
  }

  getFlyweight(sharedState: readonly string[]): Flyweight {
    const key = this.getKey(sharedState);
    const existing = this.flyweights.get(key);
    if (existing) return existing;

    const created = new Flyweight(sharedState);
    this.flyweights.set(key, created);
    return created;
  }
}

function addCarToDatabase(
  factory: FlyweightFactory,
  plate: string,
  owner: string,
  brand: string,
  model: string,
  color: string,
): string {
  return factory.getFlyweight([brand, model, color]).operation([plate, owner]);
}

const factory = new FlyweightFactory([["BMW", "M5", "red"]]);
addCarToDatabase(factory, "CL234IR", "James", "BMW", "M5", "red");
```

**Tradeoff:** Saves memory at scale but adds lookup cost, state separation, and cache-lifecycle complexity.

References: [main article](https://refactoring.guru/design-patterns/flyweight), [TypeScript example](https://refactoring.guru/design-patterns/flyweight/typescript/example)
