# Replace Parameter with Method Call

**Category:** Simplifying Method Calls  

## Problem

A caller passes a value the receiving object can reliably compute itself.

## Refactoring

Let the receiver obtain the value and remove the parameter.

## Why use it

Make an interface communicate what callers provide, receive, and may observe. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

This can hide an expensive lookup or make dependencies less explicit, so preserve testability and performance. Treat public callers, overrides, reflection, and serialized contracts as compatibility constraints.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Identify a stable query available to the receiver.
3. Replace parameter reads with the query.
4. Update callers and remove calculations used only for the argument.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- No directly linked catalog technique.
