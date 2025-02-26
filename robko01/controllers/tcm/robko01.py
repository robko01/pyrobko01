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

from robko01.controllers.base_robko01 import BaseRobko01

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

class Robko01(BaseRobko01):
    """This class is dedicated to control robot controller made by Orlin Dimitrov.
    """

#region Attributes

#endregion

#region Constructor

    def __init__(self, communicator):

        super().__init__()

        if communicator is None:
            raise ValueError("Communicator can not be None.")

        self.__communicator = communicator
        """Communicator
        """

        self.__is_moving_cb = None
        """Is moving callback.
        """
#endregion

#region Public Methods

    def connect(self):
        """Connect to the robot controller.
        """
        self.__communicator.connect()

    def disconnect(self):
        """Disconnect from robot controller.
        """
        self.__communicator.disconnect()

    def wait_to_stop(self):
        """Wait robot to stop moving.
        """
        response = self.is_moving()

        while response != 0:
            response = self.is_moving()

            time.sleep(self._sync_interval)

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

        while True:
            response = self.__pm.request(OpCode.Ping.value, payload)
            if response.is_valid():
                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.Ping.value:
                        break
                    else:
                        raise InvalidOperationCode("Operation code: {}".format(response.opcode))
                else:
                    raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                        StatusCode.to_text(response.status),\
                        OpCode.to_text(response.opcode)))
            else:
                raise InvalidPackage("Invalid package.")

            time.sleep(self._sync_interval)

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

        while True:
            response = self.__pm.request(OpCode.Stop.value)
            if response.is_valid():
                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.Stop.value:
                        break
                    else:
                        raise InvalidOperationCode("Operation code: {}".format(response.opcode))
                else:
                    raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                        StatusCode.to_text(response.status),\
                        OpCode.to_text(response.opcode)))
            else:
                raise InvalidPackage("Invalid package.")

            time.sleep(self._sync_interval)

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

        while True:
            response = self.__pm.request(OpCode.Disable.value)
            if response.is_valid():
                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.Disable.value:
                        break
                    else:
                        raise InvalidOperationCode("Operation code: {}".format(response.opcode))
                else:
                    raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                        StatusCode.to_text(response.status),\
                        OpCode.to_text(response.opcode)))
            else:
                raise InvalidPackage("Invalid package.")

            time.sleep(self._sync_interval)

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

        while True:
            response = self.__pm.request(OpCode.Enable.value)
            if response.is_valid():
                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.Enable.value:
                        break
                    else:
                        raise InvalidOperationCode("Operation code: {}".format(response.opcode))
                else:
                    raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                        StatusCode.to_text(response.status),\
                        OpCode.to_text(response.opcode)))
            else:
                raise InvalidPackage("Invalid package.")

            time.sleep(self._sync_interval)

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

        while True:
            response = self.__pm.request(OpCode.Clear.value)
            if response.is_valid():
                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.Clear.value:
                        break
                    else:
                        raise InvalidOperationCode("Operation code: {}".format(response.opcode))
                else:
                    raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                        StatusCode.to_text(response.status),\
                        OpCode.to_text(response.opcode)))
            else:
                raise InvalidPackage("Invalid package.")

            time.sleep(self._sync_interval)

        return response

    def move_relative(self, current_point):
        """Move relative to next robot position.

        Args:
            current_point (list): New robot position.

        Raises:
            InvalidOperationCode: Invalid operation code.
            InvalidStatusCode: Invalid status code.
            InvalidPackage: Invalid package code.

        Returns:
            any: Communicator response.
        """
        response = None

        while True:

            payload = pack("<hhhhhhhhhhhh",\
                int(current_point[0]), int(current_point[1]),\
                int(current_point[2]), int(current_point[3]),\
                int(current_point[4]), int(current_point[5]),\
                int(current_point[6]), int(current_point[7]),\
                int(current_point[8]), int(current_point[9]),\
                int(current_point[10]), int(current_point[11]))

            response = self.__pm.request(OpCode.MoveRelative.value, payload)
            if response.is_valid():

                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.MoveRelative.value:
                        break
                    else:
                        raise InvalidOperationCode("Operation code: {}".format(response.opcode))

                elif response.status == StatusCode.Busy.value:
                    break

                else:
                    raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                        StatusCode.to_text(response.status),\
                        OpCode.to_text(response.opcode)))
            else:
                raise InvalidPackage("Invalid package.")

        return response

    def move_absolute(self, current_point):
        """Move absolute to next robot position.

        Args:
            current_point (_type_): _description_

        Raises:
            InvalidOperationCode: Invalid operation code.
            InvalidStatusCode: Invalid status code.
            InvalidPackage: Invalid package code.

        Returns:
            any: Communicator response.
        """

        steps = current_point[0:12:2]
        speed = max(current_point[1:12:2])

        d = abs(int(speed))
        q1 = round(steps[0], 0)
        q2 = round(steps[1], 0)
        q3 = round(steps[2], 0)
        q4 = round(steps[3], 0)
        q5 = round(steps[4], 0)
        q6 = int(0)
        command = f"@STEP {d},{q1},{q2},{q3},{q4+q5},{q4-q5},{q6},0\r".encode('ASCII')
        self.__communicator.send_frame(command)
        print(f"Command: {command}")

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

        while True:

            response = self.__pm.request(OpCode.IsMoving.value)

            if response.is_valid():
                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.IsMoving.value:
                        value = response.payload
                        result = value[0]
                        break
                    else:
                        raise InvalidOperationCode("Operation code: {}".format(response.opcode))
                else:
                    raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                        StatusCode.to_text(response.status),\
                        OpCode.to_text(response.opcode)))
            else:
                raise InvalidPackage("Invalid package.")

            time.sleep(self._sync_interval)

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

        while True:
            response = self.__pm.request(OpCode.CurrentPosition.value)
            if response.is_valid():
                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.CurrentPosition.value:
                        value = response.payload
                        position = unpack("<hhhhhhhhhhhh", bytes(value))
                        break
                    else:
                        raise InvalidOperationCode("Operation code: {}".format(response.opcode))
                else:
                    raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                        StatusCode.to_text(response.status),\
                        OpCode.to_text(response.opcode)))
            else:
                raise InvalidPackage("Invalid package.")

            time.sleep(self._sync_interval)

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

        while True:

            response = self.__pm.request(OpCode.DI.value)

            if response.is_valid():
                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.DI.value:
                        value = response.payload[0]
                        break
                    else:
                        raise InvalidOperationCode("Operation code: {}".format(response.opcode))
                else:
                    raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                        StatusCode.to_text(response.status),\
                        OpCode.to_text(response.opcode)))
            else:
                raise InvalidPackage("Invalid package.")

            time.sleep(self._sync_interval)

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

        while True:
            response = self.__pm.request(OpCode.DO.value, [value])

            if response.is_valid():
                if response.status == StatusCode.Ok.value:
                    if response.opcode == OpCode.DO.value:
                        response_value = response.payload[0]
                        arr = [int(x) for x in bin(response_value)[2:]]
                        break
                    else:
                        raise InvalidOperationCode("Operation code: {}".format(response.opcode))
                else:
                    raise InvalidStatusCode("Status: {}; OpCode: {}".format(\
                        StatusCode.to_text(response.status),\
                        OpCode.to_text(response.opcode)))
            else:
                raise InvalidPackage("Invalid package.")

            time.sleep(self._sync_interval)

        return arr

    def is_moving_cb(self, callback):
        """Is moving callback.

        Args:
            callback (function): Callable callback function.
        """
        self.__is_moving_cb = callback

#endregion
