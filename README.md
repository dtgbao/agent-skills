# Agent Skills

Small collection of Codex-oriented skills, plugins, and local agent presets.

This repo is a source tree for reusable instruction bundles. Standalone skills live under `skills/`, while installable plugins live under `plugins/` and can bundle multiple related skills.

## Standalone skills

| Skill                     | Purpose                                                                                      |
| ------------------------- | -------------------------------------------------------------------------------------------- |
| `design-pattern`          | Provide TypeScript implementations and tradeoffs for the 22 Gang of Four design patterns.    |
| `frontend-scaffold`       | Guide framework-agnostic frontend architecture, tooling choices, and project scaffolding.    |
| `frontend-ui-engineering` | Build accessible, responsive, production-quality interfaces and components.                  |
| `orchestrator`            | Plan multi-step work and delegate clean, reviewable subtasks.                                |
| `react-best-practices`    | Provide focused React and TypeScript architecture, state, composition, and testing guidance. |
| `web-search`              | Research current technical guidance and return concise, source-backed summaries.             |

## Plugins

| Plugin                                             | Purpose                                                                                                                  | Bundled skills                                                   |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| [`fullstack-dev`](plugins/fullstack-dev/README.md) | Coordinate full-stack work from focused context and requirements through implementation, review, operations, and launch. | `index` router plus focused engineering workflows                |
| [`spec-workflow`](plugins/spec-workflow/README.md) | Guide requirements, design, bug-fix, quick-spec, task-planning, and execution workflows.                                 | `spec-new`, spec phases, execution, status, and `steering-setup` |
| [`swe-wiki`](plugins/swe-wiki/README.md)           | Maintain a domain-first, Git-synced software engineering knowledge base across computers.                                | `swe-wiki`                                                       |

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
│       ├── plugin.json       # Portable Agent Plugins manifest
│       ├── .claude-plugin/   # Optional Claude-specific compatibility metadata
│       └── skills/      # Skills bundled by the plugin
└── skills/
    ├── <skill>/SKILL.md # Main instructions
    ├── <skill>/references/
    ├── <skill>/agents/
    ├── <skill>/assets/
    └── <skill>/evals/
```

## Notes

- Plugin roots follow the [Agent Plugins 1.0.0 specification](https://agent-plugins.org/), with
  client-specific compatibility metadata retained only where needed.
- Reference files stay next to the skill that uses them.
