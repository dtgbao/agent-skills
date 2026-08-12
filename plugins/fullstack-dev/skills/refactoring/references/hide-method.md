# Hide Method

**Category:** Simplifying Method Calls  

## Problem

A method is public even though only its declaring class or package uses it.

## Refactoring

Reduce its visibility to the narrowest level required.

## Why use it

Make an interface communicate what callers provide, receive, and may observe. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Search external consumers, reflection, templates, serializers, and framework hooks before restricting access. Treat public callers, overrides, reflection, and serialized contracts as compatibility constraints.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Locate every static and dynamic use.
3. Reduce visibility one level at a time if needed.
4. Run integration checks that cover framework-driven invocation.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- No directly linked catalog technique.
