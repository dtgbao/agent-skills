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
const button = new WindowsButton();
const checkbox = new MacCheckbox();
```

**Correct (one factory guarantees a compatible family):**

```typescript
interface UiFactory {
  button(): Button;
  checkbox(): Checkbox;
}
class MacUiFactory implements UiFactory {
  button() {
    return new MacButton();
  }
  checkbox() {
    return new MacCheckbox();
  }
}
function render(factory: UiFactory) {
  factory.button().paint();
  factory.checkbox().paint();
}
```

**Tradeoff:** Adding a family is easy; adding a new product kind changes every factory.

References: [main article](https://refactoring.guru/design-patterns/abstract-factory), [TypeScript example](https://refactoring.guru/design-patterns/abstract-factory/typescript/example)
