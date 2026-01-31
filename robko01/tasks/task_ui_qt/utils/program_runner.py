#!/usr/bin/env python
# -*- coding: utf8 -*-

"""

Robko 01 - Python Control Software

Copyright (C) [2020] [Orlin Dimitrov]

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import sys
import threading
import linecache
import traceback

from PySide6.QtCore import Signal
from PySide6.QtCore import QThread

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, Orlin Dimitrov"
"""Copyright holder"""

__credits__ = []
"""Credits"""

__license__ = "GPLv3"
"""License
@see http://www.gnu.org/licenses/"""


__maintainer__ = "Orlin Dimitrov"
"""Name of the maintainer."""

__email__ = "robko01@8bitclub.com"
"""E-mail of the author."""

__status__ = "Debug"
"""File status."""

#endregion

class ProgramRunner(QThread):
    """
    ProgramRunner is thread that executes a Python script with step-by-step debugging support.

    This class uses Python's `sys.settrace` mechanism to intercept line execution events,
    enabling step, pause, continue, and stop controls for script execution. It runs the
    user-loaded Python script inside a dedicated QThread, preventing the GUI from blocking.

    Signals:
        started: emitted when the script execution begins.
        finished: emitted when the script execution ends (normally or by stop request).
        output(str): emitted whenever script output or error messages are produced.
        dbg_line(int, str): emitted when a new line is reached during execution,
                            providing (lineno, source text).

    Public Methods:
        pause()      -> Pause script execution (wait before the next line runs).
        continue_()  -> Resume script execution until completion or stop.
        step_once()  -> Execute exactly one line, then pause again.
        stop()       -> Stop script execution immediately.

    Usage:
        - Assign a Python script path to `self.script_path`.
        - Call `self.start()` to begin execution.
        - Use `pause()`, `continue_()`, `step_once()`, or `stop()` from the GUI
          to control the running script.
    """

    started = Signal()
    finished = Signal()
    output = Signal(str)
    dbg_line = Signal(int, str)  # (lineno, source text)

#region Constructor

    def __init__(self):
        """Constructor
        """
        super().__init__()
        self.script_path = ""
        # stepping control
        self._gate = threading.Event()     # when set -> run; when clear -> paused
        self._gate.set()                   # start in "running"
        self._stepping = False
        self._stop_requested = False
        self.__g = {
            "__name__": "__main__",
            "__file__": self.script_path,
            "output": lambda msg: self.output.emit(str(msg)),
        }
        """globals for executed script: provide an 'output' helper if desired
        """

#endregion

#region Protected Methods

    def _trace(self, frame, event: str, arg):
        """Tracing

        Args:
            frame (_type_): _description_
            event (str): Event type
            arg (_type_): _description_

        Raises:
            SystemExit: _description_
            SystemExit: _description_

        Returns:
            _type_: _description_
        """
        if event == "line" and frame.f_code.co_filename == self.script_path:
            lineno = frame.f_lineno
            src = linecache.getline(self.script_path, lineno).rstrip("\n")
            self.dbg_line.emit(lineno, src)

            if self._stop_requested:
                raise SystemExit

            # wait if paused
            self._gate.wait()
            if self._stop_requested:
                raise SystemExit

            # if stepping, pause again for the next line
            if self._stepping:
                self._gate.clear()
        return self._trace  # keep tracing subsequent events

#endregion

#region Public Methods

    def add_api(self, fx: dict):
        """Update dependencies of the code runner/ e.g. API.
        """
        self.__g.update(fx)

    def pause(self):
        """Pause the code execution.
        """
        self._stepping = False
        self._gate.clear()

    def continue_(self):
        """Continue code running.
        """
        self._stepping = False
        self._gate.set()

    def step_once(self):
        """Step over.
        """
        # allow exactly one line to execute; then pause again
        self._stepping = True
        self._gate.set()

    def stop(self):
        """Stop the execution.
        """
        self._stop_requested = True
        self._gate.set()  # in case we're paused, let trace raise SystemExit

    def run(self):
        """Run the code.
        """
        if not self.script_path:
            self.output.emit("No script loaded.\n")
            return

        self.started.emit()
        self._stop_requested = False
        # default to running; UI may immediately pause/step if desired
        if not self._gate.is_set():
            self._gate.set()

        try:
            with open(self.script_path, "r", encoding="utf-8") as f:
                code = compile(f.read(), self.script_path, "exec")

            # install tracer for THIS thread
            sys.settrace(self._trace)

            # Execute
            exec(code, self.__g, self.__g)

        except SystemExit:
            self.output.emit("Execution stopped by user.\n")
        except Exception:
            self.output.emit(f"{traceback.format_exc()}")
        finally:
            sys.settrace(None)
            self.finished.emit()

#endregion
