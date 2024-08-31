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

from robko01.controllers.tu_gabrovo.protocol.communicator import Communicator

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

class PackageManager(Communicator):
    """Package manager."""

#region Public Methods

    def request(self, payload=None):
        """Request to device.

        Args:
            payload (bytes, optional): Payload bytes of the request. Defaults to None.

        Returns:
            bytes: Response of the device.
        """
        res_frame = self._send_frame(payload.encode())
        list_res_frame = list(res_frame)

        return Response(list(list_res_frame))

    def response(self, opcode, status, payload=None):
        """Response from device.

        Args:
            opcode (int): _description_
            status (int): _description_
            payload (int, optional): _description_. Defaults to None.

        Returns:
            bytes: _description_
        """
        # clear the buffer
        res_frame = ""

        # Begin byte.
        res_frame += chr(0xAA)

        # Request byte.
        res_frame += chr(PackageType.Response)

        # Length of the frame.
        if payload is not None:
            res_frame += chr(len(payload) + 2)
        else:
            res_frame += chr(2)

        # Operation code.
        res_frame += chr(opcode.value)

        # Status code
        res_frame += chr(status.value)

        if payload is not None:
            # Payload
            res_frame += payload

        # CRC
        res_frame += self.__crc(res_frame)

        return res_frame

#endregion
