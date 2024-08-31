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

__version__ = "1.0.0"
"""Version of the file."""

__maintainer__ = "Orlin Dimitrov"
"""Name of the maintainer."""

__email__ = "robko01@8bitclub.com"
"""E-mail of the author."""

__status__ = "Debug"
"""File status."""

#endregion

class BaseTask:
    """Base task class.
    """

#region Attributes

#endregion

#region Properties

    @property
    def name(self):
        """Name of the task.

        Returns:
            str: Name of the task.
        """
        return self._name

#endregion

#region Constructor

    def __init__(self, kwargs):

        self._kwargs = kwargs
        """Key words arguments.
        """

        self._controller = None
        """Controller
        """

        self._stop_flag = False
        """Stop flag.
        """

        self._execution_mode = 0
        """Execution mode.
        """

        self._name = ""

        if "controller" in self._kwargs:
            self._controller = self._kwargs["controller"]

        if "em" in self._kwargs:
            self._execution_mode = self._kwargs["em"]

#endregion

#region Protected Methods

    def _start_cont(self):
        """Start the app.
        """

        if self._stop_flag:
            return

        self._stop_flag = False

        if self._controller is not None:

            self._controller.connect()

            # Enter synchronous mode.
            self._controller.synchronous = True

            # Wait for controller to respond.
            self._controller.wait_for_controller()

            # Enable the motors.
            self._controller.enable()

    def _stop_cont(self):
        """Stop the app.
        """

        if not self._stop_flag:
            return

        self._stop_flag = True

        if self._controller is not None:

            # Stop all the motors.
            self._controller.stop()

            # Disable motors.
            self._controller.disable()

            self._controller.disconnect()

#endregion

#region Public Methods

    def start(self):
        """Start the task.
        """

    def stop(self):
        """Stop the task.
        """

#endregion
