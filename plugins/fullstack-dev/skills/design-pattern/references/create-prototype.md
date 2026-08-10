---
title: Use Prototype to Copy Configured Objects
impact: HIGH
impactDescription: "Popularity: 2/3; Complexity: 1/3"
tags: creational, prototype, cloning
---

## Use Prototype to Copy Configured Objects

Use Prototype when clients must copy configured objects without depending on their concrete classes. Define whether nested state is copied or shared.

**Incorrect (shallow copy aliases mutable state):**

```typescript
const original = new Prototype();
const copy = Object.assign(Object.create(Object.getPrototypeOf(original)), original);
copy.component === original.component; // nested state is still shared
```

**Correct (the prototype clones primitive, nested, and back-reference state):**

```typescript
class Prototype {
  primitive = 0;
  component = { createdAt: new Date() };
  circularReference!: ComponentWithBackReference;

  clone(): this {
    const clone = Object.create(Object.getPrototypeOf(this));
    Object.assign(clone, this);
    clone.component = { createdAt: new Date(this.component.createdAt) };
    clone.circularReference = new ComponentWithBackReference(clone);
    return clone;
  }
}

class ComponentWithBackReference {
  constructor(public prototype: Prototype) {}
}

function clientCode(): boolean {
  const original = new Prototype();
  original.primitive = 42;
  original.circularReference = new ComponentWithBackReference(original);

  const copy = original.clone();
  return (
    copy !== original &&
    copy.component !== original.component &&
    copy.circularReference.prototype === copy
  );
}

clientCode();
```

**Tradeoff:** Reuses expensive configuration, but cyclic graphs and external resources make cloning difficult.

References: [main article](https://refactoring.guru/design-patterns/prototype), [TypeScript example](https://refactoring.guru/design-patterns/prototype/typescript/example)
