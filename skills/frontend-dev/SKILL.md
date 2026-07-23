---
name: frontend-dev
description: Frontend architecture and scaffolding for framework-agnostic web development. Use when starting a frontend project, choosing its framework or architecture/tooling stack, or entering an existing frontend codebase whose structure, UI, styling, state, quality gates, or test strategy must be understood before implementation.
---

# Frontend Development

Run architecture choices as sequential decision gates. Research the current gate, recommend the smallest fitting option, record the user's choice, and only then open the next gate.

## Operating contract

1. Determine whether the work is greenfield or in an existing project and whether the user wants a plan, a scaffold, or implementation.
2. Inspect repository instructions and existing code before asking questions. Reuse established choices and ask only about decisions that remain open.
3. Work through one gate at a time because later recommendations depend on earlier choices.
4. Apply the source gate and present a decision card at every open technology gate.
5. Treat “use your judgment” as permission to choose the recommendation and record it. Otherwise, wait for the user's choice.
6. Begin file writes and dependency installation only after the user approves the consolidated blueprint.

For a capability with no demonstrated need, recommend **none** as an option. Prefer an existing project pattern, the standard library, an installed dependency, or a native platform feature before proposing new code or packages.

## Source gate

Complete these actions for every decision gate:

1. Inspect the descriptions of repository-local and available global skills. Load each directly relevant skill when repository instructions permit it; otherwise identify the skill and ask for explicit invocation.
2. Research the current official documentation for the viable candidates. Use an available technical web-research skill such as `$web-search`; otherwise search and open the official sources directly.
3. Verify current release status, framework/version compatibility, setup commands, and consequential limitations. Prefer official documentation, specifications, release notes, and maintainer repositories.
4. Cite only the supporting `$skill-name` actually loaded and sources actually opened. Treat `$frontend-dev` as procedure rather than evidence. State `Relevant skill: none found` when the skill search has no match.

Research only the current gate. If current web access is unavailable, disclose that limit and ask whether to proceed with repository and skill evidence alone.

**Complete the source gate when:** every material recommendation and compatibility claim in the decision card is traceable to an inspected skill or opened primary source.

## Decision card

Present each gate in this compact shape:

- **Recommendation:** the option that best fits the known constraints and why.
- **Options:** two or three viable choices, each with `Use when` and its material tradeoff. Include `none` when it is viable.
- **Evidence:** exact skill names and official documentation links, with version or freshness context when it affects the decision.
- **Question:** one explicit choice that closes the gate.

Eliminate candidates that conflict with an accepted choice or stated constraint. End the turn at the question and continue downstream planning after the user answers.

## Greenfield gates

### 0. Establish decision drivers

Treat this as intake rather than a technology decision. Summarize the known drivers, then ask one compact question covering only missing constraints that could change the framework recommendation: product shape, rendering and SEO needs, deployment target, browser targets, accessibility bar, team experience, expected scale, backend boundary, and package-manager preference.

Record a default only when the user explicitly delegates that constraint. Begin web and skill research at the first technology decision after intake.

**Complete this gate when:** every constraint that could materially change the framework choice is known or explicitly delegated.

### 1. Choose the framework

Research and compare two or three context-fit options. Include the native web platform without a framework when the product does not justify one. Explain implications for rendering, routing, data loading, deployment, ecosystem maturity, and team fit.

**Complete this gate when:** one framework and its current supported setup path are selected.

### 2. Choose the folder structure

Base every proposed tree on the selected framework's routing, build, and colocation conventions. Show two or three concrete trees spanning only plausible scale horizons, such as:

- route-first or framework-conventional for a small-to-medium app
- feature-first vertical slices for a medium or growing app
- domain or package boundaries for a genuinely large app

For each tree, show where routes, feature UI, shared UI, domain logic, data access, assets, and tests live. Define what may cross a boundary and where new files go. Recommend the least structure that fits the demonstrated horizon.

**Complete this gate when:** the user selects a concrete tree and the placement rules cover every planned code category.

### 3. Choose the UI library

Research libraries compatible with the selected framework and compare only relevant models: native elements, headless primitives, copy-owned components, or a styled component suite. Evaluate accessibility behavior, ownership and customization, styling integration, server-rendering support, bundle impact, and design-system maturity.

**Complete this gate when:** one UI strategy is selected, including `none`, and its ownership model is explicit.

### 4. Choose styling and conventions

Start with the selected UI library's supported styling path. Compare current, compatible choices such as Tailwind CSS, CSS Modules, Sass/SCSS, native scoped CSS, or the library's styling system.

Pair the system with only the convention it needs:

- Use BEM when a shared selector namespace needs predictable block and modifier names.
- Use Class Variance Authority (`cva`) or `tailwind-variants` (`tv`) when class-based components need typed variants; choose one.
- Use framework-native scoping and naming when it already solves isolation.

Explain tokens, responsive rules, class composition, variants, and component override policy.

**Complete this gate when:** the styling system, variant strategy, naming convention, and UI-library interaction are selected without overlapping tools.

### 5. Choose state and component architecture

Classify state before choosing a library:

- local interaction state
- URL and navigation state
- remote server/cache state
- form state
- cross-tree client state

Keep state at the narrowest owner. Research external libraries only for categories the framework and accepted stack do not cover. Compare context-fit options such as TanStack Query, Zustand, Redux Toolkit, or Jotai only after verifying current framework support and demonstrating the need.

Define how modules separate business logic from presentation through framework-native hooks, composables, services, stores, or equivalent boundaries. Use composition and compound components for cohesive reusable APIs; keep domain behavior outside generic UI primitives.

**Complete this gate when:** every state category has an owner and the component/module boundaries have a concrete rule.

### 6. Choose formatting, linting, and type checking

Inspect the framework generator's current defaults before adding tools. Research a minimal, non-overlapping combination from relevant candidates such as Oxc, Biome, ESLint, Prettier, and the framework's type checker.

Define exact package scripts for:

- a read-only `check` suitable for agents and CI
- a mutating `fix`
- `typecheck`
- any separate format check only when `check` does not cover it

Show the exact package-manager commands and CI order. Ensure read-only commands return a nonzero exit code on violations.

**Complete this gate when:** each concern has one owner and the proposed local and CI commands are explicit.

### 7. Choose the test strategy

Choose tests from product risk:

- Default to Vitest for unit and integration tests in a compatible greenfield project.
- Use Jest when framework or ecosystem compatibility makes it the stronger fit.
- Add Playwright when critical journeys, browser integration, authentication, routing, or cross-browser behavior justify end-to-end coverage.

Research the selected framework's current test setup, environment, component-testing utilities, and mocking guidance. Define exact scripts and the smallest high-value coverage target.

**Complete this gate when:** unit, integration, and end-to-end scopes are each selected or explicitly omitted, with runnable command names.

### 8. Approve the blueprint

Consolidate the accepted decisions into one blueprint containing:

- selected stack and every deliberate `none`
- folder tree and boundary rules
- state ownership and component architecture
- package list and exact scaffold/setup commands
- check, fix, typecheck, test, build, and optional end-to-end commands
- the skills and official sources that support each choice

Call out conflicts or unresolved decisions. Ask for approval to scaffold.

**Complete this gate when:** the user approves a blueprint with no unresolved scaffold-affecting decision.

### 9. Scaffold and verify

Use the selected framework's current official scaffolder and verified flags. Implement only the approved structure and configuration. Add the smallest representative vertical slice needed to prove module boundaries; skip sample features when configuration alone proves them.

Run the approved read-only checks, type checking, tests, production build, and end-to-end suite when selected. Fix failures within the approved design and report any required deviation with its evidence.

**Complete this gate when:** every approved decision is reflected in the files, every agreed verification command passes, and every deviation is documented.

## Existing-project branch

1. Inspect manifests, lockfiles, framework and build configuration, routing, representative features, UI and styling setup, state/data access, test setup, and CI commands.
2. Present the observed stack with file evidence. Treat established choices as fixed unless the user requests a migration.
3. Identify only the decisions affected by the requested change. Apply the source gate to missing or changing decisions and enter the greenfield sequence at the earliest open gate.
4. Implement ordinary feature work through the existing architecture and directly relevant implementation skills. Verify with the repository's established commands.

When an affected decision remains open, present the observed stack and only the first decision card, then end the turn.

**Complete this branch when:** the change preserves every unaffected convention, changed decisions have user approval and current evidence, and the repository's relevant checks pass.
