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

from robko01.utils.utils import scale_speeds

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

__class_name__ = "TaskGrasp2"
"""Task name."""

#endregion

class TaskGrasp2(BaseTask):
    """Grasp 2"""

    

    def __init__(self, **kwargs):

        super().__init__(kwargs)

        self._name = __class_name__
    
        self.__logger = get_logger(__name__)
        """Logger
        """

#region Private Methods

    def __is_move_cb(self, result):

        msg = "Is moving: {:08b}".format(result)
        self.__logger.debug(msg)

#endregion

#region Public Methods

    def start(self):
        """Start the task."""

        self.__logger.debug("Starting")

        self._start_cont()
        self._controller.is_moving_cb(self.__is_move_cb)

        self.__logger.debug("Started")

        # Set the speed.
        speed = 150

        # Trajectory path.
        trajectory = [ \
            [450, 0, 600, 0, -400, 0, 200, 0, -200, 0, 400, 0], \
            [0, 0, 0, 0, 0, 0, 110, 0, 110, 0, 0, 0], \
            [0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -100, 0], \
            [0, 0, -100, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [-900, 0, 0, 0, 0, 0, -200, 0, -200, 0, 0, 0], \
            [0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0], \
            [0, 0, -100, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 110, 0, 110, 0, 0, 0], \
            [450, 0, -600, 0, 400, 0, -220, 0, 180, 0, -400, 0] \
            ]

        command = ""
        for position in trajectory:
            if self._execution_mode == "1":
                command = input("Press Enter to continue or type command: ")
                print("Command: {}".format(command))

            command = command.lower()

            if command == "continue":
                self._execution_mode = "2"

            elif command == "home":
                self._controller.move_absolute([0, 300, 0, 300, 0, 300, 0, 300, 0, 300, 0, 300])
                break

            self.__logger.debug("Target: {}".format(position))
            current_point = scale_speeds(position, speed)
            self.__logger.debug("Result: {}".format(current_point))
            self._controller.move_relative(current_point)
            current_point = self._controller.current_position()
            self.__logger.debug("Reach: {}".format(current_point))
            self.__logger.debug("")

        self._controller.wait_to_stop()

        self.__logger.debug("End")

#endregion
