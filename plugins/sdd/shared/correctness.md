# Correctness (property-based tests)

Property = invariant for all inputs meeting a precondition. Example test = one case. Evidence, not proof.

## Steps

1. Framework. Read manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`). Map: JS/TS → fast-check, Python → Hypothesis, Rust → proptest, Go → rapid, Java → jqwik. None fits → ask user; skip steps 2–4 on decline.
2. Classify every criterion: invariant | round-trip | idempotence | metamorphic | model | error-condition | example-only (UI copy, config, one-off).
3. Write property in `design.md` (format in `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/design.md`). Merge criteria sharing one invariant into one property.
4. Add task per property to `tasks.md`: optional `*`, after code it tests. Test file carries tag comment `Feature: <spec>, Property N: <title>`. Iterations ≥100.
5. Run. Red → report shrunk counterexample, ask: fix implementation | fix test | fix requirement. Test stays unchanged until user picks.

Done when: every criterion classified, every property validates ≥1 criterion, every property has task.
