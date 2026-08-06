---
title: Use Mediator to Centralize Component Collaboration
impact: LOW
impactDescription: "Popularity: 0/3; Complexity: 2/3"
tags: behavioral, mediator, coupling
---

## Use Mediator to Centralize Component Collaboration

Use Mediator when peer components are tightly coupled and their collaboration rules should live in one object.

**Incorrect (components call each other directly):**

```typescript
button.form.dialog.analytics.trackAndSubmit();
```

**Correct (components notify a mediator):**

```typescript
interface Mediator {
  notify(sender: object, event: string): void;
}
class DialogMediator implements Mediator {
  constructor(
    private form: Form,
    private dialog: Dialog,
  ) {}
  notify(_: object, event: string) {
    if (event === "submit") this.dialog.close(this.form.value());
  }
}
```

**Tradeoff:** Reduces peer coupling, but a mediator can accumulate too many unrelated rules.

References: [main article](https://refactoring.guru/design-patterns/mediator), [TypeScript example](https://refactoring.guru/design-patterns/mediator/typescript/example)
