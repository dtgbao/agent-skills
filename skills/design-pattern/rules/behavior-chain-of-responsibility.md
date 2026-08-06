---
title: Use Chain of Responsibility for Ordered Handlers
impact: HIGH
impactDescription: "Popularity: 2/3; Complexity: 2/3"
tags: behavioral, chain-of-responsibility, handlers
---

## Use Chain of Responsibility for Ordered Handlers

Use a handler chain when several receivers may process a request and their order or membership varies.

**Incorrect (one rigid conditional dispatcher):**

```typescript
if (kind === "auth") authenticate(req);
else if (kind === "cache") cache(req);
```

**Correct (handlers forward or stop):**

```typescript
interface Handler {
  setNext(next: Handler): Handler;
  handle(request: Request): Result | undefined;
}
abstract class BaseHandler implements Handler {
  private next?: Handler;
  setNext(next: Handler) {
    this.next = next;
    return next;
  }
  handle(request: Request) {
    return this.next?.handle(request);
  }
}
```

**Tradeoff:** Reorders handlers easily, but a request may go unhandled unless the terminal behavior is explicit.

References: [main article](https://refactoring.guru/design-patterns/chain-of-responsibility), [TypeScript example](https://refactoring.guru/design-patterns/chain-of-responsibility/typescript/example)
