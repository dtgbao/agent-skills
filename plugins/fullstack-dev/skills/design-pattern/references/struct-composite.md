---
title: Use Composite for Uniform Object Trees
impact: HIGH
impactDescription: "Popularity: 2/3; Complexity: 2/3"
tags: structural, composite, trees
---

## Use Composite for Uniform Object Trees

Use Composite when leaves and containers form a tree and clients should treat both through one contract.

**Incorrect (clients branch on node shape):**

```typescript
function clientCode(component: Leaf | Composite): string {
  if (component instanceof Leaf) return `Leaf result: ${component.operation()}`;
  return `Composite result: ${component.operation()}`;
}
```

**Correct (leaves and composites share a component hierarchy):**

```typescript
abstract class Component {
  protected parent: Component | null = null;

  setParent(parent: Component | null): void {
    this.parent = parent;
  }

  add(_component: Component): void {}
  remove(_component: Component): void {}
  isComposite(): boolean {
    return false;
  }
  abstract operation(): string;
}

class Leaf extends Component {
  operation(): string {
    return "Leaf";
  }
}

class Composite extends Component {
  private readonly children: Component[] = [];

  add(component: Component): void {
    this.children.push(component);
    component.setParent(this);
  }

  remove(component: Component): void {
    const index = this.children.indexOf(component);
    if (index !== -1) {
      this.children.splice(index, 1);
      component.setParent(null);
    }
  }

  isComposite(): boolean {
    return true;
  }

  operation(): string {
    return `Branch(${this.children.map((child) => child.operation()).join("+")})`;
  }
}

function clientCode(component: Component): string {
  return component.operation();
}

const tree = new Composite();
tree.add(new Leaf());
tree.add(new Leaf());
clientCode(tree);
```

**Tradeoff:** Simplifies recursive clients but can force unrelated leaves into an overly broad interface.

References: [main article](https://refactoring.guru/design-patterns/composite), [TypeScript example](https://refactoring.guru/design-patterns/composite/typescript/example)
