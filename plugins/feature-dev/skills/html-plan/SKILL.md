---
name: html-plan
description: Render completed software architecture designs as self-contained interactive HTML plans. Use when feature-dev Phase 4 chooses HTML, or when a user asks to turn a resolved architecture blueprint into a visual plan with comparable approaches, diagrams, implementation maps, and an approval handoff.
---

# HTML Plan

Treat the artifact as a decision interface, not a decorated document.

## 1. Gate on a complete design

Require the completion criterion in `../feature-dev/references/architecture-design.md` to hold before authoring HTML. Preserve its three approaches, evidence, recommendation, complete blueprints, and implementation detail.

If a product or architecture decision remains unresolved, stop HTML authoring and return to feature-dev Phase 3. Resolve one decision at a time before continuing. Represent a bounded technical unknown only as a validation spike with an owner, method, and completion criterion.

Complete this step when the HTML work requires no architectural invention.

## 2. Initialize the artifact

Resolve this skill's directory from the loaded `SKILL.md`. From the target repository, run:

```bash
python3 <skill-dir>/scripts/create_plan.py <feature-slug>
```

Use `--date YYYY-MM-DD` only for a backdated plan or deterministic test. Use `--force` only when the user explicitly authorizes replacing the resolved output file.

The script creates `docs/plans/YYYY-MM-DD-<feature-slug>.html` from `assets/architecture-plan.html`. Use `rg -n "PLAN:" <output>` to locate authoring zones without rereading the fixed CSS and interaction shell.

Complete this step when the destination exists and no pre-existing file was overwritten implicitly.

## 3. Build the decision interface

Keep the shell as a strong baseline, then reshape it when the architecture communicates better another way.

Always provide:

- Codebase patterns and constraints with `file:line` evidence.
- A continuously visible comparison of three viable approaches and an evidence-backed recommendation.
- Three tabbed, independently implementable blueprints; select the recommendation initially.
- For each blueprint: component design, a meaningful architecture or data-flow diagram, implementation map, build sequence, and risks with mitigations.
- An approach selector plus an approval export containing the selected approach, rationale, and reviewer concerns.

Add contract-defining code only where reviewing the exact seam changes the decision. Add UI mockups only for user-visible behavior. Add other visuals only when they clarify a nontrivial relationship.

Prefer the bundled data-driven diagram renderer: edit the compact lane, node, and edge data in each `data-diagram-data` block. Give every node useful inspector detail and codebase evidence. Replace it with accessible inline SVG carrying `data-custom-diagram="<approach-id>"` when the renderer cannot express the architecture cleanly.

Complete this step when the page communicates relationships spatially and the reader can compare, inspect, choose, and export without reconstructing the plan from prose.

## 4. Preserve the artifact boundary

Keep the output as one portable file with inline HTML, CSS, JavaScript, and SVG. Embed necessary images as data URLs. Use the neutral editorial shell for the plan; borrow project styling only inside relevant UI mockups.

Keep the comparison visible while switching blueprint tabs. Preserve keyboard operation, focus states, responsive layouts, reduced-motion behavior, and readable print output when modifying the shell.

Complete this step when the artifact works from `file://` without a network connection.

## 5. Validate and render

Run:

```bash
python3 <skill-dir>/scripts/validate_plan.py docs/plans/YYYY-MM-DD-<feature-slug>.html
```

Fix every reported failure. Then open the file in a browser and verify:

1. All blueprint tabs work with pointer and keyboard input.
2. Every diagram node opens the correct evidence and detail.
3. Approach selection updates the approval summary.
4. Reviewer concerns appear in the copied approval prompt.
5. Theme, narrow viewport, and print layouts remain legible.
6. No placeholder, overflow, clipped content, or browser-console error remains.

Complete the skill only when validation passes and the rendered interaction check succeeds. Report the artifact path and the checks performed.
