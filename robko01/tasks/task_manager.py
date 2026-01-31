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

import os
import importlib

from enum import Enum

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


__maintainer__ = "Orlin Dimitrov"
"""Name of the maintainer."""

__email__ = "robko01@8bitclub.com"
"""E-mail of the author."""

__status__ = "Debug"
"""File status."""

#endregion

class TaskManager:
    """This class handles the robot tasks in nice procedure way.
    """

#region Attributes

    __logger = None
    """Logger"""

    __controller = None
    """Robot controller."""

    __task = None
    """The task."""

#endregion

#region Properties

#endregion

#region Constructor

    def __init__(self, **kwargs):
        """Constructor
        """
        self.__logger = get_logger(__name__)

        if "controller" in kwargs:
            self.__controller = kwargs["controller"]

#endregion

#region Private Methods

    def __load_task(self, task_name):
        """Load the task.
        Args:
            task_name (str): Name of the task.
        Raises:
            ImportError: Raise when module can not me imported.
            ModuleNotFoundError: Raise when module can not be found.
            AttributeError: Not existing attribute.
            ValueError: Attribute __class_name__ is not set properly.
        Returns:
            [mixed]: Instance of the class module.
        """

        module_path = f"robko01.tasks.{task_name}.{task_name}"

        module = importlib.import_module(module_path)
        if module is None:
            raise ImportError("{}".format(module_path))

        if not hasattr(module, "__class_name__"):
            raise AttributeError(f"Module: {module_path}, has no attribute __class_name__.")

        if module.__class_name__ == "":
            raise ValueError(f"Module: {module_path}.__class_name__ is empty.")

        class_module = getattr(module, module.__class_name__)
        if class_module is None:
            raise ModuleNotFoundError(f"{module_path}.{module.__class_name__}")

        class_isinstance = class_module(controller=self.__controller)

        return class_isinstance

#endregion

#region Public Methods

    def list_tasks(self):
        """List the existing tasks.

        Returns:
            list: Names of the plugins
        """

        list_of_dirs = []

        dir_path = os.path.dirname(os.path.realpath(__file__))

        dirs = os.listdir(dir_path)
        for item in dirs:

            if item.startswith("__"):
                continue

            if item == "task_template":
                continue

            plugin_path = os.path.join(dir_path, item)

            if os.path.isdir(plugin_path):
                list_of_dirs.append(item)

        return list_of_dirs

    def start(self, start):
        """Start the task.

        Args:
            start (str): Task folder name.
        """

        self.stop()

        if self.__task is None:
            self.__task = self.__load_task(start)

        if self.__task is not None:
            self.__logger.info("Starting task: {}".format(self.__task.name))
            self.__task.start()
            self.__logger.info("Ending task: {}".format(self.__task.name))

    def stop(self):
        """Stop the task.
        """

        if self.__task is not None:
            self.__logger.info("Stopping task: {}".format(self.__task.name))
            self.__task.stop()

#endregion
