# Code Smell Checklist

Use this checklist to identify a design pressure, not to declare code defective from a name alone. Confirm the smell in context, protect existing behavior, and choose the smallest treatment that addresses the demonstrated problem.

## Bloaters

- [ ] **Long Method**

  - **Signal:** A routine contains too many steps or responsibilities to understand without sustained tracing. Growth usually hides decisions, duplicates logic, and makes safe changes harder.
  - **Solutions:** [Extract Method](extract-method.md), [Replace Temp with Query](replace-temp-with-query.md), [Introduce Parameter Object](introduce-parameter-object.md), [Preserve Whole Object](preserve-whole-object.md), [Replace Method with Method Object](replace-method-with-method-object.md), [Decompose Conditional](decompose-conditional.md).

- [ ] **Large Class**

  - **Signal:** A class owns an excessive number of fields, methods, or unrelated responsibilities. Features accumulate in the convenient existing type until cohesion and ownership are unclear.
  - **Solutions:** [Extract Class](extract-class.md), [Extract Subclass](extract-subclass.md), [Extract Interface](extract-interface.md), [Duplicate Observed Data](duplicate-observed-data.md).

- [ ] **Primitive Obsession**

  - **Signal:** Primitives, strings, arrays, or codes stand in for domain concepts and rules. Validation and behavior then scatter across callers instead of living with the concept.
  - **Solutions:** [Replace Data Value with Object](replace-data-value-with-object.md), [Introduce Parameter Object](introduce-parameter-object.md), [Preserve Whole Object](preserve-whole-object.md), [Replace Type Code with Class](replace-type-code-with-class.md), [Replace Type Code with Subclasses](replace-type-code-with-subclasses.md), [Replace Type Code with State/Strategy](replace-type-code-with-state-strategy.md), [Replace Array with Object](replace-array-with-object.md).

- [ ] **Long Parameter List**

  - **Signal:** A method requires enough arguments that calls are difficult to read or construct correctly. The interface may be exposing another object's data or combining several behaviors.
  - **Solutions:** [Replace Parameter with Method Call](replace-parameter-with-method-call.md), [Preserve Whole Object](preserve-whole-object.md), [Introduce Parameter Object](introduce-parameter-object.md).

- [ ] **Data Clumps**

  - **Signal:** The same group of values repeatedly appears together in fields, parameters, or local variables. The repeated group often represents a missing domain concept.
  - **Solutions:** [Extract Class](extract-class.md), [Introduce Parameter Object](introduce-parameter-object.md), [Preserve Whole Object](preserve-whole-object.md).

## Object-Orientation Abusers

- [ ] **Alternative Classes with Different Interfaces**

  - **Signal:** Classes perform equivalent jobs through incompatible method names or signatures. Clients cannot substitute them and duplicate adaptation logic.
  - **Solutions:** [Rename Method](rename-method.md), [Move Method](move-method.md), [Add Parameter](add-parameter.md), [Parameterize Method](parameterize-method.md), [Extract Superclass](extract-superclass.md).

- [ ] **Refused Bequest**

  - **Signal:** A subclass inherits operations or data that it does not support or use. The hierarchy likely models code reuse rather than a valid subtype relationship.
  - **Solutions:** [Replace Inheritance with Delegation](replace-inheritance-with-delegation.md), [Extract Superclass](extract-superclass.md).

- [ ] **Switch Statements**

  - **Signal:** The same type- or mode-based branching recurs when behavior varies. Every new variant requires edits across several conditionals.
  - **Solutions:** [Extract Method](extract-method.md), [Move Method](move-method.md), [Replace Type Code with Subclasses](replace-type-code-with-subclasses.md), [Replace Type Code with State/Strategy](replace-type-code-with-state-strategy.md), [Replace Conditional with Polymorphism](replace-conditional-with-polymorphism.md), [Replace Parameter with Explicit Methods](replace-parameter-with-explicit-methods.md), [Introduce Null Object](introduce-null-object.md).

- [ ] **Temporary Field**

  - **Signal:** An object's field is meaningful only during a particular operation or mode. At other times the field is empty or misleading, weakening the object's invariant.
  - **Solutions:** [Extract Class](extract-class.md), [Replace Method with Method Object](replace-method-with-method-object.md), [Introduce Null Object](introduce-null-object.md).

## Change Preventers

- [ ] **Divergent Change**

  - **Signal:** One class changes for several unrelated kinds of requirement. Multiple responsibilities have collected behind one change boundary.
  - **Solutions:** [Extract Class](extract-class.md), [Extract Superclass](extract-superclass.md), [Extract Subclass](extract-subclass.md).

- [ ] **Parallel Inheritance Hierarchies**

  - **Signal:** Adding a subtype in one hierarchy forces a matching subtype elsewhere. The paired hierarchies encode one variation across two coupled structures.
  - **Solutions:** [Move Method](move-method.md), [Move Field](move-field.md).

- [ ] **Shotgun Surgery**

  - **Signal:** One conceptual change requires small edits across many classes or modules. Responsibility is scattered rather than localized behind one interface.
  - **Solutions:** [Move Method](move-method.md), [Move Field](move-field.md), [Inline Class](inline-class.md).

## Dispensables

- [ ] **Comments**

  - **Signal:** Comments repeatedly explain confusing code mechanics or compensate for unclear names. The underlying code may not express its intent; explanatory rationale and public documentation remain legitimate.
  - **Solutions:** [Extract Variable](extract-variable.md), [Extract Method](extract-method.md), [Rename Method](rename-method.md), [Introduce Assertion](introduce-assertion.md).

- [ ] **Duplicate Code**

  - **Signal:** Equivalent logic appears in more than one place. Fixes can drift because every copy must be found and changed consistently.
  - **Solutions:** [Extract Method](extract-method.md), [Pull Up Field](pull-up-field.md), [Pull Up Constructor Body](pull-up-constructor-body.md), [Form Template Method](form-template-method.md), [Substitute Algorithm](substitute-algorithm.md), [Extract Superclass](extract-superclass.md), [Extract Class](extract-class.md), [Consolidate Conditional Expression](consolidate-conditional-expression.md), [Consolidate Duplicate Conditional Fragments](consolidate-duplicate-conditional-fragments.md).

- [ ] **Data Class**

  - **Signal:** A class mainly exposes fields while behavior that uses those fields lives elsewhere. Ownership of invariants and operations has leaked to clients.
  - **Solutions:** [Encapsulate Field](encapsulate-field.md), [Encapsulate Collection](encapsulate-collection.md), [Move Method](move-method.md), [Extract Method](extract-method.md), [Remove Setting Method](remove-setting-method.md), [Hide Method](hide-method.md).

- [ ] **Dead Code**

  - **Signal:** Declarations, branches, parameters, or classes are no longer reachable or used. Obsolete code increases search space and creates false maintenance obligations.
  - **Solutions:** [Inline Class](inline-class.md), [Collapse Hierarchy](collapse-hierarchy.md), [Remove Parameter](remove-parameter.md).

- [ ] **Lazy Class**

  - **Signal:** A class contributes too little behavior or policy to justify its separate boundary. The abstraction may be a remnant of earlier design or speculative structure.
  - **Solutions:** [Inline Class](inline-class.md), [Collapse Hierarchy](collapse-hierarchy.md).

- [ ] **Speculative Generality**

  - **Signal:** Unused hooks, parameters, abstractions, or hierarchy levels exist for hypothetical future needs. The extra flexibility adds present cost without a current consumer.
  - **Solutions:** [Collapse Hierarchy](collapse-hierarchy.md), [Inline Class](inline-class.md), [Inline Method](inline-method.md), [Remove Parameter](remove-parameter.md).

## Couplers

- [ ] **Feature Envy**

  - **Signal:** A method reads or manipulates another object's data more than its own. The behavior may be located away from the responsibility and invariants it serves.
  - **Solutions:** [Move Method](move-method.md), [Extract Method](extract-method.md).

- [ ] **Inappropriate Intimacy**

  - **Signal:** Classes depend heavily on each other's private details or internal structure. Tight mutual knowledge makes independent change difficult.
  - **Solutions:** [Move Method](move-method.md), [Move Field](move-field.md), [Extract Class](extract-class.md), [Hide Delegate](hide-delegate.md), [Change Bidirectional Association to Unidirectional](change-bidirectional-association-to-unidirectional.md), [Replace Delegation with Inheritance](replace-delegation-with-inheritance.md).

- [ ] **Message Chains**

  - **Signal:** Clients traverse a long sequence of getters or collaborators to complete one task. Callers become coupled to the entire relationship graph.
  - **Solutions:** [Hide Delegate](hide-delegate.md), [Extract Method](extract-method.md), [Move Method](move-method.md).

- [ ] **Middle Man**

  - **Signal:** A class spends most of its interface forwarding calls without enforcing policy. The extra hop adds surface area but little encapsulation.
  - **Solutions:** [Remove Middle Man](remove-middle-man.md).

## Other Smells

- [ ] **Incomplete Library Class**

  - **Signal:** A closed library type lacks operations the application repeatedly needs. Client code accumulates scattered workarounds because the original type cannot be changed.
  - **Solutions:** [Introduce Foreign Method](introduce-foreign-method.md), [Introduce Local Extension](introduce-local-extension.md).
