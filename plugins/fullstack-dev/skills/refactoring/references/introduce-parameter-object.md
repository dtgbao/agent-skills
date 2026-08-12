# Introduce Parameter Object

**Category:** Simplifying Method Calls  

## Problem

The same group of parameters travels together across multiple interfaces.

## Refactoring

Represent the group with a named parameter object.

## Why use it

Make an interface communicate what callers provide, receive, and may observe. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Create the object only when the values form a durable concept, not merely to shorten one signature. Treat public callers, overrides, reflection, and serialized contracts as compatibility constraints.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Identify the invariant group and define its meaning.
3. Create an immutable value or parameter type.
4. Migrate one method and caller chain at a time, then move group-specific behavior into the type when useful.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Preserve Whole Object](preserve-whole-object.md)
