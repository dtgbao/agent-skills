# Remove Setting Method

**Category:** Simplifying Method Calls  

## Problem

A field should not change after construction, yet the public interface exposes a setter.

## Refactoring

Initialize the field during construction and remove the setting operation.

## Why use it

Make an interface communicate what callers provide, receive, and may observe. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Account for serializers, ORMs, dependency injection, and staged builders that may require controlled initialization. Treat public callers, overrides, reflection, and serialized contracts as compatibility constraints.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Find all setter calls and distinguish initialization from mutation.
3. Move initialization into a constructor, factory, or builder.
4. Remove the setter after no supported mutation remains.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Helps other refactorings:** [Change Reference to Value](change-reference-to-value.md)
