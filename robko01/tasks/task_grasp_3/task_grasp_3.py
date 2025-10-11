
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

from robko01.utils.utils import scale_speeds

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

__class_name__ = "TaskGrasp3"
"""Class name."""

#endregion

class TaskGrasp3(BaseTask):
    """Grasp 3"""

#region Constructor

    def __init__(self, **kwargs):

        super().__init__(kwargs)

        self.__logger = get_logger(__name__)
        """Logger
        """

#endregion

#region Public Methods

    def start(self):
        """Start the task."""

        self._start_cont()

        # Set the speed.
        speed = 100

        # Trajectory path.
        trajectory = [ \
            [450, 0, 600, 0, -400, 0, 200, 0, -200, 0, 400, 0], \
            [450, 0, 600, 0, -400, 0, 310, 0, -90, 0, 400, 0], \
            [450, 0, 700, 0, -400, 0, 310, 0, -90, 0, 400, 0], \
            [450, 0, 700, 0, -400, 0, 310, 0, -90, 0, 300, 0], \
            [450, 0, 600, 0, -400, 0, 310, 0, -90, 0, 300, 0], \
            [-450, 0, 600, 0, -400, 0, 110, 0, -290, 0, 300, 0], \
            [-450, 0, 700, 0, -400, 0, 110, 0, -290, 0, 300, 0], \
            [-450, 0, 700, 0, -400, 0, 110, 0, -290, 0, 400, 0], \
            [-450, 0, 600, 0, -400, 0, 110, 0, -290, 0, 400, 0], \
            #[-450, 0, 600, 0, -400, 0, 220, 0, -180, 0, 400, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] \
            ]

        for position in trajectory:
            print("Target:", position)
            current_position = scale_speeds(position, speed)
            print("Result:", current_position)
            self._controller.move_absolute(current_position)
            current_position = self._controller.current_position()
            print("Reach:", current_position)
            print("")

#endregion
