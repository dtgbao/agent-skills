---
title: React 19 API Changes
impact: MEDIUM
impactDescription: cleaner component definitions and context usage
tags: react19, refs, context, hooks
---

## React 19 API Changes

> **React 19+ only.** Skip this if you're on React 18 or earlier.

In React 19, `ref` is now a regular prop, so no `forwardRef` wrapper is needed for new components. Prefer `use(Context)` in React 19 code, especially when conditional reads help.

**Incorrect (forwardRef in React 19):**

```tsx
const ComposerInput = forwardRef<TextInput, Props>((props, ref) => {
	return <TextInput ref={ref} {...props} />;
});
```

**Correct (ref as a regular prop):**

```tsx
function ComposerInput({ ref, ...props }: Props & { ref?: React.Ref<TextInput> }) {
	return <TextInput ref={ref} {...props} />;
}
```

**Older context read:**

```tsx
const value = useContext(MyContext);
```

**React 19 context read:**

```tsx
const value = use(MyContext);
```

`use()` can also be called conditionally, unlike `useContext()`.
