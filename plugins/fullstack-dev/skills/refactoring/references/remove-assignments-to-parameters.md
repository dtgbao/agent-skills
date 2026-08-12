# Remove Assignments to Parameters

**Category:** Composing Methods  

## Problem

A routine overwrites an input parameter, obscuring the value supplied by its caller.

## Refactoring

Keep the parameter unchanged and store derived or updated values in a local variable.

## Why use it

Make local logic reveal its intent and reduce the amount of state a reader must track. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Reference and alias semantics may make reassignment different from mutating the referenced object. Preserve evaluation order, side effects, exceptions, and the lifetime of local values.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Create a local initialized from the parameter when an updated value is needed.
3. Redirect assignments and subsequent reads to the local.
4. Verify callers still observe the same mutations and results.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Split Temporary Variable](split-temporary-variable.md)
- **Helps other refactorings:** [Extract Method](extract-method.md)
