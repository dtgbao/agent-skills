# Replace Temp with Query

**Category:** Composing Methods  

## Problem

A local caches a calculation that other code would benefit from naming and reusing.

## Refactoring

Extract the calculation into a query and call that query instead of reading the temporary.

## Why use it

Make local logic reveal its intent and reduce the amount of state a reader must track. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Repeated queries can change performance or behavior when the calculation is expensive or impure. Preserve evaluation order, side effects, exceptions, and the lifetime of local values.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Make the temporary single-assignment and isolate its initializer.
3. Extract the initializer as a side-effect-free query.
4. Replace reads with calls, then remove the temporary.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Extract Method](extract-method.md)
