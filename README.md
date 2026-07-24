# Agent Skills

Small collection of Codex-oriented skills, plugins, and local agent presets.

This repo is a source tree for reusable instruction bundles. Standalone skills live under `skills/`, while installable plugins live under `plugins/` and can bundle multiple related skills.

## Standalone skills

| Skill                     | Purpose                                                                              |
| ------------------------- | ------------------------------------------------------------------------------------ |
| `frontend-scaffold`       | Guide source-backed frontend architecture decisions and greenfield scaffolding.      |
| `orchestrator`            | Plan multi-step work and delegate clean, reviewable subtasks.                        |
| `react-best-practices`    | Reusable React/TypeScript architecture guidance plus focused reference docs.         |
| `spec-driven-development` | Turn features and complex bugs into reviewed specs and verified implementation.      |
| `swe-wiki`                | Maintain a persistent software engineering knowledge base.                           |
| `web-search`              | Structured, recency-aware technical web research with source-backed Markdown output. |

## Plugins

| Plugin        | Purpose                                                                                               | Bundled skills                                                                  |
| ------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `feature-dev` | Guide feature work from codebase discovery through architecture, implementation, review, and summary. | `feature-dev`, `code-review`, `domain-modeling`, `grilling`, `html-plan`, `tdd` |

## Agent presets

The `.codex/agents/` directory currently contains:

- `code_architect` for feature architecture and implementation planning
- `code_explorer` for read-only codebase analysis
- `code_reviewer` for focused code review
- `jira_explorer` for read-only Jira issue exploration
- `web_searcher` for invoking the web-search workflow

## Repository layout

```text
.
├── .agents/
│   └── plugins/         # Local plugin marketplace metadata
├── .codex/
│   └── agents/          # Codex agent presets
├── plugins/
│   └── <plugin>/
│       ├── .codex-plugin/plugin.json
│       └── skills/      # Skills bundled by the plugin
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
