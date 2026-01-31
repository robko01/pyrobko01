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

from __future__ import annotations

from typing import Tuple

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

class Robko01Base:
    """Concrete base used across controllers.

    This class provides a lightweight, concrete controller base so test
    code can instantiate controller classes (including via __new__) without
    requiring the concrete controllers to implement low-level methods used
    only in runtime (connect/disconnect/current_position). Controllers may
    still override any of these methods with real behavior.
    """

#region Constructor

    def __init__(self, *args, **kwargs) -> None:

        # Support legacy callers that passed a single dict as a positional
        # argument: `super().__init__(kwargs)`. Merge that dict into kwargs
        # so both calling styles work.
        if args and isinstance(args[0], dict):
            legacy = args[0]
            # Only add keys that aren't already in kwargs so explicit keyword
            # arguments take precedence.
            for k, v in legacy.items():
                if k not in kwargs:
                    kwargs[k] = v

        self._time_to_stop: bool = False
        """Time to stop flag."""

        # Optional communicator passed by ControllerFactory or test code.
        self._communicator = kwargs.get("communicator") if kwargs else None

        # validate communicator only when explicitly provided (some tests
        # create controller instances without wiring communicators)
        if "communicator" in kwargs and self._communicator is None:
            raise ValueError("Communicator can not be None.")

#endregion

#region Public Methods

    def connect(self) -> None:
        """Open connection to the robot/hardware.

        Default implementation is a noop (controllers that require a real
        connection should override this method). Tests that instantiate
        controllers won't attempt to open hardware.
        """

    def disconnect(self) -> None:
        """Close connection to the device and cleanup resources.

        Default implementation is a noop.
        """

    def is_connected(self) -> bool:
        """Return True if controller is currently connected.

        Default: False.
        """
        return False

    def current_position(self) -> Tuple[int, ...]:
        """Return the current position as a tuple of ints.

        Default implementation returns a 12-element zero tuple to make
        higher-level logic and tests tolerant to uninitialized controllers.
        """
        return tuple([0] * 12)

#endregion
