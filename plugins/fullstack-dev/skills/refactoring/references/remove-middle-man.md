# Remove Middle Man

**Category:** Moving Features between Objects  

## Problem

A class contributes little beyond forwarding a large part of another object's interface.

## Refactoring

Let appropriate clients use the underlying collaborator directly.

## Why use it

Put behavior and data with the object that owns the relevant responsibility. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Direct access increases coupling, so retain delegation when it protects a meaningful boundary or policy. Check visibility, dependency direction, object ownership, and every existing caller.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Identify forwarding methods with no added invariant or behavior.
3. Expose or inject the collaborator through a deliberate interface.
4. Move callers gradually and remove obsolete forwarding methods.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Hide Delegate](hide-delegate.md)
