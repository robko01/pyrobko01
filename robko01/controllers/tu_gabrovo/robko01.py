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
import serial

from robko01.utils.logger import get_logger
from robko01.controllers.base_robko01 import BaseRobko01

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

class Robko01(BaseRobko01):
    """This class is dedicated to drive Robko01 TU-GAB driver."""

#region Attributes



#endregion

#region Constructor

    def __init__(self, communicator):

        super().__init__()

        if communicator is None:
            raise ValueError("Communicator can not be None.")

        self.__logger = get_logger(__name__)

        self.__communicator = communicator

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
        """Connect to the robot controller."""

        self.__communicator.connect()

    def disconnect(self):
        """Disconnect from robot controller."""

        self.__communicator.disconnect()

    def wait_for_controller(self):
        """WAit for robot controller to become active."""

        response = None

        times = 0
        while True:
            response = self.get_revision()
            if response:
                break

            times += 1
            if times > self.timeout:
                raise TimeoutError("Controller does not respond.")

            time.sleep(self._sync_interval)

        return response

    # Get revision of the board.
    def get_revision(self):
        command = "?RV"
        self.__communicator.request(command)

    # Enable motor.
    def enable(self, joint=-1):

        if joint == Joints.Pitch.value or joint == Joints.Roll.value:
            self.enable(Joints.LD.value)
            time.sleep(0.025)
            self.enable(Joints.RD.value)

        elif joint == -1:
            command = "?EA"
            self.__communicator.request(command)

        elif joint <= 5 and joint >= 0:
            command = "{0}{1}".format("?E", joint)
            self.__communicator.request(command)

    # Disable motor.
    def disable(self, joint=-1):

        if joint == Joints.Pitch.value or joint == Joints.Roll.value:
            self.disable(Joints.LD.value)
            time.sleep(0.025)
            self.disable(Joints.RD.value)

        elif joint == -1:
            command = "?NA"
            self.__communicator.request(command)

        elif joint <= 5 and joint >= 0:
            command = "{0}{1}".format("?N", joint)
            self.__communicator.request(command)

    # Enable Elbow motor.
    def enable_elbow(self, state):

        if state:
            self.enable(Joints.Elbow.value)
            time.sleep(0.05)
            self.enable(Joints.Gripper.value)

        else:
            self.disable(Joints.Elbow.value)
            time.sleep(0.05)
            self.disable(Joints.Gripper.value)

    # Start single motor.
    def start_single(self, joint=-1):
        if joint <= 5 and joint >= 0:
            command = "{0}{1}".format("?S", joint)
            self.__communicator.request(command)
        elif joint == -1:
            command = "?SA"
            self.__communicator.request(command)

    # Start multiple motors.
    def start_multi(self, states):

        if len(states) >= 6:
            indexes = ""

            for index in range(0, len(states)):
                if states[index] is True:
                    state = "1"
                else:
                    state = "0"

                indexes += state
                command = "{0}{1}".format("?SD", indexes)

                self.__communicator.request(command)

    # Stop motor.
    def stop(self, joint=-1):

        if joint <= 5 and joint >= 0:
            command = "{0}{1}".format("?P", joint)
            self.__communicator.request(command)

        elif joint == -1:
            command = "?PA"
            self.__communicator.request(command)

    # Read motor state.
    def read(self, joint=-1):

        if joint <= 5 and joint >= 0:
            command = "{0}{1}".format("?R", joint)
            self.__communicator.request(command)

        elif joint == -1:
            command = "?RA"
            self.__communicator.request(command)

    # Set delay of the motor.
    def set_delay(self, joint, delay):

        if joint <= 5 and joint >= 0:
            command = "{0}{1}:{2}".format("?T", joint, str(delay).zfill(4))
            self.__communicator.request(command)

    # Set steps of the motor.
    def set_steps(self, joint, steps):

        if joint <= 5 and joint >= 0:
            command = "{0}{1}:{2}".format("?A", joint, str(steps).zfill(4))
            self.__communicator.request(command)

    # Direction of the motor.
    def set_direction(self, joint, direction):

        if joint <= 5 and joint >= 0 and (direction == self.__CW or direction == self.__CCW):
            command = "{0}{1}:{2}".format("?D", joint, direction)
            self.__communicator.request(command)

    # Move the motor in relative mode.
    def move_relative(self, joint, delay, steps):

        if joint == Joints.Elbow.value:

            direction = ""
            if steps >= 0:
                direction = "+"
            else:
                direction = "-"
            steps = abs(steps)

            command = "{0}{1}:{2}{3}:{4}"\
                .format("?F", 2, direction, str(steps).zfill(4), str(delay).zfill(4))
            self.__communicator.request(command)
            time.sleep(0.05)
            command = "{0}{1}:{2}{3}:{4}"\
                .format("?F", 5, direction, str(steps).zfill(4), str(delay).zfill(4))
            self.move_relative(Joints.Gripper.value, delay, steps)

        if joint == Joints.Pitch.value:
            self.move_relative(Joints.LD.value, delay, steps)
            time.sleep(0.05)
            self.move_relative(Joints.RD.value, delay, steps)

        elif joint == Joints.Roll.value:
            self.move_relative(Joints.LD.value, delay, steps)
            time.sleep(0.05)
            self.move_relative(Joints.RD.value, delay, -steps)

        else:
            direction = ""
            if steps >= 0:
                direction = "+"
            else:
                direction = "-"
            steps = abs(steps)

            command = "{0}{1}:{2}{3}:{4}"\
                .format("?F", joint, direction, str(steps).zfill(4), str(delay).zfill(4))
            # delay sleep
            tmpdelay = int(abs(steps * delay * 2.5) / 1000)
            time.sleep(tmpdelay)
            self.__communicator.request(command)

    #def move_relative(self, command):
    #    self.move_relative(command.joint, command.delay, command.steps)

#endregion

def calc_delay(steps, delay, time_offset):
    tmpdelay = int(abs(steps * delay * 2.5) / 1000) + time_offset
    return tmpdelay
