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

from robko01.tasks.task_ui_qt.gui import GUI

from robko01.tasks.base_task import BaseTask

from robko01.utils.logger import get_logger

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, Orlin Dimitrov"
"""Copyrighted"""

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

__class_name__ = "TaskUI"
"""Task name."""

#endregion

class TaskUI(BaseTask):
    """UI tool."""

#region Attributes

#endregion

#region Constructor

    def __init__(self, **kwargs):
        super().__init__(kwargs)

        self._name = __class_name__

        self.__logger = get_logger(__name__)
        """Logger
        """

#endregion

#region Interface Methods

    def start(self):
        """Start the task."""

        self._start_cont()

        self.__ui = GUI(controller=self._controller)
        # self.__ui.setStyle('Fusion')
        self.__ui.start()
        self.__ui.exec()

    def stop(self):

        # self.__ui.stop()
        pass

#endregion
