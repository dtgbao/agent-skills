# Substitute Algorithm

**Category:** Composing Methods  

## Problem

An implementation is harder to understand or maintain than an available equivalent algorithm.

## Refactoring

Replace the body with the simpler algorithm while retaining the same observable contract.

## Why use it

Make local logic reveal its intent and reduce the amount of state a reader must track. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Equivalent-looking algorithms can differ on ordering, stability, precision, errors, and boundary cases. Preserve evaluation order, side effects, exceptions, and the lifetime of local values.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Capture representative, boundary, and failure cases before changing the algorithm.
3. Prepare inputs and outputs so the replacement fits the existing contract.
4. Replace the body as one reviewable change and compare results.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- No directly linked catalog technique.
