# Extract Method

**Category:** Composing Methods  

## Problem

A coherent block is buried inside a larger routine, so its purpose is difficult to see.

## Refactoring

Move the block into a well-named function and replace the original block with a call.

## Why use it

Make local logic reveal its intent and reduce the amount of state a reader must track. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Avoid an extraction whose parameter and return-value plumbing is harder to understand than the original block. Preserve evaluation order, side effects, exceptions, and the lifetime of local values.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Choose one responsibility and name it by intent.
3. Identify inputs, outputs, and locally mutated values.
4. Create the function, replace the block with a call, and test the caller.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Inline Method](inline-method.md)
- **Similar refactorings:** [Move Method](move-method.md)
- **Helps other refactorings:** [Introduce Parameter Object](introduce-parameter-object.md)
- **Helps other refactorings:** [Form Template Method](form-template-method.md)
- **Helps other refactorings:** [Parameterize Method](parameterize-method.md)
