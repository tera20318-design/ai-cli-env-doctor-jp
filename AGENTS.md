# AGENTS.md

## Project Purpose

`ai-cli-env-doctor-jp` is an OSS Python CLI that diagnoses common local AI/CLI developer environment issues and explains findings in Japanese.

The tool helps users inspect problems around:

- `git`
- Python
- Node.js / `npm`
- `uv`
- Codex CLI / related local setup
- PowerShell execution policy
- `PATH`
- shell command discovery and version mismatches

The CLI runs locally, uses Python 3.10+, and keeps runtime dependencies to the Python standard library only.

## Target Users

This project is for Japanese-speaking developers who use AI coding tools, CLIs, package managers, and terminal-based workflows.

Primary users include:

- Windows / PowerShell users who hit execution policy or PATH problems
- Developers setting up AI coding tools for the first time
- Users who have multiple Python, Node.js, or CLI installations
- Users who need concrete Japanese explanations and next steps instead of raw error strings

The output should be practical, concise, and understandable without assuming deep terminal knowledge.

## Directory Structure

Expected structure:

```text
.
|-- AGENTS.md
|-- README.md
|-- pyproject.toml
|-- src/
|   `-- ai_cli_env_doctor_jp/
|       |-- __init__.py
|       |-- __main__.py
|       |-- cli.py
|       |-- checks/
|       |   |-- __init__.py
|       |   |-- codex.py
|       |   |-- git.py
|       |   |-- node.py
|       |   |-- path.py
|       |   |-- powershell.py
|       |   |-- python.py
|       |   `-- uv.py
|       |-- models.py
|       |-- report.py
|       `-- utils.py
`-- tests/
    |-- test_cli.py
    |-- test_report.py
    `-- checks/
        |-- test_codex.py
        |-- test_git.py
        |-- test_node.py
        |-- test_path.py
        |-- test_powershell.py
        |-- test_python.py
        `-- test_uv.py
```

Keep modules small and organized by diagnostic area.

## Implementation Policy

- Runtime code must use Python 3.10+ standard library only.
- Do not add runtime dependencies unless explicitly approved.
- Dev tooling may use `pytest`, `ruff`, `mypy`, `build`, and `twine`.
- Prefer `subprocess.run()` with explicit arguments over shell string execution.
- Avoid destructive commands. Diagnostics must be read-only by default.
- Do not mutate user configuration, shell profiles, registry, `PATH`, or package installations.
- Print Japanese user-facing messages.
- Keep internal code names clear and English.
- Keep remediation advice concrete, but avoid pretending the tool fixed anything unless it actually did.
- Detect missing commands with `shutil.which()`.
- Treat Windows and PowerShell as first-class targets.
- Keep platform-specific logic isolated.
- Handle command failures gracefully and include the failed command, exit code, and useful stderr when appropriate.
- Never assume a tool is installed because another related tool is installed.
- Prefer explicit status values such as `ok`, `warning`, `error`, `not_found`, and `unknown`.
- Avoid network access unless a future feature explicitly requires it and documents why.

## Testing Policy

Tests should focus on deterministic local behavior.

Use mocks for:

- command discovery
- subprocess calls
- environment variables
- platform detection
- `PATH` contents
- PowerShell execution policy output

Do not require real installations of `git`, `node`, `npm`, `uv`, or Codex for unit tests.

Every diagnostic check should have tests for:

- command found
- command missing
- command returns malformed output
- command exits non-zero
- platform-specific behavior where applicable
- Japanese explanation text presence

CLI tests should verify:

- exit codes
- basic output shape
- selected checks
- all-checks mode
- error handling

## Commands

Install dev dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run lint:

```bash
ruff check .
```

Run format check:

```bash
ruff format --check .
```

Format code:

```bash
ruff format .
```

Run typecheck:

```bash
mypy src tests
```

Build package:

```bash
python -m build
python -m twine check dist/*
```

Recommended full local verification before PR:

```bash
ruff format --check .
ruff check .
mypy src tests
pytest
python -m build
python -m twine check dist/*
```

## README Requirements

`README.md` must include:

- Clear project purpose
- Japanese-first description
- Supported Python version
- Runtime dependency policy: Python stdlib only
- Installation instructions
- Basic usage examples
- Example Japanese output
- List of current implemented checks
- Clear distinction between implemented and planned features
- Privacy statement explaining that diagnostics run locally
- Security notes about read-only behavior
- Development setup
- Test, lint, typecheck, and build commands
- Contribution guidance
- License information

Do not document features that do not work yet.

## PR Checklist

Before opening or merging a PR, confirm:

- [ ] User-facing output is Japanese.
- [ ] Runtime code uses only the Python standard library.
- [ ] No unnecessary dependency was added.
- [ ] Diagnostics are read-only by default.
- [ ] Platform-specific behavior is tested or guarded.
- [ ] Tests pass with `pytest`.
- [ ] Lint passes with `ruff check .`.
- [ ] Formatting passes with `ruff format --check .`.
- [ ] Typecheck passes with `mypy src tests`.
- [ ] Package builds with `python -m build`.
- [ ] Package metadata passes with `python -m twine check dist/*`.
- [ ] README reflects only working behavior.
- [ ] No fabricated metrics, adoption claims, stars, downloads, or usage numbers were added.
- [ ] Security and privacy implications were considered.

## Security And Privacy Notes

This tool is intended to inspect local environment state and explain likely issues.

Rules:

- Do not collect telemetry.
- Do not send diagnostic results to external services.
- Do not print secrets, tokens, API keys, or full sensitive environment dumps.
- Redact suspicious values when displaying environment variables.
- Avoid printing the full `PATH` unless the user explicitly requests verbose output.
- Prefer summarized `PATH` diagnostics over raw dumps.
- Do not modify shell profiles, registry entries, package manager config, or user files.
- Any future auto-fix mode must be opt-in, clearly documented, and tested separately.

## Things Not To Do

- Do not fabricate stars, downloads, usage, adoption, benchmarks, or community traction.
- Do not overstate the project for review, README, package metadata, or PR descriptions.
- Do not add unnecessary dependencies.
- Do not document non-working features.
- Do not claim support for platforms or shells that are not tested.
- Do not hide command failures behind vague messages.
- Do not make network calls for local diagnostics.
- Do not write to user configuration files during normal diagnosis.
- Do not present suggestions as guaranteed fixes.
- Do not include promotional language that makes the tool sound more mature than it is.
