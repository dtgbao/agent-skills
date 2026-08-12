# Replace Error Code with Exception

**Category:** Simplifying Method Calls  

## Problem

A method reports failure through a code that callers can ignore or misinterpret.

## Refactoring

Raise a typed exception and handle it at the appropriate boundary.

## Why use it

Make an interface communicate what callers provide, receive, and may observe. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Exceptions change control flow and public contracts; reserve them for exceptional failure rather than expected alternatives. Treat public callers, overrides, reflection, and serialized contracts as compatibility constraints.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Map each failure code to a clear exception contract.
3. Update callers to handle or propagate failures.
4. Replace code returns one path at a time and remove obsolete checks.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- No directly linked catalog technique.
