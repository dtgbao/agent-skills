---
title: Use Adapter to Translate an Incompatible Interface
impact: CRITICAL
impactDescription: "Popularity: 3/3; Complexity: 1/3"
tags: structural, adapter, integration
---

## Use Adapter to Translate an Incompatible Interface

Use Adapter to make a legacy or third-party object satisfy the interface expected by existing clients.

**Incorrect (translation leaks into every client):**

```typescript
const result = legacy.specificRequest().split("").reverse().join("");
```

**Correct (translate once at the boundary):**

```typescript
interface Target {
  request(): string;
}
class LegacyAdapter implements Target {
  constructor(private legacy: LegacyService) {}
  request() {
    return this.legacy.specificRequest().split("").reverse().join("");
  }
}
```

**Tradeoff:** Isolates conversion but adds a wrapper. Change the adaptee directly when you own it and compatibility is unnecessary.

References: [main article](https://refactoring.guru/design-patterns/adapter), [TypeScript example](https://refactoring.guru/design-patterns/adapter/typescript/example)
