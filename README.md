# Agent Skills

Small collection of reusable skills, plugins, and local agent presets for Codex, Claude Code, and
GitHub Copilot.

This repo is a source tree for reusable instruction bundles. Standalone skills live under `skills/`, while installable plugins live under `plugins/` and can bundle multiple related skills.

## Standalone skills

| Skill                     | Purpose                                                                                              |
| ------------------------- | ---------------------------------------------------------------------------------------------------- |
| `design-pattern`          | Provide TypeScript implementations and tradeoffs for the 22 Gang of Four design patterns.            |
| `code-architect`          | Design decisive feature architectures and implementation blueprints from existing codebase patterns. |
| `code-explore`            | Trace feature execution paths, architecture layers, dependencies, and implementation details.        |
| `frontend-scaffold`       | Guide framework-agnostic frontend architecture, tooling choices, and project scaffolding.            |
| `frontend-ui-engineering` | Build accessible, responsive, production-quality interfaces and components.                          |
| `orchestrator`            | Plan multi-step work and delegate clean, reviewable subtasks.                                        |
| `react-best-practices`    | Provide focused React and TypeScript architecture, state, composition, and testing guidance.         |
| `web-search`              | Research current technical guidance and return concise, source-backed summaries.                     |

## Plugins

| Plugin                                             | Purpose                                                                                                                  | Bundled skills                                                   |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| [`fullstack-dev`](plugins/fullstack-dev/README.md) | Coordinate full-stack work from focused context and requirements through implementation, review, operations, and launch. | `index` router plus focused engineering workflows                |
| [`spec-workflow`](plugins/spec-workflow/README.md) | Guide requirements, design, bug-fix, quick-spec, task-planning, and execution workflows.                                 | `spec-new`, spec phases, execution, status, and `steering-setup` |
| [`swe-wiki`](plugins/swe-wiki/README.md)           | Maintain a domain-first, Git-synced software engineering knowledge base across computers.                                | `swe-wiki`                                                       |

## Install plugins with Claude Code

Add the GitHub repository as a marketplace:

```text
/plugin marketplace add dtgbao/agent-skills
```

Then install any bundled plugin:

```text
/plugin install fullstack-dev@bao-plugins
/plugin install spec-workflow@bao-plugins
/plugin install swe-wiki@bao-plugins
```

## Install plugins with GitHub Copilot

Add the GitHub repository as a Copilot plugin marketplace:

```bash
copilot plugin marketplace add dtgbao/agent-skills
```

Then install any bundled plugin:

```bash
copilot plugin install fullstack-dev@bao-plugins
copilot plugin install spec-workflow@bao-plugins
copilot plugin install swe-wiki@bao-plugins
```

## Agent presets

The `.codex/agents/` directory currently contains:

- `jira_explorer` for read-only Jira issue exploration
- `web_searcher` for invoking the web-search workflow

## Repository layout

```text
.
├── .claude-plugin/
│   └── marketplace.json # Claude Code marketplace metadata
├── .github/
│   └── plugin/
│       └── marketplace.json # GitHub Copilot marketplace metadata
├── .agents/
│   └── plugins/         # Local plugin marketplace metadata
├── .codex/
│   └── agents/          # Codex agent presets
├── plugins/
│   └── <plugin>/
│       ├── plugin.json       # Portable Agent Plugins manifest
│       ├── .claude-plugin/   # Claude Code plugin metadata
│       ├── commands/         # Optional Claude Code command entrypoints
│       └── skills/           # Skills bundled by the plugin
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
