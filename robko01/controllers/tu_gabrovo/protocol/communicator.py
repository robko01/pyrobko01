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

class Communicator():
    """This class is dedicated to drive Robko01 TU-GAB driver.
    """

#region Attributes

#endregion

#region Constructor

    def __init__(self, name):

        self.__logger = get_logger(__name__)

        # Check the serial port name.
        if name is None:
            raise ValueError("Must enter serial port name.")
            #self.__port.port = "COM81"
            #self.__port.port = "/dev/ttyUSB0"
            #self.__port.port = "/dev/ttyUSB7"
            #self.__port.port = "/dev/ttyS2"

        # Set the name.
        self.__port = serial.Serial(name)
        """Serial port.
        """
        # Baud rate to 9600.
        self.__port.baudrate = 9600
        # Number of bits per bytes.
        self.__port.bytesize = serial.EIGHTBITS
        # Set parity check: no parity.
        self.__port.parity = serial.PARITY_NONE
        # Number of stop bits.
        self.__port.stopbits = serial.STOPBITS_ONE
        # B read.
        #self.__port.timeout = None
        # Non-b read.
        #self.__port.timeout = 1
        # Timeout b read
        self.__port.timeout = 5
        # Disable software flow control
        self.__port.xonxoff = False
        # Disable hardware (RTS/CTS) flow control
        self.__port.rtscts = False
        # Disable hardware (DSR/DTR) flow control
        self.__port.dsrdtr = False

        self.__timeout = 0.2
        """Timeout in second.
        """

#endregion

#region Protected Methods

    def _send(self, payload):

        self.__port.write(payload)

    def _receive(self):

        frame = None
        wait = 0.1
        times = 0

        while True:
            size = self.__port.inWaiting()
            if size > 0:
                frame = self.__port.read(size)
                break

            times += wait
            time.sleep(wait)

            if times > self.__timeout:
                raise Exception("Time out has ocurred in Communicator.")

        return frame

    def _send_frame(self, req_frame):

        if self.__port.isOpen() is False:
            raise Exception("Port is not opened on level Communicator.")

        #self._open()
        self._send(req_frame)
        res_frame = None
        res_frame = self._receive()
        #self._close()
        return res_frame

#endregion

#region Public Methods

    def connect(self):
        """Connect to the device."""

        if self.__port.isOpen() is False:

            self.__port.timeout = self.timeout
            self.__port.setDTR(False)
            self.__port.setRTS(False)
            self.__port.open()

    def disconnect(self):
        """Disconnect from device."""

        if self.__port.isOpen() is True:

            self.__port.setDTR(False)
            self.__port.setRTS(False)
            self.__port.close()

#endregion
