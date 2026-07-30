---
title: Extract Reusable Interaction Behavior
impact: HIGH
impactDescription: keeps gesture and animation edge cases fixed once
tags: composition, motion, interaction, shared
---

## Extract Reusable Interaction Behavior

Keep tap-vs-drag handling, keyboard behavior, swipe thresholds, disclosure
state, and animation glue in reusable primitives. Feature components should
describe what an interaction means, not reimplement event math.

**Incorrect:**

```tsx
function InboxMessageCard({ onArchive }: Props) {
  const x = useMotionValue(0);

  return (
    <motion.div
      drag="x"
      onDragEnd={(_, info) => {
        if (Math.abs(info.offset.x) > 120) onArchive();
      }}
    />
  );
}
```

**Correct:**

```tsx
function InboxMessageCard({ children, onArchive }: Props) {
  return (
    <Swipeable onSwipeDismiss={onArchive}>
      <article>{children}</article>
    </Swipeable>
  );
}
```

If another feature needs the same interaction, reuse or extend the primitive
before adding a new wrapper.
