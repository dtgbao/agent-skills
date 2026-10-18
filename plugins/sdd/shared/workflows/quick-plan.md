# Quick Plan

One pass. Questions first, zero gates between artifacts. `SPEC` per `${CLAUDE_PLUGIN_ROOT}/shared/state.md`.

## Steps

Resume with drafts present → step 3.

1. Questions. Ask via AskUserQuestion, ≤4 per call, ≤2 calls: scope, constraints, edge cases, stack. Skip what prompt answers.
   - Done when: every ambiguity that changes design is answered or assumed (assumption listed in Introduction).
2. Draft in order, no stop: `requirements.md` → `design.md` → `tasks.md`. Formats in `${CLAUDE_PLUGIN_ROOT}/shared/artifacts/`; properties per `${CLAUDE_PLUGIN_ROOT}/shared/correctness.md` steps 1–3. Then `SPEC draft <dir> requirements design tasks`.
   - Done when: three files exist, each artifact's Done-when list holds.
3. One question: Approve all | Analyze requirements | Refine. Analyze → `${CLAUDE_PLUGIN_ROOT}/shared/gate.md` step 3, then ask again. Approve all → `SPEC approve <dir> requirements design tasks`. Then tell user: `/sdd:spec-run <name>`.

Domain unfamiliar or high-risk → recommend Requirements-First instead.
