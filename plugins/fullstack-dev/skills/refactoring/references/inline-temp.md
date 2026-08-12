# Inline Temp

**Category:** Composing Methods  

## Problem

A local variable merely aliases an expression and obstructs another refactoring.

## Refactoring

Replace uses of the temporary with the expression and delete the declaration.

## Why use it

Make local logic reveal its intent and reduce the amount of state a reader must track. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Do not duplicate expensive, nondeterministic, or side-effecting evaluation. Preserve evaluation order, side effects, exceptions, and the lifetime of local values.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Confirm the initializer is safe to evaluate at each use.
3. Replace references to the temporary.
4. Delete the declaration and verify evaluation count and order.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Helps other refactorings:** [Replace Temp with Query](replace-temp-with-query.md)
- **Helps other refactorings:** [Extract Method](extract-method.md)
