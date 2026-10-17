# Gate

Gate = hard stop after one artifact. Next artifact stays undrafted until gate passes.

1. Show artifact path + count line (requirements / components / tasks drafted).
2. Ask via AskUserQuestion: Approve | Request changes. Requirements phase adds: Analyze first (runs `/spec-analyze` flow).
3. Request changes → ask what, edit artifact, repeat from 1.
4. Approve → set phase `approved` in `.spec.json`.

Done when: `.spec.json` phase = `approved`.
