---
title: Derive State Without Effects
impact: HIGH
impactDescription: avoids cascading renders and keeps state updates at their source
tags: state, effects, rendering, events
---

## Derive State Without Effects

Use effects to synchronize with external systems. Place synchronous state updates at their source:

- Derive values from props or state during render.
- Update state in the event handler that caused the change.
- Read initial values with a lazy state initializer.
- Reset a subtree with a `key`; when only part of the state must adjust, update it conditionally during render as a last resort.

**Incorrect (storing derived data):**

```tsx
const [fullName, setFullName] = useState("");

useEffect(() => {
	setFullName(`${firstName} ${lastName}`);
}, [firstName, lastName]);
```

**Correct (derive during render):**

```tsx
const fullName = `${firstName} ${lastName}`;
```

**Incorrect (reacting to an event later):**

```tsx
function handleSubmit() {
	setIsSubmitted(true);
}

useEffect(() => {
	if (isSubmitted) {
		sendNotification();
	}
}, [isSubmitted]);
```

**Correct (handle the event at its source):**

```tsx
function handleSubmit() {
	setIsSubmitted(true);
	sendNotification();
}
```

**Incorrect (initializing after mount):**

```tsx
const [theme, setTheme] = useState("light");

useEffect(() => {
	const savedTheme = localStorage.getItem("theme");
	if (savedTheme) {
		setTheme(savedTheme);
	}
}, []);
```

**Correct (initialize lazily in client-only code):**

```tsx
const [theme] = useState(() => localStorage.getItem("theme") ?? "light");
```

For server-rendered UI, the initializer must be server-safe and produce matching initial HTML.

Prefer a keyed subtree when all of its state belongs to a different entity:

```tsx
<ProfileForm key={userId} userId={userId} />
```

Rare escape hatch: when neither derivation nor a keyed reset preserves the intended behavior, adjust only the current component's state during render:

```tsx
const [previousItems, setPreviousItems] = useState(items);
const [selection, setSelection] = useState<Item | null>(null);

if (items !== previousItems) {
	setPreviousItems(items);
	setSelection(null);
}
```

The condition must update its own comparison guard so it converges. Render-time setters may only target the component currently rendering. Prefer storing an item ID or deriving the selection when that removes the adjustment entirely.

State updates from asynchronous callbacks, subscriptions, or external-system synchronization may still belong in an effect. The target is the synchronous effect body that immediately calls a state setter and forces React to render twice.
