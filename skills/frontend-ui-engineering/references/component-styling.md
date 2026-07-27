# Component Styling

## Styling Ladder

Before editing styles, locate the project theme entry point, the UI library's supported customization APIs, the component's canonical style or variant definition, and matching usages. Walk the ladder in order; lower rungs may compose higher ones:

1. **Theme and semantic tokens for system decisions.**
   - Put broad brand customization in one project-owned theme layer. Map the UI library's public token contract when present.
   - Prefer existing semantic tokens in components. Keep primitive values in theme definitions and map them to roles such as `surface`, `foreground`, `accent`, and `border`.
   - Inspect a token's consumers before changing it. Change the value only when every consumer should inherit the result; otherwise add the narrowest semantic token or component variant.
   - Add a token only for a stable role reused across themes or a component family. Define or map it in every supported theme and verify foreground/background contrast.
2. **Variants for component decisions.**
   - Add a variant for a required named mode or a treatment reused by the component. Define it once in the canonical component recipe, compose it from semantic tokens, and set defaults there.
   - Keep axes such as `tone`, `size`, and `state` independent. Add a compound variant only when a specific combination needs extra styling.
   - Migrate matching uses within the requested component or feature. Report matches outside that scope.
3. **Local styles for one-off consumer layout.**
   - Keep placement and surrounding layout local, including width, margin, grid position, and responsive visibility.
   - Keep intrinsic appearance—color, radius, internal spacing, states, and shadows—in tokens or variants.

## Convention Mapping

Use the project's established convention. When none exists:

- UI library: use its public theme, token, slot, and variant APIs. When none fits, keep the narrow override beside a project-owned adapter component.
- CSS or Sass with a shared selector namespace: use BEM modifiers.
- Scoped CSS: use the framework or module's native naming.
- Utility classes: reuse an installed `cva` or `tailwind-variants`. For the first simple variant, a component-owned modifier is enough; propose a dependency when demonstrated reuse or complexity warrants it.

## Token-Backed Variant Examples

```css
/* CSS/Sass with BEM */
.button {
	background: var(--accent);
	color: var(--accent-foreground);
}

.button--danger {
	background: var(--danger);
	color: var(--danger-foreground);
}
```

```tsx
import { tv } from "tailwind-variants";

const button = tv({
	base: "rounded-control font-medium",
	variants: {
		tone: {
			primary: "bg-accent text-accent-foreground",
			danger: "bg-danger text-danger-foreground",
		},
	},
	defaultVariants: { tone: "primary" },
});
```

## Completion Checks

- [ ] Each styling decision sits at the highest applicable ladder rung and follows the project's established convention.
- [ ] Modified tokens and variants render correctly in every affected theme and interaction state.
- [ ] Matching style recipes within the touched scope use the canonical variant.
