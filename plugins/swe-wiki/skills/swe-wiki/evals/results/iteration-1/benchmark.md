# Skill Benchmark: swe-wiki

**Model**: claude-opus-5-5
**Date**: 2026-11-23T04:09:20Z
**Evals**: 0, 1, 2, 3 (1 runs each per configuration)

## Summary

| Metric | With Skill | Old Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 84% ± 18% | +0.16 |
| Time | 120.7s ± 81.8s | 71.2s ± 28.2s | +49.5s |
| Tokens | 79685 ± 8314 | 76150 ± 5191 | +3535 |

## Notes

- Query eval is non-discriminating: both versions read the wiki's AGENTS.md unprompted and followed its local conventions (6/6 each). It does not prove the new 'read AGENTS.md' instruction matters.
- All failures of the old skill trace to new features: no raw snapshot for URL sources, no summary frontmatter, no takeaways or emphasis question at approval time.
- Time cost: the new parallel-research step makes ingest slower, not faster, in these runs (URL ingest 227s vs 93s; approval proposal 143s vs 30s). The old skill did no web research at all, so this is not the sequential-research baseline the user complained about.
- Every old-skill run used `init` to rebuild indexes and added a stray `bootstrap` log entry; new-skill runs used the new `index` command.
- Tokens are similar (69k-90k per run); the parallel subagents' own tokens are not included in the parent count.