# Architecture Design

Produce a comprehensive, actionable architecture blueprint grounded in the existing codebase.

## Core Process

### 1. Analyze Codebase Patterns

Identify the technology stack, module boundaries, abstractions, repository guidelines, and relevant architectural decisions. Trace similar features and cite evidence with file and line references.

### 2. Compare Three Approaches

Develop three viable approaches:

- **Minimal change:** smallest change with maximum reuse.
- **Clean architecture:** strongest boundaries and maintainability.
- **Pragmatic balance:** best trade-off between delivery speed and quality.

For each, describe the design, affected surface, benefits, trade-offs, and risks. Recommend one approach with evidence-backed reasoning. Do not stop at the comparison.

### 3. Build Three Blueprints

Build a complete, implementation-ready blueprint for each approach. For each blueprint, specify every file to create or modify, component responsibilities, interfaces, integration points, data flow, and test strategy. Break implementation into clear phases with concrete tasks.

Use diagrams only when they clarify a nontrivial relationship or flow. Avoid speculative files and abstractions.

## Output Guidance

Include:

- **Patterns & Conventions Found**: Existing patterns with file:line references, similar features, key abstractions
- **Approach Comparison**: The design, affected surface, benefits, trade-offs, and risks of all three approaches
- **Recommendation**: The selected approach with evidence-backed reasoning
- **Three Blueprints**: A separate complete blueprint for each approach, each containing:
  - **Component Design**: Each component with file path, hierarchy, responsibilities, dependencies, and interfaces
  - **Implementation Map**: Specific files to create/modify with detailed change descriptions
  - **Data Flow**: Complete flow from entry points through transformations to outputs
  - **Build Sequence**: Phased implementation steps as a checklist
  - **Critical Details**: Error handling, state management, testing, performance, and security considerations

Be specific and actionable: provide file paths, function names, and concrete steps.

Complete the design when all three approaches are concrete, comparable, and independently implementable without inventing unresolved decisions, and the recommendation is evidence-backed.
