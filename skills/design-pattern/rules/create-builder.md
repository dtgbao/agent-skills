---
title: Use Builder for Step-by-Step Construction
impact: CRITICAL
impactDescription: "Popularity: 3/3; Complexity: 2/3"
tags: creational, builder, construction
---

## Use Builder for Step-by-Step Construction

Use Builder when a complex product has optional or ordered construction steps, or when the same process must produce different representations.

**Incorrect (client owns and repeats the construction sequence):**

```typescript
const product = new Product1();
product.parts.push("PartA", "PartB", "PartC");
```

**Correct (separate construction steps, concrete builders, and reusable recipes):**

```typescript
interface Builder {
  producePartA(): void;
  producePartB(): void;
  producePartC(): void;
}

class Product1 {
  readonly parts: string[] = [];

  listParts(): string {
    return this.parts.join(", ");
  }
}

class ConcreteBuilder1 implements Builder {
  private product!: Product1;

  constructor() {
    this.reset();
  }

  reset(): void {
    this.product = new Product1();
  }

  producePartA(): void {
    this.product.parts.push("PartA");
  }

  producePartB(): void {
    this.product.parts.push("PartB");
  }

  producePartC(): void {
    this.product.parts.push("PartC");
  }

  getProduct(): Product1 {
    const result = this.product;
    this.reset();
    return result;
  }
}

class Director {
  private builder!: Builder;

  setBuilder(builder: Builder): void {
    this.builder = builder;
  }

  buildMinimalViableProduct(): void {
    this.builder.producePartA();
  }

  buildFullFeaturedProduct(): void {
    this.builder.producePartA();
    this.builder.producePartB();
    this.builder.producePartC();
  }
}

function clientCode(director: Director): void {
  const builder = new ConcreteBuilder1();
  director.setBuilder(builder);

  director.buildMinimalViableProduct();
  console.log(builder.getProduct().listParts());

  director.buildFullFeaturedProduct();
  console.log(builder.getProduct().listParts());

  builder.producePartA();
  builder.producePartC();
  console.log(builder.getProduct().listParts());
}

clientCode(new Director());
```

**Tradeoff:** Construction becomes readable and reusable but introduces another type and mutable build state.

References: [main article](https://refactoring.guru/design-patterns/builder), [TypeScript example](https://refactoring.guru/design-patterns/builder/typescript/example)
