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

# Lazy import for pyserial to avoid import-time failures when pyserial is not
# installed. The module will raise ImportError when serial functionality is
# actually needed.
_serial = None
def _get_serial():
    global _serial
    if _serial is None:
        try:
            import serial as _s
        except Exception as exc:
            raise ImportError("pyserial is required for serial communicator: pip install pyserial") from exc
        _serial = _s
    return _serial

from robko01.communicators.base import CommunicatorBase

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

__version__ = "1.0.0"
"""Version of the file."""

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

    def __init__(self, port, baudrate=115200, timeout=1):
        """Constructor

        Args:
            port (str): Name of the port.
        """

        super().__init__()

        self.__logger = get_logger(__name__)
        """Logger
        """

        serial = _get_serial()
        self.__client = serial.Serial(port)
        """Serial port.
        """

        self.__client.baudrate = baudrate
        self.timeout = timeout
        self.__client.timeout = self.timeout

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

    def send(self, payload):
        """Send data.

        Args:
            payload (bytes): Payload
        """
        msg = f"TX -> {self.__make_buffer(payload)}"
        self.__logger.debug(msg)
        self.__client.write(payload)

    def receive(self):
        """Receive the frame.
        """
        frame = None
        wait = 0.1
        times = 0

        while True:
            size = self.__client.inWaiting()
            if size > 0:
                frame = self.__client.read(size)
                break

            times += wait
            time.sleep(wait)

            if times > self.timeout:
                raise TimeoutError("Time out has occurred in Communicator.")

        msg = f"RX <- {self.__make_buffer(frame)}"
        self.__logger.debug(msg)
        return frame

    def send_frame(self, req_frame):
        """Send the frame.
        """
        if self.__client.isOpen() is False:
            raise FileNotFoundError("Port is not opened on level Communicator.")

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
        is_open = self.__client.isOpen()
        if not is_open:
            self.__client.timeout = self.timeout
            # self.__client.setDTR(False)
            # self.__client.setRTS(False)
            self.__client.open()

    def disconnect(self):
        """Disconnect from device.
        """
        if self.__client.isOpen() is True:

            # self.__client.setDTR(False)
            # self.__client.setRTS(False)
            self.__client.close()

    def reset(self):
        """Reset target device.
        """

        return
        if self.__client.isOpen() is False:
            raise Exception("Port is not opened on level Communicator.")

        self.__client.setDTR(False)
        self.__client.setRTS(False)
        time.sleep(0.001)
        self.__client.setDTR(True)
        self.__client.setRTS(True)
        time.sleep(0.001)
        self.__client.setDTR(False)
        self.__client.setRTS(False)
        time.sleep(self.timeout)

    def is_connected(self) -> bool:
        """Return True if communicator is currently connected."""
        status = False

        try:
            status = self.__client.isOpen()
        except Exception:
            pass

        return status

#endregion
