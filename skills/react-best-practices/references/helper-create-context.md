# Hook-Backed Context Helper

Copy this shape when a feature needs a generated provider plus consumer hook.
Adapt names, imports, and provider placement to the target project.

## `src/shared/utils/create-context.tsx`

```tsx
import { type ReactNode, createContext as createReactContext, use } from "react";

type ProviderProps<TContextHook extends (...args: any[]) => unknown> =
	Parameters<TContextHook> extends []
		? { children: ReactNode }
		: NonNullable<Parameters<TContextHook>[0]> & { children: ReactNode };

export default function createContext<TContextHook extends (...args: any[]) => unknown>(
	contextHook: TContextHook
) {
	type ContextType = ReturnType<TContextHook>;
	const Context = createReactContext<ContextType | null>(null);

	function useContext() {
		const context = use(Context);
		if (context === null) {
			throw new Error("useContext must be used within Provider");
		}
		return context;
	}

	function Provider({ children, ...contextHookProps }: ProviderProps<TContextHook>) {
		const value =
			Object.keys(contextHookProps).length === 0
				? (contextHook as () => ContextType)()
				: (contextHook as (props: NonNullable<Parameters<TContextHook>[0]>) => ContextType)(
						contextHookProps as NonNullable<Parameters<TContextHook>[0]>
				  );

		return <Context value={value}>{children}</Context>;
	}

	return [Provider, useContext] as const;
}
```
