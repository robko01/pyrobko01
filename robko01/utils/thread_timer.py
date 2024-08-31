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

import threading
import time

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

__class_name__ = "TaskGUI"
"""Task name."""

#endregion

class ThreadTimer():
    """Thread timer.
    """

#region Attributes

    __exit_event = None
    """Exit event.
    """

    __thread = None
    """GUI thread.
    """

    __update_rate = 0.1
    """Update rate in seconds.
    """

    __callback = None
    """Callback function.
    """

#endregion

#region Properties

    @property
    def update_rate(self):
        """Update rate.

        Returns:
            float: Update rate.
        """
        return self.__update_rate

    @update_rate.setter
    def update_rate(self, value):
        """Update rate.

        Args:
            value (float): Update rate.
        """
        self.__update_rate = value

#endregion

#region Constructor

    def __init__(self):

        pass

#endregion

#region Private Methods

    def __thread_worker(self):

        t0 = 0
        t1 = 0
        delta_t = 0

        while True:

            t1 = time.time()
            delta_t = t1 - t0
            if delta_t >= self.__update_rate:
                t0 = t1

                if self.__callback is not None:
                    self.__callback()

            if self.__exit_event.is_set():
                break

        if self.__exit_event is not  None:
            del self.__exit_event

        if self.__thread is not None:
            del self.__thread

#endregion

#region Public Methods

    def start(self):
        """Start the timer.
        """
        self.__exit_event = threading.Event()

        self.__thread = threading.Thread(target=self.__thread_worker)

        if self.__thread is not None:
            self.__thread.daemon = True
            self.__thread.start()

    def stop(self):
        """Stop the timer.
        """

        if self.__exit_event is not None:
            self.__exit_event.set()

        if self.__thread is not None:
            self.__thread.join()

    def set_cb(self, callback):
        """Set the callback of the timer.

        Args:
            callback (function): Callback function.
        """
        if callback is not None:
            self.__callback = callback

#endregion
