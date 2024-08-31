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

from robko01.tasks.base_task import BaseTask

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

__class_name__ = "TaskCmd"
"""Task name."""

#endregion

class TaskCmd(BaseTask):
    """Command line test tool."""

#region Attributes

#endregion

    def __init__(self, **kwargs):

        super().__init__(kwargs)

        self._name = __class_name__

        self.__logger = get_logger(__name__)
        """Logger
        """

#region Public Methods

    def start(self):
        """Start the task."""

        self._start_cont()

        poses = []

        while not self._stop_flag:

            self.__logger.info("")
            command = input("Enter command: ")
            command = command.lower()

            if command == "exit":
                self.stop()
                break

            if "base" == command or "0" == command:
                steps = input("Enter steps: ")
                speed = input("Enter speed: ")

                if steps == "":
                    steps = "10"

                if speed == "":
                    speed = "10"

                steps = int(steps.lower())
                speed = int(speed.lower())

                self.__logger.info("Execute %s @ %d steps and %d speed." % (command, steps, speed))

                self._controller.move_relative_base(steps, speed)

            elif "shoulder" == command or "1" == command:
                steps = input("Enter steps: ")
                speed = input("Enter speed: ")

                if steps == "":
                    steps = "10"

                if speed == "":
                    speed = "10"

                steps = int(steps.lower())
                speed = int(speed.lower())

                self.__logger.info("Execute %s @ %d steps and %d speed." % (command, steps, speed))

                self._controller.move_relative_shoulder(steps, speed)

            elif "elbow" == command or "2" == command:
                steps = input("Enter steps: ")
                speed = input("Enter speed: ")

                if steps == "":
                    steps = "10"

                if speed == "":
                    speed = "10"

                steps = int(steps.lower())
                speed = int(speed.lower())

                self.__logger.info("Execute %s @ %d steps and %d speed." % (command, steps, speed))

                self._controller.move_relative_elbow(steps, speed)

            elif "p" == command or "3" == command:
                steps = input("Enter steps: ")
                speed = input("Enter speed: ")

                if steps == "":
                    steps = "10"

                if speed == "":
                    speed = "10"

                steps = int(steps.lower())
                speed = int(speed.lower())


                self.__logger.info("Execute %s @ %d steps and %d speed." % (command, steps, speed))

                self._controller.move_relative_p(steps, speed)

            elif "r" == command or "4" == command:
                steps = input("Enter steps: ")
                speed = input("Enter speed: ")

                if steps == "":
                    steps = "10"

                if speed == "":
                    speed = "10"

                steps = int(steps.lower())
                speed = int(speed.lower())

                self.__logger.info("Execute %s @ %d steps and %d speed." % (command, steps, speed))

                self._controller.move_relative_r(steps, speed)

            elif "gripper" == command or "5" == command:
                steps = input("Enter steps: ")
                speed = input("Enter speed: ")

                if steps == "":
                    steps = "10"

                if speed == "":
                    speed = "10"

                steps = int(steps.lower())
                speed = int(speed.lower())

                self.__logger.info("Execute %s @ %d steps and %d speed." % (command, steps, speed))

                self._controller.move_relative_gripper(steps, speed)

            elif command == "pos":

                current_point = self._controller.current_position()
                self.__logger.info("Current position:", current_point)

            elif command == "add_c_pos":

                current_point = self._controller.current_position()
                self.__logger.info("Current position:", current_point)
                poses.append(current_point)

            elif command == "ls_pos":

                self.__logger.info("Current positions:")
                self.__logger.info(poses)

            else:
                self.__logger.info("Invalid command: {}".format(command))

#endregion
