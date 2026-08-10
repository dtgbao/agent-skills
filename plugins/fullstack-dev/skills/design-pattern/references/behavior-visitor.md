---
title: Use Visitor for Operations over a Stable Hierarchy
impact: MEDIUM
impactDescription: "Popularity: 1/3; Complexity: 3/3"
tags: behavioral, visitor, double-dispatch
---

## Use Visitor for Operations over a Stable Hierarchy

Use Visitor when element types are stable but many operations must be added without modifying those elements.

**Incorrect (operation branches on concrete elements):**

```typescript
function clientCode(components: Array<ConcreteComponentA | ConcreteComponentB>): void {
  components.forEach((component) => {
    if (component instanceof ConcreteComponentA) visitA(component);
    else visitB(component);
  });
}
```

**Correct (elements and visitors perform double dispatch across all concrete types):**

```typescript
interface Component {
  accept(visitor: Visitor): void;
}

class ConcreteComponentA implements Component {
  accept(visitor: Visitor): void {
    visitor.visitConcreteComponentA(this);
  }

  exclusiveMethodOfConcreteComponentA(): string {
    return "A";
  }
}

class ConcreteComponentB implements Component {
  accept(visitor: Visitor): void {
    visitor.visitConcreteComponentB(this);
  }

  specialMethodOfConcreteComponentB(): string {
    return "B";
  }
}

interface Visitor {
  visitConcreteComponentA(element: ConcreteComponentA): void;
  visitConcreteComponentB(element: ConcreteComponentB): void;
}

class ConcreteVisitor1 implements Visitor {
  visitConcreteComponentA(element: ConcreteComponentA): void {
    console.log(`${element.exclusiveMethodOfConcreteComponentA()} + Visitor1`);
  }

  visitConcreteComponentB(element: ConcreteComponentB): void {
    console.log(`${element.specialMethodOfConcreteComponentB()} + Visitor1`);
  }
}

class ConcreteVisitor2 implements Visitor {
  visitConcreteComponentA(element: ConcreteComponentA): void {
    console.log(`${element.exclusiveMethodOfConcreteComponentA()} + Visitor2`);
  }

  visitConcreteComponentB(element: ConcreteComponentB): void {
    console.log(`${element.specialMethodOfConcreteComponentB()} + Visitor2`);
  }
}

function clientCode(components: Component[], visitor: Visitor): void {
  components.forEach((component) => component.accept(visitor));
}

const components: Component[] = [new ConcreteComponentA(), new ConcreteComponentB()];
clientCode(components, new ConcreteVisitor1());
clientCode(components, new ConcreteVisitor2());
```

**Tradeoff:** New operations are easy; adding an element type requires changing every visitor.

References: [main article](https://refactoring.guru/design-patterns/visitor), [TypeScript example](https://refactoring.guru/design-patterns/visitor/typescript/example)
