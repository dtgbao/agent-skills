# Skill Benchmark: swe-wiki

**Model**: claude-opus-5-5
**Date**: 2026-11-23T04:16:51Z
**Evals**: 0, 1 (1 runs each per configuration)

## Summary

| Metric | With Skill | Old Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 69% ± 3% | +0.31 |
| Time | 118.8s ± 46.0s | 61.4s ± 44.8s | +57.4s |
| Tokens | 81720 ± 7692 | 73556 ± 7273 | +8164 |

## Notes

- Iteration 2 reruns only the two ingest evals with the tuned research step; old_skill runs are reused from iteration 1 (same snapshot).
- User-visible latency (start to response ready): approval proposal 68 s (iteration 1: 143 s); URL ingest 130 s (iteration 1: about 227 s total).
- Both background haiku researchers finished before the agent's own wiki scan ended, so research left the critical path in both runs.
- Quality held: 13/13 checks pass, including external Related Reading URLs and contradictions in the proposal.
- The old skill is still faster (30 s and 93 s) because it does no web research at all.