# Split Temporary Variable

**Category:** Composing Methods  

## Problem

One local variable represents unrelated values at different points in a routine.

## Refactoring

Give each independent use its own narrowly scoped variable.

## Why use it

Make local logic reveal its intent and reduce the amount of state a reader must track. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Do not split a genuine accumulator or loop variable whose changing value expresses one concept. Preserve evaluation order, side effects, exceptions, and the lifetime of local values.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Identify each distinct responsibility represented by the variable.
3. Create a separate name for every responsibility.
4. Replace assignments and reads in one lifetime at a time.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Inline Temp](inline-temp.md)
- **Similar refactorings:** [Extract Variable](extract-variable.md)
- **Similar refactorings:** [Remove Assignments to Parameters](remove-assignments-to-parameters.md)
- **Helps other refactorings:** [Extract Method](extract-method.md)
