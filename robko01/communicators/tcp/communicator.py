
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

import socket

from robko01.utils.logger import get_logger

from robko01.communicators.base import CommunicatorBase

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

class Communicator(CommunicatorBase):
    """This class is dedicated to work with the serial interface."""

#region Attributes

#endregion

#region Constructor

    def __init__(self, host, port=10182, timeout=1):
        """Constructor

        Args:
            host (str): IP address or domain of the target.
            port (int): Port of the service. Default is 10182.
        """
        super().__init__()

        self.__logger = get_logger(__name__)
        """Data logger.
        """

        self.__host = host
        """Service host.
        """

        self.__port = port
        """Service port.
        """

        self.timeout = timeout

        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        """Socket client.
        """
        self.__client.settimeout(self.timeout)

#endregion

#region Private Methods

    def __make_buffer(self, frame):
        """Make human readable the buffer."""

        buffer = ""
        length = len(frame)
        index = 0

        for data in frame:
            if index < length - 1:
                buffer += f"{data:02X}, "

            else:
                buffer += f"{data:02X}"

            index += 1

        return buffer

#endregion

#region Protected Methods

    def send(self, payload):
        """Send data."""

        msg = f"TX -> {self.__make_buffer(payload)}"
        self.__logger.debug(msg)
        self.__client.sendall(payload)

    def receive(self):
        """Receive the frame."""

        frame = self.__client.recv(1024)
        msg = f"RX <- {self.__make_buffer(frame)}"
        self.__logger.debug(msg)
        return frame

    def send_frame(self, req_frame):
        """Send the frame.

        Args:
            req_frame (bytes): Request frame.

        Returns:
            bytes: Response frame.
        """
        # if self.__client.isOpen() is False:
            # raise FileNotFoundError("Port is not opened on level Communicator.")

        #self._open()
        self.send(req_frame)
        res_frame = None
        res_frame = self.receive()
        #self._close()
        return res_frame

#endregion

#region Public Methods

    def connect(self):
        """Connect to the device.
        """

        if self.__client is not None:

            self.__client.connect((self.__host, self.__port))
            # self.__client.settimeout = self.timeout

    def disconnect(self):
        """Disconnect from device.
        """

        if self.__client is not None:

            self.__client.close()

#endregion
