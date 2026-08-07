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
function clientCode(realSubject: RealSubject): void {
  if (checkAccess()) {
    realSubject.request();
    logAccess();
  }
}
```

**Correct (proxy and real subject expose the same contract):**

```typescript
interface Subject {
  request(): void;
}

class RealSubject implements Subject {
  request(): void {
    console.log("RealSubject handling request");
  }
}

class Proxy implements Subject {
  constructor(private readonly realSubject: RealSubject) {}

  request(): void {
    if (this.checkAccess()) {
      this.realSubject.request();
      this.logAccess();
    }
  }

  private checkAccess(): boolean {
    return true;
  }

  private logAccess(): void {
    console.log("Proxy logged request time");
  }
}

function clientCode(subject: Subject): void {
  subject.request();
}

clientCode(new Proxy(new RealSubject()));
```

**Tradeoff:** Controls a service transparently but adds latency and another lifecycle layer.

References: [main article](https://refactoring.guru/design-patterns/proxy), [TypeScript example](https://refactoring.guru/design-patterns/proxy/typescript/example)
