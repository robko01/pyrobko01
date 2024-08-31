#!/usr/bin/env python
# -*- coding: utf8 -*-

"""

Robko 01 - Python Controloftware

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

class CPosition():
    """Cartesian position.
    """

#region Attributes

#endregion

#region Properties

    @property
    def X(self):
        """Get X coordinate.

        Returns:
            float: X value.
        """
        return self.__x

    @X.setter
    def X(self, value):
        """Set X coordinate.

        Args:
            value (float): X value.
        """
        self.__x = value
        self.__update()

    @property
    def Y(self):
        """Get Y coordinate.

        Returns:
            float: Y value.
        """
        return self.__y

    @Y.setter
    def Y(self, value):
        """Set Y coordinate.

        Args:
            value (float): Y value.
        """
        self.__y = value
        self.__update()

    @property
    def Z(self):
        """Get Z coordinate.

        Returns:
            float: Z value.
        """
        return self.__z

    @Z.setter
    def Z(self, value):
        """Set Z coordinate.

        Args:
            value (float): Z value.
        """
        self.__z = value
        self.__update()

    @property
    def P(self):
        """Get P coordinate.

        Returns:
            float: P value.
        """
        return self.__p

    @P.setter
    def P(self, value):
        """Set P coordinate.

        Args:
            value (float): P value.
        """
        self.__p = value
        self.__update()

    @property
    def R(self):
        """Get R coordinate.

        Returns:
            float: R value.
        """
        return self.__r

    @R.setter
    def R(self, value):
        """Set R coordinate.

        Args:
            value (float): R value.
        """
        self.__r = value
        self.__update()

#endregion

#region Constructor

    def __init__(self, **kwargs):

        self.__x = 0.0

        self.__y = 0.0

        self.__z = 0.0

        self.__p = 0.0

        self.__r = 0.0

        if "X" in kwargs:
            self.X = kwargs["X"]

        if "Y" in kwargs:
            self.Y = kwargs["Y"]

        if "Z" in kwargs:
            self.Z = kwargs["Z"]

        if "P" in kwargs:
            self.P = kwargs["P"]

        if "R" in kwargs:
            self.R = kwargs["R"]

    def __str__(self):

        message = "X = {:3.2f}\r\nY = {:3.2f}\r\nZ = {:3.2f}\r\nP = {:3.2f}\r\nR = {:3.2f}"\
            .format(self.X, self.Y, self.Z, self.P, self.R)

        return message

    __repr__ = __str__

#endregion

#region Private Methods

    def __update(self):

        pass

#endregion
