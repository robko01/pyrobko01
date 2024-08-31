
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

from robko01.communicators.base_communicator import BaseCommunicator

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

class Communicator(BaseCommunicator):
    """This class is dedicated to work with the serial interface."""

#region Attributes

    __logger = None
    """Data logger.
    """

    __host = None
    """Service host.
    """

    __port = None
    """Service port.
    """

    __client = None
    """Socket client.
    """

#endregion

#region Constructor

    def __init__(self, host, port=10182):
        """Constructor

        Args:
            host (str): IP address or domain of the target.
            port (int): Port of the service. Default is 10182.
        """

        self.__host = host
        self.__port = port

        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.settimeout(self.timeout)

        self.__logger = get_logger(__name__)

#endregion

#region Private Methods

    def __make_buffer(self, frame):
        """Make human readable the buffer."""

        buffer = ""
        length = len(frame)
        index = 0

        for data in frame:
            if index < length - 1:
                buffer += "{:02X}, ".format(data)

            else:
                buffer += "{:02X}".format(data)

            index += 1

        return buffer

#endregion

#region Protected Methods

    def send(self, frame):
        """Send data."""

        msg = "TX -> {}".format(self.__make_buffer(frame))
        self.__logger.debug(msg)
        self.__client.sendall(frame)

    def receive(self):
        """Receive the frame."""

        frame = self.__client.recv(1024)

        msg = "RX <- {}".format(self.__make_buffer(frame))
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
