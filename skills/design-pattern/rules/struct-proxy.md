---
title: Use Proxy to Control Access Transparently
impact: MEDIUM
impactDescription: "Popularity: 1/3; Complexity: 2/3"
tags: structural, proxy, access-control
---

## Use Proxy to Control Access Transparently

Use Proxy when a stand-in must preserve a service interface while controlling access, caching, logging, remoting, or lazy initialization.

**Incorrect (cross-cutting access logic in every client):**

```typescript
if (user.allowed) {
  audit.log();
  service.request();
}
```

**Correct (proxy remains substitutable):**

```typescript
interface Subject {
  request(): void;
}
class GuardedSubject implements Subject {
  constructor(
    private real: Subject,
    private allowed: () => boolean,
  ) {}
  request() {
    if (this.allowed()) this.real.request();
  }
}
```

**Tradeoff:** Controls a service transparently but adds latency and another lifecycle layer.

References: [main article](https://refactoring.guru/design-patterns/proxy), [TypeScript example](https://refactoring.guru/design-patterns/proxy/typescript/example)
