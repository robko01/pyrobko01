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

#endregion

class AxisActionController():
    """Axis controller.
    """

#region Attributes

    __direction = 0

    __speed = 100

#endregion

#region Constructor

    def __init__(self, **kwargs):

        if "callback" in kwargs:
            self.__callback = kwargs["callback"]

        if "speed" in kwargs:
            self.__speed = kwargs["speed"]

#endregion

#region Properties

    @property
    def speed(self):
        """Speed of the controller.

        Returns:
            int: Speed
        """

        return self.__speed

    @speed.setter
    def speed(self, value):
        """Set speed of the controller.

        Args:
            value (int): Speed
        """

        self.__speed = value

        if self.__callback is not  None:
            self.__callback(self.__direction * self.__speed)

    @property
    def is_stopped(self):
        """Is stopped.

        Returns:
            bool: State
        """

        return self.__direction == 0

    @property
    def direction(self):
        """Current direction.

        Returns:
            _type_: _description_
        """

        return self.__direction

#endregion

#region Public Methods

    def stop(self):
        """Stop
        """

        if self.__direction == 0:
            return

        self.__direction = 0

        if self.__callback is not None:
            self.__callback(self.__direction * self.__speed)

    def set_cw(self):
        """Set CW direction.
        """

        if self.__direction == -1:
            self.__direction = 0

        elif self.__direction == 0:
            self.__direction = 1

        else:
            return

        if self.__callback is not None:
            self.__callback(self.__direction * self.__speed)

    def set_ccw(self):
        """Set CCW direction.
        """

        if self.__direction == 1:
            self.__direction = 0

        elif self.__direction == 0:
            self.__direction = -1

        else:
            return

        if self.__callback is not None:
            self.__callback(self.__direction * self.__speed)

#endregion
