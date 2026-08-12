# Extract Variable

**Category:** Composing Methods  

## Problem

A compound expression forces readers to decode several ideas at once.

## Refactoring

Assign meaningful parts of the expression to named local values.

## Why use it

Make local logic reveal its intent and reduce the amount of state a reader must track. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

A weak name or a mutable temporary can make the expression less clear rather than more clear. Preserve evaluation order, side effects, exceptions, and the lifetime of local values.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Select the subexpression that represents one concept.
3. Introduce a name that describes its meaning, not its mechanics.
4. Replace the subexpression and repeat only while clarity improves.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Inline Temp](inline-temp.md)
- **Similar refactorings:** [Extract Method](extract-method.md)
