
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

__class_name__ = "TaskGrasp1"
"""Task name."""

#endregion

class TaskGrasp1(BaseTask):
    """Task Grasp 1
    """

#region Public Methods

    def start(self):
        """Start the task."""

        self._start_cont()

        # Set the speed.
        speed = 100

        # Trajectory but like commands.
        self._controller.move_relative_base(450, speed)
        self._controller.move_relative_shoulder(600, speed)
        self._controller.move_relative_p(200, speed)
        self._controller.move_relative_elbow(-400, speed)
        self._controller.move_relative_r(110, speed)
        self._controller.move_relative_shoulder(100, speed)
        self._controller.move_relative_gripper(-10, speed)
        self._controller.move_relative_shoulder(-100, speed)
        self._controller.move_relative_base(-900, speed)
        self._controller.move_relative_r(-220, speed)
        self._controller.move_relative_shoulder(100, speed)
        self._controller.move_relative_shoulder(-100, speed)
        self._controller.move_relative_r(110, speed)
        self._controller.move_relative_elbow(400, speed)
        self._controller.move_relative_p(-200, speed)
        self._controller.move_relative_shoulder(-600, speed)
        self._controller.move_relative_base(450, speed)

#endregion
