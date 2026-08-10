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
function clientCode(request: string): string | undefined {
  if (request === "Banana") return "Monkey handled Banana";
  if (request === "Nut") return "Squirrel handled Nut";
  if (request === "MeatBall") return "Dog handled MeatBall";
}
```

**Correct (concrete handlers process or forward through a configurable chain):**

```typescript
interface Handler<Request = string, Result = string> {
  setNext(handler: Handler<Request, Result>): Handler<Request, Result>;
  handle(request: Request): Result | undefined;
}

abstract class AbstractHandler implements Handler {
  private nextHandler?: Handler;

  setNext(handler: Handler): Handler {
    this.nextHandler = handler;
    return handler;
  }

  handle(request: string): string | undefined {
    return this.nextHandler?.handle(request);
  }
}

class MonkeyHandler extends AbstractHandler {
  handle(request: string): string | undefined {
    return request === "Banana" ? "Monkey handled Banana" : super.handle(request);
  }
}

class SquirrelHandler extends AbstractHandler {
  handle(request: string): string | undefined {
    return request === "Nut" ? "Squirrel handled Nut" : super.handle(request);
  }
}

class DogHandler extends AbstractHandler {
  handle(request: string): string | undefined {
    return request === "MeatBall" ? "Dog handled MeatBall" : super.handle(request);
  }
}

function clientCode(handler: Handler, requests: string[]): Array<string | undefined> {
  return requests.map((request) => handler.handle(request));
}

const monkey = new MonkeyHandler();
const squirrel = new SquirrelHandler();
const dog = new DogHandler();
monkey.setNext(squirrel).setNext(dog);
clientCode(monkey, ["Nut", "Banana", "Cup of coffee"]);
```

**Tradeoff:** Reorders handlers easily, but a request may go unhandled unless the terminal behavior is explicit.

References: [main article](https://refactoring.guru/design-patterns/chain-of-responsibility), [TypeScript example](https://refactoring.guru/design-patterns/chain-of-responsibility/typescript/example)
