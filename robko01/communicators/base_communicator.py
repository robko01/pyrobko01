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

import serial

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

class BaseCommunicator:
    """Base communicator.
    """

#region Attributes

#endregion

#region Constructor

    def __init__(self):
        self.__timeout = 5
        """Timeout in second.
        """

#endregion

#region Properties

    @property
    def timeout(self):
        """Timeout

        Returns:
            float: Timeout value.
        """
        return self.__timeout

    @timeout.setter
    def timeout(self, value):
        """Timeout

        Args:
            value (float): Timeout value.
        """
        self.__timeout = value

#endregion

#region Public Methods

    def connect(self):
        """Connect to the device.
        """
        pass

    def disconnect(self):
        """Disconnect from device.
        """
        pass

    def reset(self):
        """Reset target device.
        """
        pass

    def send(self, payload):
        """Send
        """
        pass

    def receive(self):
        """Receive
        """
        pass

    def send_frame(self, req_frame):
        """Send frame.

        Args:
            req_frame (bytes): Request frame.
        """
        pass

#endregion
