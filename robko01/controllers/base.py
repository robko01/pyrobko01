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

from abc import ABC, abstractmethod
from typing import Sequence, Tuple

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

class Robko01Base(ABC):
    """Concrete base used across controllers.

    Provides basic attributes and default implementations that raise package
    exceptions. Concrete controllers should inherit from this class and
    override methods where necessary. This keeps tests and mocks simple.
    """

#region Constructor

    def __init__(self, kwargs) -> None:

        self._time_to_stop: bool = False
        """Time to stop flag.
        """

        self._communicator = None
        """Communicator instance.
        """

        if 'communicator' in kwargs:
            self._communicator = kwargs['communicator']
            if self._communicator is None:
                raise ValueError("Communicator can not be None.")

#endregion

#region Abstract Methods

    @abstractmethod
    def connect(self) -> None:
        """Open connection to the robot/hardware.

        Raises:
            robko01.exceptions.ControllerConnectionError on failure.
        """

    @abstractmethod
    def disconnect(self) -> None:
        """Close connection to the device and cleanup resources."""

    @abstractmethod
    def is_connected(self) -> bool:
        """Return True if controller is currently connected."""

    @abstractmethod
    def current_position(self) -> Tuple[int, ...]:
        """Return the current position as a tuple of ints."""

#endregion
