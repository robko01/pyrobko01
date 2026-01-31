# AGENTS.md

## Project Overview

This is a Python library for controlling Robko 01-compatible robot controllers. The project provides:

- **Communicators**: Serial, TCP, UDP (pluggable implementations)
- **Controller implementations**: Support for several firmware variants
- **UI tasks**: Qt-based and Tkinter-based interfaces for testing and development
- **Kinematics**: Forward and inverse kinematics calculations

## Essential Commands

```bash
# Virtual environment setup
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # Windows PowerShell
source .venv/bin/activate        # Linux/macOS

# Installation
python -m pip install -e .       # Editable install
python -m pip install -e .[dev]  # With development extras

# Testing
pytest -q                        # Run test suite
pytest -v                        # Verbose output
pytest tests/test_specific.py   # Run specific test file

# Linting and formatting
black .                          # Format code
black --check .                  # Check formatting only
ruff check .                     # Lint code
ruff check . --fix               # Auto-fix lint issues
isort .                          # Sort imports
isort --check-only .             # Check import order only
mypy robko01/                    # Type checking

# Pre-commit hooks
pip install pre-commit           # Install pre-commit (once)
pre-commit install               # Set up git hooks (once)
pre-commit run --all-files       # Run all pre-commit checks
```

## Naming Standards (Python)

| Element | Style | Example |
|---------|-------|---------|
| Modules/packages | lower_snake_case | `task_ui_qt`, `task_grasp_1` |
| Classes | PascalCase | `TaskUI`, `BaseCommunicator` |
| Task classes | Task prefix | `TaskGrasp1`, `TaskInputs` |
| Controller classes | Robko01 | `Robko01` (in controller modules) |
| Exceptions | PascalCase + Error | `InvalidPackageError` |
| Functions/methods | snake_case | `move_relative()`, `get_position()` |
| Callbacks | `_cb` suffix or `on_` prefix | `on_connect()`, `update_cb()` |
| Variables | snake_case | `current_position`, `motor_speed` |
| Private members | leading underscore | `_internal_state` |
| Constants | UPPER_SNAKE | `MAX_SPEED`, `DEFAULT_TIMEOUT` |
| Enum members | Match external spec | `OpCode.MoveRelative`, `DO`, `DI` |

## Code Organization Best Practices

### Module Structure

Use clear separation of concerns in modules:

```python
# region Imports
import logging
from typing import Optional
# endregion

# region Constants
DEFAULT_TIMEOUT = 1.0
# endregion

# region Classes
class MyController:
    """Controller implementation."""
    pass
# endregion
```

### Documentation Style

Use Google-style docstrings for all public classes and functions:

```python
def move_relative(self, positions: list[int]) -> bool:
    """Move the robot by relative step values.

    Args:
        positions: List of 12 integers [steps, delay] * 6 axes.

    Returns:
        True if the move was successful, False otherwise.

    Raises:
        InvalidPackageError: If the positions list is malformed.
    """
    pass
```

### Type Hints

Always use type hints for function signatures:

```python
from typing import Optional, Callable

def connect(
    self,
    port: str,
    timeout: float = 1.0,
    callback: Optional[Callable[[bytes], None]] = None
) -> bool:
    ...
```

## Critical Development Patterns

### Controller Pattern

Each controller implementation follows this structure:

- Inherit from `BaseRobko01` base class
- Implement required abstract methods: `connect()`, `disconnect()`, `move_relative()`, etc.
- Use a communicator instance for actual I/O

### Communicator Pattern

Communicators handle the transport layer:

- Inherit from `BaseCommunicator`
- Implement `connect()`, `disconnect()`, `send()`, `receive()`
- Keep protocol logic in the controller, not the communicator

### Task Pattern

UI tasks follow this structure:

- Inherit from `BaseTask`
- Implement `run()` method as the entry point
- Use dependency injection for the controller instance

### Factory Pattern

Use `ControllerFactory` for creating controller instances:

```python
from robko01.controllers.controller_factory import ControllerFactory

controller = ControllerFactory.create(
    interface="serial",
    port="COM1",
    cname="super",
    timeout=1.0
)
```

## Version Management

Version is managed in `pyproject.toml`:

```toml
[project]
version = "1.0.0"
```

**Before merging to main:**

1. Update version number in `pyproject.toml`
2. Update CHANGELOG.md with changes (if present)
3. Request user approval before merging

## Best Practices

### Git Workflow

- Branching: `main` is production-ready, `dev` is integration; feature branches are created from `dev`.
- Branch naming: `feature/<short-description>` for features, `fix/<short-description>` for bug fixes.
- Commit flow:
  1. `git checkout dev`
  2. `git checkout -b feature/<short-description>`
  3. Stage and commit with a descriptive message.
  4. Test the feature before merging; if hardware-dependent, ask the user to test manually.
  5. Ask for approval before merging the feature into `dev`.
- Merging: always use `--no-ff` to preserve history in GitLens visualization.
  - Merge feature into `dev`: `git merge feature/<short-description> --no-ff -m "Merge feature/<short-description> into dev"`
  - Merge `dev` into `main`: `git merge dev --no-ff -m "Merge dev into main"`
- Push/cleanup: push `main` and `dev`; do not delete merged feature branches unless the user explicitly asks.

### Commit Message Format

```
Short summary in imperative mood (<= 50 chars)

- Bullet point for key change 1
- Bullet point for key change 2

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

## Testing

### Test File Organization

- Test files: `test_*.py` in the `tests/` directory
- Test classes: `Test*` (e.g., `TestController`)
- Test functions: `test_*` (e.g., `test_connect_success`)

### Running Tests

```bash
# Run all tests
pytest -q

# Run with coverage
pytest --cov=robko01

# Run specific test file
pytest tests/test_controllers.py

# Run tests matching pattern
pytest -k "test_connect"
```

### Hardware-Dependent Tests

For tests requiring physical hardware:

1. Mark them with `@pytest.mark.hardware`
2. Skip by default: `pytest -m "not hardware"`
3. Ask the user to run manually when needed

### Testing Without Hardware

Tests are designed to avoid touching real serial ports or joysticks. When testing code that normally talks to hardware:

- Use mocking with `pytest-mock`
- Use the `dummy` communicator/controller for integration tests
- Create lightweight dummy communicators using `BaseCommunicator`

## CI/CD

The repository includes GitHub Actions workflows:

- **CI workflow**: `.github/workflows/ci.yml` runs tests and linters across multiple Python versions
- **Pre-commit hooks**: Configured in `.pre-commit-config.yaml`

## Contributing Guidelines

- Follow Black/ruff/isort rules (pre-commit enforces these automatically)
- Make small, well-scoped commits
- Open PRs against the `dev` branch first
- Do not modify `pyserial` dependency without discussion (kept for backward compatibility)

