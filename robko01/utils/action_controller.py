#!/usr/bin/env python
# -*- coding: utf8 -*-

"""

Robko 01 - Python Controlftware

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

import queue

from robko01.utils.thread_timer import ThreadTimer

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

class ActionController():
    """Action controller dispatcher.
    """

#region Constructor

    def __init__(self):
        self.__actions_queue = queue.Queue()
        """Actions queue.
        """

        self.__action_update_timer = ThreadTimer("Action controller queue update timer.")
        """Action update timer.
        """
        self.__action_update_timer.update_rate = 0.1 # Update time!
        self.__action_update_timer.set_cb(self.__action_timer_cb)

        self.__action_cb = None
        """Action callback.
        """

#endregion

#region Private Methods

    def __action_timer_cb(self):
        if not self.__actions_queue.empty():
            action = self.__actions_queue.get()
            if self.__action_cb is not None:
                self.__action_cb(action)

#endregion

#region Public Methods

    def set_action_cb(self, cb):
        """Set action callback function.

        Args:
            cb (function): Callback function.
        """
        if cb is not None:
            self.__action_cb = cb

    def add_action(self, action: dict):
        """Add action to the queue.

        Args:
            action (dict): Dictionary made of action and action type.
        """
        #ugly make it OOP.
        self.__actions_queue.put(action)

    def start(self):
        """Start the action to be executed from the queue.
        """
        self.__action_update_timer.start()

    def stop(self):
        """Stop the action to be executed from the queue.
        """
        self.__action_update_timer.stop()

#endregion
