# v0.1.0 Release Notes

Initial MVP release of `ai-cli-env-doctor-jp`.

## Highlights

- Adds a Python CLI for Japanese local AI/CLI environment diagnostics.
- Runs read-only checks for Python, Git, Node.js / npm, uv, Codex CLI, PowerShell, and PATH.
- Supports human-readable Japanese output and JSON output.
- Includes `--check` for focused diagnostics and `--strict` for CI-oriented failure behavior.
- Uses only the Python standard library at runtime.
- Applies best-effort redaction for user home paths and common token-like values before rendering reports.

## Verification

- `ruff format --check .`
- `ruff check .`
- `mypy src tests`
- `pytest`
- `python -m build`
- `twine check dist/*`
- built wheel smoke test in GitHub Actions

## Notes

This is a new project. It does not yet have public adoption metrics, stars, downloads, or external usage examples.
