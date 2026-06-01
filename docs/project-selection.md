# Project Selection Notes

The project was selected for a weekend-sized honest OSS MVP. These notes are planning context, not application claims.

| Idea | Concrete problem | Users | MVP | One-night feasibility | Maintenance value | Honest application point | Difficulty |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ai-cli-env-doctor-jp` | Windows/PowerShell/npm/Codex/uv/git setup failures are hard to interpret | Japanese AI/CLI developers | Environment checks plus Japanese next steps | High | Add diagnostic rules over time | Reduces local setup friction for Japanese AI/CLI developers | 2/5 |
| `prompt-runbook-lint` | Prompts and runbooks become ambiguous | Solo AI developers | Markdown lint for vague instructions | High | Add rules | Improves AI workflow docs | 2/5 |
| `jp-issue-triage-cli` | Japanese issues take time to prioritize | Small OSS maintainers | Summarize and classify issues | Medium | Label rules and output formats | Helps Japanese OSS maintenance | 3/5 |
| `readme-ja-sync-check` | Japanese README drifts from English README | Bilingual OSS authors | Heading and untranslated text checks | High | Multilingual extensions | Keeps Japanese docs fresh | 2/5 |
| `cli-screenshot-recorder` | README terminal screenshots get stale | CLI authors | Command output to SVG/PNG | Medium | Themes and CI integration | Improves CLI documentation | 3/5 |
| `llm-cost-log` | AI API experiment costs are hard to review | AI solo developers | JSONL cost summary | High | Pricing table updates | Improves cost transparency | 2/5 |
| `jp-changelog-helper` | Changelogs are postponed | Solo OSS authors | Draft Japanese changelog from commits | Medium | Templates and release formats | Helps small release workflows | 3/5 |
| `dotfiles-health-check` | Dotfiles break silently | CLI users | PATH, alias, symlink checks | High | More checks over time | Improves environment reproducibility | 2/5 |
| `ai-agent-task-ledger` | AI agent decisions and unfinished work scatter | Codex/Claude users | Markdown/JSONL task ledger | Medium | Search/export features | Improves auditability of AI-assisted work | 3/5 |
| `oss-maintenance-kanban-cli` | Solo OSS maintenance tasks are forgotten | Solo maintainers | CLI kanban from issues/TODOs | Medium | GitHub integration | Supports ongoing OSS maintenance | 3/5 |

## Selected Idea

`ai-cli-env-doctor-jp` was selected because it has a concrete problem, a small read-only MVP, clear test boundaries, and natural maintenance value through additional diagnostic rules. It can be described honestly as a new local diagnostic CLI; no traction or adoption claims are needed.

## README Heading Plan

- Project name and one-sentence purpose
- Features
- Implemented Checks
- Installation
- Quick Start
- Example Output
- Privacy And Security
- Development
- Roadmap
- Contributing
- License

## Initial Issues

- Add more malformed version-output fixtures for each command check.
- Improve PowerShell and npm shim wording from real user reports.
- Add a GitHub Actions usage example for `--strict`.
- Add an optional verbose mode design note with redaction rules.

## v0.1.0 Done Conditions

- CLI can run all documented checks locally.
- `--check`, `--json`, and `--strict` work.
- Runtime code has no dependencies outside the Python standard library.
- Tests do not require real installations of git, node, npm, uv, Codex, or PowerShell.
- `ruff format --check .`, `ruff check .`, `mypy src tests`, `pytest`, and `python -m build` pass.
- README, LICENSE, CHANGELOG, CONTRIBUTING, SECURITY, roadmap, example output, release notes draft, and CI config exist.
- README does not claim stars, downloads, users, PyPI publication, or external adoption.
