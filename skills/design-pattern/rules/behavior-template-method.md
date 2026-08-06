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
class CsvImport {
  run() {
    /* parse, validate, save */
  }
}
class JsonImport {
  run() {
    /* same flow */
  }
}
```

**Correct (base class fixes the sequence):**

```typescript
abstract class Importer {
  run(raw: string) {
    const rows = this.parse(raw);
    this.validate(rows);
    return this.save(rows);
  }
  protected abstract parse(raw: string): Row[];
  protected validate(rows: Row[]) {
    if (!rows.length) throw new Error("empty");
  }
  protected abstract save(rows: Row[]): number;
}
```

**Tradeoff:** Removes workflow duplication, but inheritance fixes variation at class level and may constrain subclasses.

References: [main article](https://refactoring.guru/design-patterns/template-method), [TypeScript example](https://refactoring.guru/design-patterns/template-method/typescript/example)
