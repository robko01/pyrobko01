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

from robko01.controllers.orlin369.protocol.frame_indexes import FrameIndexes
from robko01.controllers.orlin369.protocol.package_type import PackageType

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

class Response:
    """Response parser.
    """

#region Attributes

    __frame = None
    """Frame container.
    """

    __payload = None
    """Payload container.
    """

    __size = 0
    """Package size.
    """

    __FRAME_STATIC_FIELD_OFFSET = 5
    __FRAME_MIN_PAYLOAD_SIZE = 0
    __FRAME_MAX_PAYLOAD_SIZE = 27

#endregion

#region Constructor

    def __init__(self, frame):
        """Constructor
        """

        self.__frame = frame
        self.__parse()

#endregion

#region Destructor

    def __del__(self):
        del self.__frame

#endregion

#region Properties

    @property
    def opcode(self):
        """Operation code.

        Returns:
            int: Operation code.
        """
        return int(self.__frame[FrameIndexes.OpCode.value])

    @property
    def payload(self):
        """Payload data.

        Returns:
            bytes: Payload data.
        """
        return self.__payload

    @property
    def status(self):
        """Status code.

        Returns:
            int: Status code.
        """
        return int(self.__frame[FrameIndexes.Status.value])

#endregion

#region Private Methods

    def __parse(self):

        if self.is_valid():
            self.__size = int(self.__frame[FrameIndexes.Size.value])

            if (self.__size - 2) > 0:
                self.__payload = []

                for index in range(self.__size - 2):
                    self.__payload.append(self.__frame[index + self.__FRAME_STATIC_FIELD_OFFSET])

    def __is_valid_container(self):
        return self.__frame is not None

    def __is_valid_len(self):
        return len(self.__frame) > 6

    def __is_valid_sentinel(self):
        return self.__frame[FrameIndexes.Sentinel.value] == 0xAA

    def __is_response(self):
        return self.__frame[FrameIndexes.PackageType.value] == PackageType.Response.value

    def __is_valid_size(self):
        return (int(self.__frame[FrameIndexes.Size.value]) > self.__FRAME_MIN_PAYLOAD_SIZE) and \
                (int(self.__frame[FrameIndexes.Size.value]) < self.__FRAME_MAX_PAYLOAD_SIZE)

#endregion

#region Public Methods

    def is_valid(self):
        """Is valid frame.

        Returns:
            bool: Is valid frame.
        """
        if self.__is_valid_container() is False:
            return False

        if self.__is_valid_len() is False:
            return False

        state = True

        state = state and self.__is_valid_sentinel()

        state = state and self.__is_response()

        state = state and self.__is_valid_size()

        return state

    def payload_is(self, payload):
        """Payload validator.

        Args:
            payload (bytes):  Payload data.

        Returns:
            bool: Is the same.
        """
        if self.payload is None:
            return False

        if len(self.payload) <= 0:
            return False

        if payload is None:
            return False

        if payload != self.payload:
            return False

        return True

#endregion
