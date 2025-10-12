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

from enum import Enum

from robko01.utils.logger import get_logger
from robko01.controllers.base import Robko01Base

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

class Joints(Enum):
    """Joint indexes."""

    All = -1
    Base = 0
    Shoulder = 1
    Elbow = 2
    LD = 3
    RD = 4
    Gripper = 5
    Pitch = 6
    Roll = 7

class Robko01(Robko01Base):
    """This class is dedicated to drive Robko01 TU-GAB driver."""

#region Attributes



#endregion

#region Constructor

    def __init__(self, **kwargs):

        super().__init__(kwargs)

        self.__logger = get_logger(__name__)

        self.__serial_port = None
        self.__PKG_LEN = 250
        self.__EnableMotor = "Enable motor"
        self.__DisableMotor = "Disable motor"
        self.__Drive = "Drive"
        self.__Direction = "Direction"
        self.__MotorFlag = "Motor Flag"
        self.__StepTime = "StepTime"
        self.__StepsNumber = "Steps Number"
        self.__CurrentStep = "Current Step"
        self.__CurrentTimeout = "Current Timeout"
        self.__CurrentEnable = "Current Enable"
        self.__CurrentDisable = "Current Disable"
        self.__CW = "+"
        self.__CCW = "-"

#endregion

#region Public methods

    def connect(self):
        """Connect to the robot controller.

        This delegates to the communicator's `connect` method.
        """

        self._communicator.connect()

    def disconnect(self):
        """Disconnect from the robot controller.

        Delegates to the communicator's `disconnect` method.
        """

        self._communicator.disconnect()

    # Get revision of the board.
    def get_revision(self):
        """Get board revision.

        Sends the `?RV` command to request the firmware/hardware revision.
        """

        command = "?RV"
        self._communicator.request(command)

    # Enable motor.
    def enable(self, joint=-1):
        """Enable motor(s) on the controller.

        Args:
            joint (int, optional): Joint index to enable (0-5). Use -1 to
                enable all joints. Special values `Joints.Pitch` and
                `Joints.Roll` will enable left/right motors together.
        """

        if joint == Joints.Pitch.value or joint == Joints.Roll.value:
            self.enable(Joints.LD.value)
            time.sleep(0.025)
            self.enable(Joints.RD.value)

        elif joint == -1:
            command = "?EA"
            self._communicator.request(command)

        elif joint <= 5 and joint >= 0:
            command = "{0}{1}".format("?E", joint)
            self._communicator.request(command)

    # Disable motor.
    def disable(self, joint=-1):
        """Disable motor(s) on the controller.

        Args:
            joint (int, optional): Joint index to disable (0-5). Use -1 to
                disable all joints. Special values `Joints.Pitch` and
                `Joints.Roll` will disable left/right motors together.
        """

        if joint == Joints.Pitch.value or joint == Joints.Roll.value:
            self.disable(Joints.LD.value)
            time.sleep(0.025)
            self.disable(Joints.RD.value)

        elif joint == -1:
            command = "?NA"
            self._communicator.request(command)

        elif joint <= 5 and joint >= 0:
            command = "{0}{1}".format("?N", joint)
            self._communicator.request(command)

    # Enable Elbow motor.
    def enable_elbow(self, state):
        """Enable or disable elbow and gripper motors.

        Args:
            state (bool): If True enable elbow and gripper; if False disable.
        """
        response = None
        if state:
            response += self.enable(Joints.Elbow.value)
            time.sleep(0.05)
            response += self.enable(Joints.Gripper.value)

        else:
            response += self.disable(Joints.Elbow.value)
            time.sleep(0.05)
            response += self.disable(Joints.Gripper.value)

        return response
    
    # Start single motor.
    def start_single(self, joint=-1):
        """Start a motor or all motors.

        Args:
            joint (int, optional): Joint index to start (0-5). Use -1 to start all.
        """
        response = None
        if joint <= 5 and joint >= 0:
            command = "{0}{1}".format("?S", joint)
            self._communicator.request(command)
        elif joint == -1:
            command = "?SA"
            self._communicator.request(command)

    # Start multiple motors.
    def start_multi(self, states):
        """Start multiple motors using a boolean state list.

        Args:
            states (sequence): Sequence with at least 6 boolean values. Each
                value indicates whether the corresponding motor should be
                started.
        """
        response = None
        if len(states) >= 6:
            indexes = ""

            for index in range(0, len(states)):
                if states[index] is True:
                    state = "1"
                else:
                    state = "0"

                indexes += state
                command = "{0}{1}".format("?SD", indexes)

                self._communicator.request(command)

    # Stop motor.
    def stop(self, joint=-1):
        """Stop a motor or all motors.

        Args:
            joint (int, optional): Joint index to stop (0-5). Use -1 to stop all.
        """
        response = None
        if joint <= 5 and joint >= 0:
            command = "{0}{1}".format("?P", joint)
            self._communicator.request(command)

        elif joint == -1:
            command = "?PA"
            self._communicator.request(command)

    # Read motor state.
    def read(self, joint=-1):
        """Read the state of a motor or all motors.

        Args:
            joint (int, optional): Joint index to query (0-5). Use -1 to query all.
        """
        response = None
        if joint <= 5 and joint >= 0:
            command = "{0}{1}".format("?R", joint)
            self._communicator.request(command)

        elif joint == -1:
            command = "?RA"
            self._communicator.request(command)

    # Set delay of the motor.
    def set_delay(self, joint, delay):
        """Set the delay (speed) parameter for a motor.

        Args:
            joint (int): Joint index (0-5).
            delay (int): Delay value used by the controller.
        """
        response = None
        if joint <= 5 and joint >= 0:
            command = "{0}{1}:{2}".format("?T", joint, str(delay).zfill(4))
            self._communicator.request(command)

    # Set steps of the motor.
    def set_steps(self, joint, steps):
        """Set the number of steps for a motor.

        Args:
            joint (int): Joint index (0-5).
            steps (int): Number of steps to set for the motor.
        """
        response = None
        if joint <= 5 and joint >= 0:
            command = "{0}{1}:{2}".format("?A", joint, str(steps).zfill(4))
            self._communicator.request(command)

    # Direction of the motor.
    def set_direction(self, joint, direction):
        """Set the rotation direction for a motor.

        Args:
            joint (int): Joint index (0-5).
            direction (str): '+' for clockwise or '-' for counter-clockwise.
        """
        response = None
        if joint <= 5 and joint >= 0 and (direction == self.__CW or direction == self.__CCW):
            command = "{0}{1}:{2}".format("?D", joint, direction)
            self._communicator.request(command)

    # Move the motor in relative mode.
    def _move_relative_impl(self, joint, delay, steps):
        """Perform single-joint relative movement.

        Args:
            joint (int): Joint index to move.
            delay (int): Delay parameter for the move.
            steps (int): Number of steps (can be negative for direction).

        Returns:
            any: Communicator response.
        """
        response = None
        # Special handling for Elbow -> uses joint index 2 and gripper coupling
        if joint == Joints.Elbow.value:
            direction = "+" if steps >= 0 else "-"
            steps_val = abs(steps)
            command = "{0}{1}:{2}{3}:{4}".format("?F", 2, direction, str(steps_val).zfill(4), str(delay).zfill(4))
            self._communicator.request(command)
            return None

        # Pitch/Roll map to LD/RD pairs
        if joint == Joints.Pitch.value:
            self._move_relative_impl(Joints.LD.value, delay, steps)
            time.sleep(0.05)
            self._move_relative_impl(Joints.RD.value, delay, steps)
            return None

        if joint == Joints.Roll.value:
            self._move_relative_impl(Joints.LD.value, delay, steps)
            time.sleep(0.05)
            self._move_relative_impl(Joints.RD.value, delay, -steps)
            return None

        # General joint handling
        direction = "+" if steps >= 0 else "-"
        steps_val = abs(steps)
        command = "{0}{1}:{2}{3}:{4}".format("?F", joint, direction, str(steps_val).zfill(4), str(delay).zfill(4))
        tmpdelay = int(abs(steps_val * delay * 2.5) / 1000)
        time.sleep(tmpdelay)
        self._communicator.request(command)
        return None

    def move_relative(self, *args):
        """Unified move_relative dispatcher.

        Accepts either a single sequence of positions (the new, unified API)
        or the old (joint, delay, steps) signature. Old-style calls are
        forwarded to `_move_relative_impl`.

        Args:
            *args: Either (positions_list,) or (joint, delay, steps)

        Raises:
            TypeError: If the call signature is invalid.
        """
        response = None
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            positions = args[0]
            if len(positions) >= 12:
                for joint_idx in range(6):
                    steps_val = positions[joint_idx * 2]
                    delay_val = positions[joint_idx * 2 + 1]
                    if steps_val != 0 or delay_val != 0:
                        self._move_relative_impl(joint_idx, delay_val, steps_val)
                return None
            else:
                raise TypeError("positions list must have at least 12 elements")
        elif len(args) == 3:
            return self._move_relative_impl(args[0], args[1], args[2])
        else:
            raise TypeError("move_relative expects either positions list or (joint,delay,steps)")

    #def move_relative(self, command):
    #    self.move_relative(command.joint, command.delay, command.steps)

#endregion

def calc_delay(steps, delay, time_offset):
    """Calculate a delay (in seconds) used between commands.

    Parameters
    ----------
    steps : int
        Number of steps to move.
    delay : int
        Delay parameter used by the controller.
    time_offset : int
        Additional offset (milliseconds) to add to the calculated delay.

    Returns
    -------
    int
        Delay value in seconds (rounded to integer) including the time_offset.
    """

    tmpdelay = int(abs(steps * delay * 2.5) / 1000) + time_offset
    return tmpdelay
