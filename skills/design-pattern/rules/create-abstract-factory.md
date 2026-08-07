---
title: Use Abstract Factory for Compatible Product Families
impact: CRITICAL
impactDescription: "Popularity: 3/3; Complexity: 2/3"
tags: creational, abstract-factory, families
---

## Use Abstract Factory for Compatible Product Families

Use Abstract Factory when clients must create several related products that must belong to the same variant. Depend on factory and product interfaces so a whole family can change together.

**Incorrect (clients mix concrete variants):**

```typescript
const productA = new ConcreteProductA1();
const productB = new ConcreteProductB2();
productB.anotherUsefulFunctionB(productA); // incompatible product variants
```

**Correct (factories and products collaborate only through abstract contracts):**

```typescript
interface AbstractFactory {
  createProductA(): AbstractProductA;
  createProductB(): AbstractProductB;
}

class ConcreteFactory1 implements AbstractFactory {
  createProductA(): AbstractProductA {
    return new ConcreteProductA1();
  }

  createProductB(): AbstractProductB {
    return new ConcreteProductB1();
  }
}

class ConcreteFactory2 implements AbstractFactory {
  createProductA(): AbstractProductA {
    return new ConcreteProductA2();
  }

  createProductB(): AbstractProductB {
    return new ConcreteProductB2();
  }
}

interface AbstractProductA {
  usefulFunctionA(): string;
}

class ConcreteProductA1 implements AbstractProductA {
  usefulFunctionA(): string {
    return "Product A1";
  }
}

class ConcreteProductA2 implements AbstractProductA {
  usefulFunctionA(): string {
    return "Product A2";
  }
}

interface AbstractProductB {
  usefulFunctionB(): string;
  anotherUsefulFunctionB(collaborator: AbstractProductA): string;
}

class ConcreteProductB1 implements AbstractProductB {
  usefulFunctionB(): string {
    return "Product B1";
  }

  anotherUsefulFunctionB(collaborator: AbstractProductA): string {
    return `B1 collaborating with ${collaborator.usefulFunctionA()}`;
  }
}

class ConcreteProductB2 implements AbstractProductB {
  usefulFunctionB(): string {
    return "Product B2";
  }

  anotherUsefulFunctionB(collaborator: AbstractProductA): string {
    return `B2 collaborating with ${collaborator.usefulFunctionA()}`;
  }
}

function clientCode(factory: AbstractFactory): string {
  const productA = factory.createProductA();
  const productB = factory.createProductB();
  return `${productB.usefulFunctionB()}; ${productB.anotherUsefulFunctionB(productA)}`;
}

clientCode(new ConcreteFactory1());
clientCode(new ConcreteFactory2());
```

**Tradeoff:** Adding a family is easy; adding a new product kind changes every factory.

References: [main article](https://refactoring.guru/design-patterns/abstract-factory), [TypeScript example](https://refactoring.guru/design-patterns/abstract-factory/typescript/example)
