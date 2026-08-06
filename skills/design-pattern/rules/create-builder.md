---
title: Use Builder for Step-by-Step Construction
impact: CRITICAL
impactDescription: "Popularity: 3/3; Complexity: 2/3"
tags: creational, builder, construction
---

## Use Builder for Step-by-Step Construction

Use Builder when a complex product has optional or ordered construction steps, or when the same process must produce different representations.

**Incorrect (telescoping constructor):**

```typescript
const report = new Report(title, rows, true, false, "pdf", undefined, logo);
```

**Correct (name and compose required steps):**

```typescript
class ReportBuilder {
  private sections: Section[] = [];
  addTable(rows: Row[]) {
    this.sections.push({ kind: "table", rows });
    return this;
  }
  addSummary(text: string) {
    this.sections.push({ kind: "summary", text });
    return this;
  }
  build() {
    return new Report([...this.sections]);
  }
}
```

**Tradeoff:** Construction becomes readable and reusable but introduces another type and mutable build state.

References: [main article](https://refactoring.guru/design-patterns/builder), [TypeScript example](https://refactoring.guru/design-patterns/builder/typescript/example)
