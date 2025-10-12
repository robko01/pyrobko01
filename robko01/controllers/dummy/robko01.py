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

import time
from struct import pack, unpack

from robko01.controllers.base import Robko01Base
from robko01.utils.logger import get_logger

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

class Robko01(Robko01Base):
    """This class is dummy controller.
    """

#region Attributes

#endregion

#region Constructor

    def __init__(self, communicator):

        super().__init__()

        if communicator is None:
            raise ValueError("Communicator can not be None.")

        self._communicator = communicator
        """Communicator
        """

        self.__current_position = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        """Current end-effector position.
        """

        self.__logger = get_logger(__name__)

#endregion

#region Public Methods

    def connect(self):
        """Connect to the robot controller.
        """
        self.__logger.info("Connect to dummy controller.")

    def disconnect(self):
        """Disconnect from robot controller.
        """
        self.__logger.info("Disconnect from dummy controller.")

    def ping(self, payload):
        """Ping the robot controller.

        Args:
            payload (bytes): Ping payload.

        Raises:
            ValueError: Payload can not be None.
            InvalidOperationCode: Invalid operation code.
            InvalidStatusCode: Invalid status code.
            InvalidPackage: Invalid package code.

        Returns:
            bytes: Answer payload.
        """
        if payload is None:
            raise ValueError("Payload can not be None")

        response = None
        # TODO: Will explode.

        return response

    def stop(self):
        """Stop robot motion execution.

        Raises:
            InvalidOperationCode: Invalid operation code.
            InvalidStatusCode: Invalid status code.
            InvalidPackage: Invalid package code.

        Returns:
            any: Communicator response.
        """
        response = None
        # TODO: Will explode.

        return response

    def disable(self):
        """Stop robot motion execution.

        Raises:
            InvalidOperationCode: Invalid operation code.
            InvalidStatusCode: Invalid status code.
            InvalidPackage: Invalid package code.

        Returns:
            any: Communicator response.
        """
        response = None
        # TODO: Will explode.

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
        # TODO: Will explode.

        return response

    def clear(self):
        """Clear robot position.

        Raises:
            InvalidOperationCode: Invalid operation code.
            InvalidStatusCode: Invalid status code.
            InvalidPackage: Invalid package code.

        Returns:
            any: Communicator response.
        """
        response = None
        # TODO: Will explode.

        return response

    def _move_relative_impl(self, current_position):
        """Move relative to next robot position.

        Args:
            current_position (list): New robot position.

        Raises:
            InvalidOperationCode: Invalid operation code.
            InvalidStatusCode: Invalid status code.
            InvalidPackage: Invalid package code.

        Returns:
            any: Communicator response.
        """
        response = None
        # TODO: Will explode.

        return response

    def move_relative(self, *args):
        """Unified move_relative dispatcher.

        Accepts either a single sequence of positions (the new, unified API)
        or the old (joint, delay, steps) signature. Old-style calls are
        forwarded to the original implementation which is now
        `_move_relative_impl`.
        """
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            return self._move_relative_impl(args[0])
        elif len(args) == 3:
            joint, delay, steps = args
            # Map single-joint call into a full positions array expected by
            # the implementation: place steps and delay at the appropriate
            # indices and call the list-based implementation.
            point = [0] * 12
            idx = int(joint) * 2
            if 0 <= idx < 12:
                point[idx] = steps
                point[idx + 1] = delay
            return self._move_relative_impl(point)
        else:
            raise TypeError("move_relative expects either positions list or (joint,delay,steps)")

    def move_absolute(self, current_position):
        """Move absolute to next robot position.

        Args:
            current_position (_type_): _description_

        Raises:
            InvalidOperationCode: Invalid operation code.
            InvalidStatusCode: Invalid status code.
            InvalidPackage: Invalid package code.

        Returns:
            any: Communicator response.
        """
        response = None
        # TODO: Will explode.

        self.__current_position = current_position

        return response

    def is_moving(self):
        """Is moving. Every bit represents an axis.

        Raises:
            InvalidOperationCode: Invalid operation code.
            InvalidStatusCode: Invalid status code.
            InvalidPackage: Invalid package code.

        Returns:
            int: Bit masking of robot motion.
        """
        response = 0

        return response

    def current_position(self):
        """Current robot position.

        Raises:
            InvalidOperationCode: Invalid operation code.
            InvalidStatusCode: Invalid status code.
            InvalidPackage: Invalid package code.

        Returns:
            list: Robot positions.
        """
        response = self.__current_position

        return response

    def get_inputs(self):
        """Current robot inputs.

        Raises:
            InvalidOperationCode: Invalid operation code.
            InvalidStatusCode: Invalid status code.
            InvalidPackage: Invalid package code.

        Returns:
            list: Inputs of the robot.
        """
        response = 0

        return response

    def set_outputs(self, value):
        """Set robot outputs.

        Args:
            value (int): New robot position.

        Raises:
            InvalidOperationCode: Invalid operation code.
            InvalidStatusCode: Invalid status code.
            InvalidPackage: Invalid package code.

        Returns:
            any: Communicator response.
        """
        response = None
        # TODO: Will explode.

        return response

    def move_speed(self, current_position):
        """Move the robot in speed mode.

        Args:
            current_position (list): New robot direction.

        Raises:
            InvalidOperationCode: Invalid operation code.
            InvalidStatusCode: Invalid status code.
            InvalidPackage: Invalid package code.

        Returns:
            any: Communicator response.
        """
        response = None
        # TODO: Will explode.

        return response

    def move_relative_base(self, steps, speed):
        """Move axis in relative mode.

        Args:
            steps (int): Axis steps.
            speed (int): Axis speed.

        Returns:
            any: Communicator response.
        """
        point = [steps, speed, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        return self.move_relative(point)

    def move_relative_shoulder(self, steps, speed):
        """Move axis in relative mode.

        Args:
            steps (int): Axis steps.
            speed (int): Axis speed.

        Returns:
            any: Communicator response.
        """
        point = [0, 0, steps, speed, 0, 0, 0, 0, 0, 0, 0, 0]
        return self.move_relative(point)

    def move_relative_elbow(self, steps, speed):
        """Move axis in relative mode.

        Args:
            steps (int): Axis steps.
            speed (int): Axis speed.

        Returns:
            any: Communicator response.
        """
        point = [0, 0, 0, 0, steps, speed, 0, 0, 0, 0, -steps, speed]
        return self.move_relative(point)

    def move_relative_r(self, steps, speed):
        """Move axis in relative mode.

        Args:
            steps (int): Axis steps.
            speed (int): Axis speed.

        Returns:
            any: Communicator response.
        """
        point = [0, 0, 0, 0, 0, 0, steps, speed, steps, speed, 0, 0]
        return self.move_relative(point)

    def move_relative_p(self, steps, speed):
        """Move axis in relative mode.

        Args:
            steps (int): Axis steps.
            speed (int): Axis speed.

        Returns:
            any: Communicator response.
        """
        point = [0, 0, 0, 0, 0, 0, steps, speed, -steps, speed, 0, 0]
        return self.move_relative(point)

    def move_relative_gripper(self, steps, speed):
        """Move axis in relative mode.

        Args:
            steps (int): Axis steps.
            speed (int): Axis speed.

        Returns:
            any: Communicator response.
        """
        point = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, steps, speed]
        return self.move_relative(point)

    def move_absolute_base(self, steps, speed):
        """Move axis in absolute mode.

        Args:
            steps (int): Axis steps.
            speed (int): Axis speed.

        Returns:
            any: Communicator response.
        """
        point = [steps, speed, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        return self.move_absolute(point)

    def move_absolute_shoulder(self, steps, speed):
        """Move axis in absolute mode.

        Args:
            steps (int): Axis steps.
            speed (int): Axis speed.

        Returns:
            any: Communicator response.
        """
        point = [0, 0, steps, speed, 0, 0, 0, 0, 0, 0, 0, 0]
        return self.move_absolute(point)

    def move_absolute_elbow(self, steps, speed):
        """Move axis in absolute mode.

        Args:
            steps (int): Axis steps.
            speed (int): Axis speed.

        Returns:
            any: Communicator response.
        """
        point = [0, 0, 0, 0, steps, speed, 0, 0, 0, 0, -steps, speed]
        return self.move_absolute(point)

    def move_absolute_r(self, steps, speed):
        """Move axis in absolute mode.

        Args:
            steps (int): Axis steps.
            speed (int): Axis speed.

        Returns:
            any: Communicator response.
        """
        point = [0, 0, 0, 0, 0, 0, steps, speed, steps, speed, 0, 0]
        return self.move_absolute(point)

    def move_absolute_p(self, steps, speed):
        """Move axis in absolute mode.

        Args:
            steps (int): Axis steps.
            speed (int): Axis speed.

        Returns:
            any: Communicator response.
        """
        point = [0, 0, 0, 0, 0, 0, steps, speed, -steps, speed, 0, 0]
        return self.move_absolute(point)

    def move_absolute_gripper(self, steps, speed):
        """Move axis in absolute mode.

        Args:
            steps (int): Axis steps.
            speed (int): Axis speed.

        Returns:
            any: Communicator response.
        """
        point = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, steps, speed]
        return self.move_absolute(point)

    def is_moving_cb(self, callback):
        """Is moving callback.

        Args:
            callback (function): Callable callback function.
        """
        self.__is_moving_cb = callback

#endregion
