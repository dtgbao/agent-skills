# Hide Delegate

**Category:** Moving Features between Objects  

## Problem

Clients navigate through an object to reach one of its collaborators, coupling them to the relationship.

## Refactoring

Expose the required operation on the owning object and delegate internally.

## Why use it

Put behavior and data with the object that owns the relevant responsibility. Apply it only to a demonstrated design pressure, not to prepare for a hypothetical requirement.

## Apply carefully

Too many forwarding methods can turn the owner into a middle man with an inflated interface. Check visibility, dependency direction, object ownership, and every existing caller.

## Procedure

1. Lock current behavior with focused tests or characterization checks.
2. Find the smallest operation clients actually need.
3. Add that operation to the owner and delegate to the collaborator.
4. Update clients and hide direct collaborator access where appropriate.
5. Run the focused checks after each safe step, then run the broader relevant suite.

## Related techniques

- **Anti-refactoring:** [Remove Middle Man](remove-middle-man.md)
