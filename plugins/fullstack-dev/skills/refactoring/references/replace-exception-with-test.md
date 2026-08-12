# Replace Exception with Test

**Category:** Simplifying Method Calls  

## Problem

Expected conditions are detected by throwing and catching an exception.

## Refactoring

Check the condition explicitly before performing the operation.

## Why use it

Make an interface communicate what callers provide, receive, and may observe. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Keep the exception when a precheck introduces a time-of-check/time-of-use race or duplicates the operation's authority. Treat public callers, overrides, reflection, and serialized contracts as compatibility constraints.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Identify the predictable condition represented by the exception.
3. Add a side-effect-free query or guard.
4. Use the guarded path and retain handling for genuinely exceptional races or failures.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Similar refactorings:** [Replace Error Code with Exception](replace-error-code-with-exception.md)
