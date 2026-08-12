# Inline Method

**Category:** Composing Methods  

## Problem

A tiny helper adds indirection without contributing a useful name or abstraction.

## Refactoring

Replace each call with the helper body, then remove the helper.

## Why use it

Make local logic reveal its intent and reduce the amount of state a reader must track. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Do not inline polymorphic, recursive, or widely reused behavior merely to reduce the method count. Preserve evaluation order, side effects, exceptions, and the lifetime of local values.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Confirm the method is not overridden and that its body is safe at every call site.
3. Substitute the body one caller at a time.
4. Remove the method only after no references remain.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Extract Method](extract-method.md)
