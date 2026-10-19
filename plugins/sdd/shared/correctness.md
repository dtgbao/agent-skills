# Correctness (property-based tests)

Property = invariant for all inputs meeting a precondition. Example test = one case. Evidence, not proof.

## Steps

1. Framework. Read manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`). Map: JS/TS → fast-check, Python → Hypothesis, Rust → proptest, Go → rapid, Java → jqwik. None fits → ask user; skip steps 2–4 on decline.
2. Classify every criterion: invariant | round-trip | idempotence | metamorphic | model | error-condition | example-only (UI copy, config, one-off). Write the table in design.md `## Criteria Classification`.
3. Write property in `design.md` (format in `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/design.md`). Merge criteria sharing one invariant into one property.
4. Tasks: a property sits in the slice that implements its criteria (`${CLAUDE_PLUGIN_ROOT}/shared/artifacts/tasks.md`); the property is that slice's red test for those criteria. Bugfix: Property 1 in the exploration pin, Property 2 in a preservation pin. Leaf may hold several properties. Test file carries tag comment `Feature: <spec>, Property N: <title>` per property. Iterations ≥100. Oracle values and generator bounds are literals from the criterion text; the test imports only the unit under test, never its constants.
5. Run (in `/sdd:spec-run` only). Red → report shrunk counterexample, ask: fix implementation | fix test | fix requirement. Test stays unchanged until user picks.

Done when: every criterion classified, every property validates ≥1 criterion, every property sits in a leaf.
