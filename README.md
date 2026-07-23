# Agent Skills

Small collection of Codex-oriented skills and local agent presets.

This repo is a source tree for reusable instruction bundles. Each skill lives in its own folder under `skills/` and can include a `SKILL.md`, reference notes, agent metadata, assets, or eval fixtures.

## Included skills

| Skill                     | Purpose                                                                              |
| ------------------------- | ------------------------------------------------------------------------------------ |
| `frontend-dev`            | Guide source-backed frontend architecture decisions and greenfield scaffolding.      |
| `orchestrator`            | Plan multi-step work and delegate clean, reviewable subtasks.                        |
| `prd-to-plan`             | Turn a PRD or spec into an implementation plan grounded in the codebase.             |
| `react-best-practices`    | Reusable React/TypeScript architecture guidance plus focused reference docs.         |
| `spec-driven-development` | Turn features and complex bugs into reviewed specs and verified implementation.      |
| `web-search`              | Structured, recency-aware technical web research with source-backed Markdown output. |

## Agent presets

The `.codex/agents/` directory currently contains:

- `code_explorer` for read-only codebase analysis
- `jira_explorer` for read-only Jira issue exploration
- `web_searcher` for invoking the web-search workflow

## Repository layout

```text
.
├── .codex/
│   └── agents/          # Codex agent presets
└── skills/
    ├── <skill>/SKILL.md # Main instructions
    ├── <skill>/references/
    ├── <skill>/agents/
    ├── <skill>/assets/
    └── <skill>/evals/
```

## Notes

- `SKILL.md` is the entrypoint for each skill.
- Reference files stay next to the skill that uses them.
