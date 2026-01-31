CONTRIBUTING
============

Thank you for contributing to robko01.

This document explains how to set up a local development environment, run
checks, and follow the project workflow. It focuses on Windows (PowerShell)
but also includes Unix-like notes.

Developer setup (Windows - PowerShell)
-------------------------------------
1. Create and activate a virtual environment

```powershell
python -m venv .venv
# Activate (PowerShell)
.\.venv\Scripts\Activate.ps1
# Or for cmd.exe
.\.venv\Scripts\activate
```

2. Upgrade pip and install development dependencies

```powershell
python -m pip install --upgrade pip
# Install the package with dev extras (linters, test tools)
python -m pip install -e .[dev]
```

Note: The repository lists `pyserial` in the project dependencies for backward
compatibility. Do not remove or modify `pyserial` unless you intentionally want
to change runtime requirements.

3. Install pre-commit hooks

```powershell
python -m pip install pre-commit
pre-commit install
# Run hooks once on all files
pre-commit run --all-files
```

Run tests and linters locally
-----------------------------
- Run the full test suite:

```powershell
python -m pytest -q
```

- Run ruff (linter):

```powershell
python -m ruff check .
```

- Run black (format check) and autoformat with black if needed:

```powershell
python -m black --check .
python -m black .
```

- Run isort (imports ordering):

```powershell
python -m isort --check-only .
python -m isort .
```

- Run mypy (type checking):

```powershell
python -m mypy .
```

Working with optional features
------------------------------
- GUI (PySide6) and joystick (pygame) dependencies are included in the base
  install. If you only need core logic, you can still run most tests without
  hardware attached.

Testing without hardware
------------------------
- Tests are designed to avoid touching real serial ports or joysticks. When you
  need to test code that normally talks to hardware, prefer mocking or using
  the included `CommunicatorBase` to create lightweight dummy communicators.

CI and pre-commit
-----------------
- The repository includes a GitHub Actions workflow (`.github/workflows/ci.yml`)
  that runs tests and linters across multiple Python versions. Pre-commit hooks
  are configured in `.pre-commit-config.yaml`.

Style and contributions
-----------------------
- Follow Black/ruff/isort rules. Pre-commit will help enforce these
  automatically.
- Make small, well-scoped commits and open PRs against the `dev` branch first.

Git workflow
------------
- `main` is production-ready and only receives merges from `dev`.
- `dev` is the integration branch.
- Feature branches are created from `dev` and follow:
  - `feature/<short-description>`
  - `fix/<short-description>`
- Always ask for approval before merging a feature branch into `dev`.
- Always use `--no-ff` when merging to preserve history.
- Do not delete merged feature branches unless explicitly asked.

Commit message format
---------------------

```
Short summary in imperative mood (<= 50 chars)

- Bullet point for key change 1
- Bullet point for key change 2

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

Questions
---------
If you're unsure about modifying runtime dependencies (like `pyserial`), ask on
the issue/PR thread - `pyserial` is kept for backward compatibility and should
not be removed lightly.
