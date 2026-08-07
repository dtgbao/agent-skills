---
title: Use Template Method for an Invariant Algorithm Skeleton
impact: HIGH
impactDescription: "Popularity: 2/3; Complexity: 1/3"
tags: behavioral, template-method, inheritance
---

## Use Template Method for an Invariant Algorithm Skeleton

Use Template Method when subclasses may vary selected steps but must preserve the overall algorithm order.

**Incorrect (duplicate workflows drift apart):**

```typescript
class ConcreteClass1 {
  templateMethod(): void {
    baseOperation1();
    concreteClass1RequiredOperation1();
    baseOperation2();
  }
}

class ConcreteClass2 {
  templateMethod(): void {
    baseOperation1();
    concreteClass2RequiredOperation1();
    baseOperation2();
  }
}
```

**Correct (the template calls invariant steps, required operations, and hooks):**

```typescript
abstract class AbstractClass {
  templateMethod(): void {
    this.baseOperation1();
    this.requiredOperation1();
    this.baseOperation2();
    this.hook1();
    this.requiredOperation2();
    this.baseOperation3();
    this.hook2();
  }

  protected baseOperation1(): void {
    console.log("Base operation 1");
  }

  protected baseOperation2(): void {
    console.log("Base operation 2");
  }

  protected baseOperation3(): void {
    console.log("Base operation 3");
  }

  protected abstract requiredOperation1(): void;
  protected abstract requiredOperation2(): void;
  protected hook1(): void {}
  protected hook2(): void {}
}

class ConcreteClass1 extends AbstractClass {
  protected requiredOperation1(): void {
    console.log("ConcreteClass1 operation 1");
  }

  protected requiredOperation2(): void {
    console.log("ConcreteClass1 operation 2");
  }
}

class ConcreteClass2 extends AbstractClass {
  protected requiredOperation1(): void {
    console.log("ConcreteClass2 operation 1");
  }

  protected requiredOperation2(): void {
    console.log("ConcreteClass2 operation 2");
  }

  protected hook1(): void {
    console.log("ConcreteClass2 hook");
  }
}

function clientCode(abstractClass: AbstractClass): void {
  abstractClass.templateMethod();
}

clientCode(new ConcreteClass1());
clientCode(new ConcreteClass2());
```

**Tradeoff:** Removes workflow duplication, but inheritance fixes variation at class level and may constrain subclasses.

References: [main article](https://refactoring.guru/design-patterns/template-method), [TypeScript example](https://refactoring.guru/design-patterns/template-method/typescript/example)
