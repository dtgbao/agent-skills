# Hook-Backed Context Helper

Copy this shape when a feature needs a generated provider plus consumer hook.
Adapt names, imports, and provider placement to the target project.

```tsx
//create-context.tsx
import {
	type ReactNode,
	createContext as createReactContext,
	useContext as useReactContext,
} from "react";

type ProviderProps<TContextHook extends (...args: any[]) => unknown> =
	Parameters<TContextHook> extends []
		? { children: ReactNode }
		: NonNullable<Parameters<TContextHook>[0]> & { children: ReactNode };

export default function createContext<TContextHook extends (...args: any[]) => unknown>(
	contextHook: TContextHook,
) {
	type ContextType = ReturnType<TContextHook>;
	const Context = createReactContext<ContextType | null>(null);

	function useContext() {
		const context = useReactContext(Context);
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
						contextHookProps as NonNullable<Parameters<TContextHook>[0]>,
					);

		return <Context.Provider value={value}>{children}</Context.Provider>;
	}

	return [Provider, useContext] as const;
}

// ThemeContext.tsx
import { useState } from "react";

export const useTheme = () => {
	const [theme, setTheme] = useState<"light" | "dark">("dark");

	const toggle = () => setTheme((current) => (current === "dark" ? "light" : "dark"));

	return {
		theme,
		toggle,
	};
};

export const [ThemeContext, useThemeContext] = createContext(useTheme);
```
