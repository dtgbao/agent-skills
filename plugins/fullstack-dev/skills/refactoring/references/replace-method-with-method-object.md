# Replace Method with Method Object

**Category:** Composing Methods  

## Problem

A long routine depends on many intertwined locals, making ordinary extraction awkward.

## Refactoring

Turn the routine into an object whose fields hold the former local state, then split its work into methods.

## Why use it

Make local logic reveal its intent and reduce the amount of state a reader must track. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

The extra object is justified only when it enables meaningful decomposition; otherwise it is ceremony. Preserve evaluation order, side effects, exceptions, and the lifetime of local values.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Create a method-object type with fields for inputs and changing local state.
3. Move the original body into an execution method.
4. Extract coherent steps into private methods, then delegate from the original routine.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Replace Data Value with Object](replace-data-value-with-object.md)
