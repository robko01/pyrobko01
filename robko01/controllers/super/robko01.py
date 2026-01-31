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

from robko01.controllers.super.protocol.package_manager import PackageManager
from robko01.controllers.super.op_code import OpCode
from robko01.controllers.super.status_code import StatusCode
from robko01.controllers.base import Robko01Base
from robko01.controllers.super.exceptions.controller_is_busy import ControllerIsBusy
from robko01.controllers.super.exceptions.invalid_package import InvalidPackage
from robko01.controllers.super.exceptions.invalid_operation_code import InvalidOperationCode
from robko01.controllers.super.exceptions.invalid_status_code import InvalidStatusCode

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

class Robko01(Robko01Base):
    """SUPER protocol controller implementation."""

#region Attributes

#endregion

#region Constructor

    def __init__(self, **kwargs):

        super().__init__(kwargs)

        self.__pm = PackageManager(self._communicator)
        """Package manager.
        """

        self.__is_moving_cb = None
        """Is moving callback.
        """
#endregion

#region Public Methods

    def connect(self):
        """Connect to the robot controller.
        """
        time.sleep(1.0)
        self._communicator.connect()
        time.sleep(1.0)

    def disconnect(self):
        """Disconnect from robot controller.
        """
        self._communicator.disconnect()

    def is_connected(self) -> bool:
        """Return True if controller is currently connected."""
        return self._communicator.is_connected()

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
        response = self.__pm.request(OpCode.Ping.value, payload)
        if response.is_valid():
            if response.status == StatusCode.Ok.value:
                if response.opcode == OpCode.Ping.value:
                    pass
                else:
                    raise InvalidOperationCode("Operation code: {}".format(response.opcode))
            else:
                raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                    StatusCode.to_text(response.status),\
                    OpCode.to_text(response.opcode)))
        else:
            raise InvalidPackage("Invalid package.")

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
        response = self.__pm.request(OpCode.Stop.value)
        if response.is_valid():
            if response.status == StatusCode.Ok.value:
                if response.opcode == OpCode.Stop.value:
                    pass
                else:
                    raise InvalidOperationCode("Operation code: {}".format(response.opcode))
            else:
                raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                    StatusCode.to_text(response.status),\
                    OpCode.to_text(response.opcode)))
        else:
            raise InvalidPackage("Invalid package.")

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
        response = self.__pm.request(OpCode.Disable.value)
        if response.is_valid():
            if response.status == StatusCode.Ok.value:
                if response.opcode == OpCode.Disable.value:
                    pass
                else:
                    raise InvalidOperationCode("Operation code: {}".format(response.opcode))
            else:
                raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                    StatusCode.to_text(response.status),\
                    OpCode.to_text(response.opcode)))
        else:
            raise InvalidPackage("Invalid package.")

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

        response = self.__pm.request(OpCode.Enable.value)
        if response.is_valid():
            if response.status == StatusCode.Ok.value:
                if response.opcode == OpCode.Enable.value:
                    pass
                else:
                    raise InvalidOperationCode("Operation code: {}".format(response.opcode))
            else:
                raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                    StatusCode.to_text(response.status),\
                    OpCode.to_text(response.opcode)))
        else:
            raise InvalidPackage("Invalid package.")

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

        response = self.__pm.request(OpCode.Clear.value)
        if response.is_valid():
            if response.status == StatusCode.Ok.value:
                if response.opcode == OpCode.Clear.value:
                    pass
                else:
                    raise InvalidOperationCode("Operation code: {}".format(response.opcode))
            else:
                raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                    StatusCode.to_text(response.status),\
                    OpCode.to_text(response.opcode)))
        else:
            raise InvalidPackage("Invalid package.")

        return response

    def _move_relative_impl(self, target_position):
        """Move relative to next robot position.

        Args:
            target_position (list): New robot position.

        Raises:
            InvalidOperationCode: Invalid operation code.
            InvalidStatusCode: Invalid status code.
            InvalidPackage: Invalid package code.

        Returns:
            any: Communicator response.
        """
        response = None

        payload = pack("<hhhhhhhhhhhh",\
            int(target_position[0]), int(target_position[1]),\
            int(target_position[2]), int(target_position[3]),\
            int(target_position[4]), int(target_position[5]),\
            int(target_position[6]), int(target_position[7]),\
            int(target_position[8]), int(target_position[9]),\
            int(target_position[10]), int(target_position[11]))
        response = self.__pm.request(OpCode.MoveRelative.value, payload)
        if response.is_valid():
            if response.status == StatusCode.Ok.value:
                if response.opcode == OpCode.MoveRelative.value:
                    pass
                else:
                    raise InvalidOperationCode("Operation code: {}".format(response.opcode))
            elif response.status == StatusCode.Busy.value:
                raise ControllerIsBusy("The controller is busy.")
            else:
                raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                    StatusCode.to_text(response.status),\
                    OpCode.to_text(response.opcode)))
        else:
            raise InvalidPackage("Invalid package.")

        return response

    # wrapper supports both unified and legacy signatures
    def move_relative(self, *args):
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            return self._move_relative_impl(args[0])
        elif len(args) == 3:
            joint, delay, steps = args
            point = [0] * 12
            idx = int(joint) * 2
            if 0 <= idx < 12:
                point[idx] = steps
                point[idx + 1] = delay
            return self._move_relative_impl(point)
        else:
            raise TypeError("move_relative expects either positions list or (joint,delay,steps)")

    def move_absolute(self, target_position):
        """Move absolute to next robot position.

        Args:
            target_position (_type_): _description_

        Raises:
            InvalidOperationCode: Invalid operation code.
            InvalidStatusCode: Invalid status code.
            InvalidPackage: Invalid package code.

        Returns:
            any: Communicator response.
        """
        response = None
        payload = pack("<hhhhhhhhhhhh",\
            int(target_position[0]), int(target_position[1]),\
            int(target_position[2]), int(target_position[3]),\
            int(target_position[4]), int(target_position[5]),\
            int(target_position[6]), int(target_position[7]),\
            int(target_position[8]), int(target_position[9]),\
            int(target_position[10]), int(target_position[11]))
        response = self.__pm.request(OpCode.MoveAbsolute.value, payload)
        if response.is_valid():
            if response.status == StatusCode.Ok.value:
                if response.opcode == OpCode.MoveAbsolute.value:
                    pass
                else:
                    raise InvalidOperationCode("Operation code: {}".format(response.opcode))
            elif response.status == StatusCode.Busy.value:
                raise ControllerIsBusy("The controller is busy.")
            else:
                raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                    StatusCode.to_text(response.status),\
                    OpCode.to_text(response.opcode)))
        else:
            raise InvalidPackage("Invalid package.")

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
        response = None
        result = 0
        response = self.__pm.request(OpCode.IsMoving.value)
        if response.is_valid():
            if response.status == StatusCode.Ok.value:
                if response.opcode == OpCode.IsMoving.value:
                    value = response.payload
                    result = value[0]
                    pass
                else:
                    raise InvalidOperationCode("Operation code: {}".format(response.opcode))
            else:
                raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                    StatusCode.to_text(response.status),\
                    OpCode.to_text(response.opcode)))
        else:
            raise InvalidPackage("Invalid package.")

        if self.__is_moving_cb is not None:
            self.__is_moving_cb(result)

        return result

    def current_position(self):
        """Current robot position.

        Raises:
            InvalidOperationCode: Invalid operation code.
            InvalidStatusCode: Invalid status code.
            InvalidPackage: Invalid package code.

        Returns:
            list: Robot positions.
        """
        response = None
        position = None
        response = self.__pm.request(OpCode.CurrentPosition.value)
        if response.is_valid():
            if response.status == StatusCode.Ok.value:
                if response.opcode == OpCode.CurrentPosition.value:
                    value = response.payload
                    position = unpack("<hhhhhhhhhhhh", bytes(value))
                    pass
                else:
                    raise InvalidOperationCode("Operation code: {}".format(response.opcode))
            else:
                raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                    StatusCode.to_text(response.status),\
                    OpCode.to_text(response.opcode)))
        else:
            raise InvalidPackage("Invalid package.")

        return position

    def get_inputs(self):
        """Current robot inputs.

        Raises:
            InvalidOperationCode: Invalid operation code.
            InvalidStatusCode: Invalid status code.
            InvalidPackage: Invalid package code.

        Returns:
            list: Inputs of the robot.
        """
        response = None
        value = None
        response = self.__pm.request(OpCode.DI.value)
        if response.is_valid():
            if response.status == StatusCode.Ok.value:
                if response.opcode == OpCode.DI.value:
                    value = response.payload[0]
                    pass
                else:
                    raise InvalidOperationCode("Operation code: {}".format(response.opcode))
            else:
                raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                    StatusCode.to_text(response.status),\
                    OpCode.to_text(response.opcode)))
        else:
            raise InvalidPackage("Invalid package.")

        return value

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
        response = self.__pm.request(OpCode.DO.value, [value])
        if response.is_valid():
            if response.status == StatusCode.Ok.value:
                if response.opcode == OpCode.DO.value:
                    response_value = response.payload[0]
                    arr = [int(x) for x in bin(response_value)[2:]]
                    pass
                else:
                    raise InvalidOperationCode("Operation code: {}".format(response.opcode))
            else:
                raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                    StatusCode.to_text(response.status),\
                    OpCode.to_text(response.opcode)))
        else:
            raise InvalidPackage("Invalid package.")

        return arr

    def move_speed(self, target_position):
        """Move the robot in speed mode.

        Args:
            target_position (list): New robot direction.

        Raises:
            InvalidOperationCode: Invalid operation code.
            InvalidStatusCode: Invalid status code.
            InvalidPackage: Invalid package code.

        Returns:
            any: Communicator response.
        """
        response = None

        payload = pack("<hhhhhhhhhhhh",\
            target_position[0], target_position[1],\
            target_position[2], target_position[3],\
            target_position[4], target_position[5],\
            target_position[6], target_position[7],\
            target_position[8], target_position[9],\
            target_position[10], target_position[11])
        response = self.__pm.request(OpCode.MoveSpeed.value, payload)
        if response.is_valid():
            if response.status == StatusCode.Ok.value:
                if response.opcode == OpCode.MoveSpeed.value:
                    pass
                else:
                    raise InvalidOperationCode("Operation code: {}".format(response.opcode))
            elif response.status == StatusCode.Busy.value:
                raise ControllerIsBusy("The controller is busy.")
            else:
                raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                    StatusCode.to_text(response.status),\
                    OpCode.to_text(response.opcode)))
        else:
            raise InvalidPackage("Invalid package.")

        return response

    def move_interpolated(self, j1=0, j2=0, j3=0, j4=0, j5=0, j6=0) -> int:
        """Interpolated joint move. Returns duration in ms."""
        payload = pack("<hhhhhh", int(j1), int(j2), int(j3), int(j4), int(j5), int(j6))
        response = self.__pm.request(OpCode.MoveInterpolated.value, payload)
        if response.is_valid():
            if response.status == StatusCode.Ok.value:
                if response.opcode == OpCode.MoveInterpolated.value:
                    if response.payload and len(response.payload) >= 4:
                        return int(unpack("<I", bytes(response.payload[:4]))[0])
                    return -1
                else:
                    raise InvalidOperationCode("Operation code: {}".format(response.opcode))
            elif response.status == StatusCode.Busy.value:
                raise ControllerIsBusy("The controller is busy.")
            else:
                raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                    StatusCode.to_text(response.status),\
                    OpCode.to_text(response.opcode)))
        else:
            raise InvalidPackage("Invalid package.")

    def move_ik(self, x=0, y=0, z=0, pitch=0, roll=0, gripper=0) -> int:
        """Inverse kinematics move. Returns duration in ms."""
        payload = pack("<hhhhhh", int(x), int(y), int(z), int(pitch), int(roll), int(gripper))
        response = self.__pm.request(OpCode.MoveIK.value, payload)
        if response.is_valid():
            if response.status == StatusCode.Ok.value:
                if response.opcode == OpCode.MoveIK.value:
                    if response.payload and len(response.payload) >= 4:
                        return int(unpack("<I", bytes(response.payload[:4]))[0])
                    return -1
                else:
                    raise InvalidOperationCode("Operation code: {}".format(response.opcode))
            elif response.status == StatusCode.Busy.value:
                raise ControllerIsBusy("The controller is busy.")
            else:
                raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                    StatusCode.to_text(response.status),\
                    OpCode.to_text(response.opcode)))
        else:
            raise InvalidPackage("Invalid package.")

    def get_interpolator_state(self):
        """Get interpolator state and progress."""
        response = self.__pm.request(OpCode.GetInterpolatorState.value)
        if response.is_valid():
            if response.status == StatusCode.Ok.value:
                if response.opcode == OpCode.GetInterpolatorState.value:
                    if response.payload and len(response.payload) >= 5:
                        state = int(response.payload[0])
                        progress = unpack("<f", bytes(response.payload[1:5]))[0]
                        return {"state": state, "progress": progress}
                    return {"state": 0, "progress": 0.0}
                else:
                    raise InvalidOperationCode("Operation code: {}".format(response.opcode))
            else:
                raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                    StatusCode.to_text(response.status),\
                    OpCode.to_text(response.opcode)))
        else:
            raise InvalidPackage("Invalid package.")

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
