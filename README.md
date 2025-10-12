# robko01 — Robko 01 control library

Robko01 (robko01) is a small, test-friendly Python library and command-line
tool for controlling Robko 01-compatible robot controllers. It provides:

- Communicators: serial, TCP, UDP (pluggable implementations)
- Controller implementations for several firmwares
- Small UI tasks and utilities for testing and development

This repository aims to make it easy to script robot motions, run simple UIs,
and develop new controller backends without requiring hardware during testing.

Table of contents
-----------------

- Installation (Windows / Linux / macOS)
- Quick examples (programmatic dummy, CLI serial, trajectory runner)
- Contributing
- License

Requirements
------------

- Python 3.8 or newer
- Required runtime dependencies:
    - `pyserial` for serial communicators
    - `pygame` for joystick/support and game-related tasks
    - `PySide6`, `PySide6-Addons`, `PySide6-Essentials`, and `shiboken6` for
        the Qt-based UI tasks

If you plan to develop or run tests, install the `dev` extras to get linters
and test dependencies.

Installation
------------

Recommended: create and activate a virtual environment before installing.

Windows (PowerShell)

```powershell
python -m venv .venv
# Activate
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Linux / macOS (bash)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Install options
---------------

- Editable install for development (recommended when contributing):

```powershell
python -m pip install -e .
# with development extras (linters, tests):
python -m pip install -e .[dev]
```

- Direct install from GitHub (non-editable):

```powershell
# Latest main branch
python -m pip install "git+https://github.com/robko01/pyrobko01.git"

# Include development extras when installing from GitHub
python -m pip install "git+https://github.com/robko01/pyrobko01.git#egg=robko01[dev]"
```

Notes
-----

- If the package is uploaded to PyPI in the future, you could install with
    `python -m pip install robko01`.
- Extras: `.[dev]` — check `pyproject.toml` for available extras.

Uninstall
---------

Windows (PowerShell)

```powershell
python -m pip uninstall robko01
```

Linux / macOS (bash)

```bash
python3 -m pip uninstall robko01
```

Quick examples
--------------

1) Programmatic example (safe to run without hardware — uses `dummy`)

```py
from robko01.controllers.controller_factory import ControllerFactory

# Create a dummy controller (no hardware required)
ctrl = ControllerFactory.create(interface="dummy", port="0", cname="dummy", timeout=1)

# Build a 12-value move_relative payload: [steps,delay]*6 axes
positions = [0] * 12
positions[0] = 450  # steps for axis 0
positions[1] = 100  # delay for axis 0

ctrl.move_relative(positions)
print("Current position:", ctrl.current_position())
ctrl.disconnect()
```

2) Serial controller script example

Use this script to connect to a Robko01 controller over a serial port and
run a sequence of relative moves. Replace `COM1` with your platform-specific
port name (for Linux use `/dev/ttyUSB0` or similar).

```py
#!/usr/bin/env python
# -*- coding: utf8 -*-

from robko01.controllers.controller_factory import ControllerFactory

port = "COM1" # You should change it according to your setup.
cname = "orlin369"
interface = "serial"

# Controller
controller = ControllerFactory.create(interface=interface, port=port, cname=cname)

# Set the speed.
speed = 150

# Trajectory path.
trajectory = [ \
        [450, 0, 600, 0, -400, 0, 200, 0, -200, 0, 400, 0], \
        [0, 0, 0, 0, 0, 0, 110, 0, 110, 0, 0, 0], \
        [0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -100, 0], \
        [0, 0, -100, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [-900, 0, 0, 0, 0, 0, -200, 0, -200, 0, 0, 0], \
        [0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0], \
        [0, 0, -100, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
        [0, 0, 0, 0, 0, 0, 110, 0, 110, 0, 0, 0], \
        [450, 0, -600, 0, 400, 0, -220, 0, 180, 0, -400, 0] \
        ]

# Run trough trajectory points.
for position in trajectory:
        current_position = scale_speeds(position, speed)            
        controller.move_relative(current_position)
        current_position = controller.current_position()

```

3) Trajectory runner (script using `dummy` communicator)

Save as `run_trajectory.py` and run from an activated virtualenv.

```py
from robko01.controllers.controller_factory import ControllerFactory

ctrl = ControllerFactory.create(interface="dummy", port="0", cname="dummy", timeout=1)

trajectory = [
        [450,0, 600,0, -400,0, 200,0, -200,0, 400,0],
        [0]*12,
]

for pos in trajectory:
        ctrl.move_relative(pos)
        print("position ->", ctrl.current_position())

ctrl.disconnect()
```

Running tests
-------------

To run the test suite locally (after an editable install with dev extras):

```powershell
# from project root
python -m pip install -e .[dev]
pytest -q
```

Contributing
------------

We welcome contributions. See [CONTRIBUTING.md](CONTRIBUTING.md) for a
step-by-step developer setup guide (virtualenv, installing dev extras,
pre-commit hooks and running linters/tests).

If you're preparing a PR please:

- Run `pre-commit run --all-files` before pushing
- Keep changes small and focused
- Add tests for new behavior where possible

License
-------

This project is provided under the GPL-3.0-or-later license. See
[LICENSE](LICENSE) for full text.

Acknowledgements & contact
--------------------------

Maintained by the robko01 organization. For questions or to report issues,
please open an issue on the GitHub repository.

