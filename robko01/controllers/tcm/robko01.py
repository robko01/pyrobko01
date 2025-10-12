#!/usr/bin/env python
# -*- coding: utf8 -*-

"""

Robko 01 - Python Control Software

Copyright (C) [2025] [Orlin Dimitrov]

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

import time

from robko01.controllers.base import Robko01Base
from robko01.utils.logger import get_logger

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2025, Orlin Dimitrov"
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

class Robko01(Robko01Base):
    """This class is dedicated to control robot controller made by Orlin Dimitrov.
    """

#region Attributes

#endregion

#region Constructor

    def __init__(self, **kwargs):

        super().__init__(kwargs)

        self.__logger = get_logger(__name__)

        self.__is_moving_cb = None
        """Is moving callback.
        """

        self.__digital_inputs = 0

        self.__digital_outputs = 0
        """Digital outputs.
        """

#endregion

#region Public Methods

    def connect(self):
        """Connect to the robot controller.
        """
        self._communicator.connect()

    def disconnect(self):
        """Disconnect from robot controller.
        """
        self._communicator.disconnect()

    def stop(self):
        """Stop robot motion execution.
        """
        response = None

        return response

    def disable(self):
        """Disable robot motion execution.
        """
        response = None

        return response

    def enable(self):
        """Enable robot motion execution.

        Raises:
            InvalidOperationCode: Invalid operation code.
            InvalidStatusCode: Invalid status code.
            InvalidPackage: Invalid package code.

        Returns:
            any: _description_
        """
        response = None

        return response

    def clear(self):
        """Clear robot position.

        """
        response = None
        command = "@CLEAR\r".encode('ASCII')
        self.__logger.debug("Command: %s", command)
        response = self._communicator.send_frame(command)
        self.__logger.debug("Response: %s", response)
        return response

    def move_absolute(self, target_position):
        """Move absolute to next robot position.
        """

        steps = target_position[0:12:2]
        speed = max(target_position[1:12:2])

        d = abs(int(speed))
        q1 = round(steps[0], 0)
        q2 = round(steps[1], 0)
        q3 = round(steps[2], 0)
        q4 = round(steps[3], 0)
        q5 = round(steps[4], 0)
        q6 = int(0)
        out = self.__digital_outputs
        command = f"@STEP {d},{q1},{q2},{q3},{q4+q5},{q4-q5},{q6},{out}\r".encode('ASCII')
        self.__logger.debug("Command: %s", command)
        response = self._communicator.send_frame(command)
        self.__logger.debug("Response: %s", response)

        return response

    def is_moving(self):
        """Is moving. Every bit represents an axis.
        """
        result = 0

        if self.__is_moving_cb is not None:
            self.__is_moving_cb(result)

        return result

    def current_position(self):
        """Current robot position.
        """
        response = []
        command = f"@READ\r".encode('ASCII')
        self.__logger.debug("Command: %s", command)
        response = self._communicator.send_frame(command)
        self.__logger.debug("Response: %s", response)

        return response

    def get_inputs(self):
        """Current robot inputs.
        """

        return self.__digital_inputs

    def set_outputs(self, value: int):
        """Set robot outputs.

        Args:
            value (int): Digital outputs bit mask.
        """
        response = None

        if value < 0:
            raise ValueError(f"The value: {value} should be bigger then 0.")

        if value > 255:
            raise ValueError(f"The value: {value} should be less then 255.")

        self.__digital_outputs = value

        return response

    def is_moving_cb(self, callback):
        """Is moving callback.

        Args:
            callback (function): Callable callback function.
        """
        self.__is_moving_cb = callback

#endregion
