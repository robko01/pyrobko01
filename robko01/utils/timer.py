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

#endregion

class Timer():

#region Attributes

    __t0 = 0

    __t1 = 0

    __delta = 0

    __update_rate = 1

    __enable = False

    __cb = None

#endregion

#region Propertyes

    @property
    def update_rate(self):
        """Update rate.

        Returns:
            int: Update rate value.
        """
        return self.__update_rate

    @update_rate.setter
    def update_rate(self, value: int):
        """Update rate.

        Args:
            value (int): Update rate value.
        """        
        self.__update_rate = value


#endregion

#region Constructor

    def __init__(self):

        pass

#endregion

#region Public Methods

    def start(self):
        """Start the timer.
        """
        self.__enable = True

    def stop(self):
        """Stop the timer.
        """
        self.__enable = False

    def set_cb(self, callback):
        """Set callback.

        Args:
            callback (function): _description_
        """
        self.__cb = callback

    def update(self):
        """Update the timer.
        """
        if not self.__enable:
            return

        self.__t1 = time.time()

        self.__delta = self.__t1 - self.__t0

        if self.__delta >= self.update_rate:

            self.__t0 = self.__t1

            if self.__cb is not None:
                self.__cb()

#endregion
