---
title: Use Bridge for Independent Dimensions
impact: MEDIUM
impactDescription: "Popularity: 1/3; Complexity: 3/3"
tags: structural, bridge, composition
---

## Use Bridge for Independent Dimensions

Use Bridge when two dimensions must evolve independently without creating a subclass for every combination.

**Incorrect (class explosion):**

```typescript
class UrgentEmailAlert {}
class UrgentSmsAlert {}
class DigestEmailAlert {}
```

**Correct (bridge abstraction to implementation):**

```typescript
interface Channel {
  send(message: string): void;
}
class Alert {
  constructor(private channel: Channel) {}
  send(message: string) {
    this.channel.send(message);
  }
}
```

**Tradeoff:** Prevents combinatorial inheritance but adds indirection; avoid it when the dimensions are not independently variable.

References: [main article](https://refactoring.guru/design-patterns/bridge), [TypeScript example](https://refactoring.guru/design-patterns/bridge/typescript/example)
