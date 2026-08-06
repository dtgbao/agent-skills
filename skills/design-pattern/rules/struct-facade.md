---
title: Use Facade for a Simple Subsystem Entry Point
impact: HIGH
impactDescription: "Popularity: 2/3; Complexity: 1/3"
tags: structural, facade, subsystem
---

## Use Facade for a Simple Subsystem Entry Point

Use Facade to expose common operations without making clients coordinate a complex subsystem.

**Incorrect (every client repeats orchestration):**

```typescript
codec.load(file);
mixer.normalize();
writer.encode(codec.frames(), mixer.track());
```

**Correct (facade owns the common workflow):**

```typescript
class VideoConverter {
  constructor(
    private codec: Codec,
    private writer: Writer,
  ) {}
  convert(file: File) {
    return this.writer.encode(this.codec.decode(file));
  }
}
```

**Tradeoff:** Reduces client coupling, but an oversized facade can become a god object.

References: [main article](https://refactoring.guru/design-patterns/facade), [TypeScript example](https://refactoring.guru/design-patterns/facade/typescript/example)
