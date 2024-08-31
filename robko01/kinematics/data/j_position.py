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

from .steppers_coefficients import SteppersCoefficients

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

class JPosition():

#region Attributes

#endregion

#region Properties

    @property
    def T1(self):
        """Get T1 coordinate.

        Returns:
            float: T1 value.
        """
        return self.__t1

    @T1.setter
    def T1(self, value):
        """Set T1 coordinate.

        Args:
            value (float): T1 value.
        """
        self.__t1 = value
        self.__update()

    @property
    def T2(self):
        """Get T2 coordinate.

        Returns:
            float: T2 value.
        """
        return self.__t2

    @T2.setter
    def T2(self, value):
        """Set T2 coordinate.

        Args:
            value (float): T2 value.
        """
        self.__t2 = value
        self.__update()

    @property
    def T3(self):
        """Get T3 coordinate.

        Returns:
            float: T3 value.
        """
        return self.__t3

    @T3.setter
    def T3(self, value):
        """Set T3 coordinate.

        Args:
            value (float): T3 value.
        """
        self.__t3 = value
        self.__update()

    @property
    def T4(self):
        """Get T4 coordinate.

        Returns:
            float: T4 value.
        """
        return self.__t4

    @T4.setter
    def T4(self, value):
        """Set T4 coordinate.

        Args:
            value (float): T4 value.
        """
        self.__t4 = value
        self.__update()

    @property
    def T5(self):
        """Get T5 coordinate.

        Returns:
            float: T5 value.
        """
        return self.__t5

    @T5.setter
    def T5(self, value):
        """Set T5 coordinate.

        Args:
            value (float): T5 value.
        """
        self.__t5 = value
        self.__update()

    @property
    def T6(self):
        """Get T6 coordinate.

        Returns:
            float: T6 value.
        """
        return self.__t6

    @T6.setter
    def T6(self, value):
        """Set T6 coordinate.

        Args:
            value (float): T6 value.
        """
        self.__t6 = value
        self.__update()

#endregion

#region Constructor

    def __init__(self, **kwargs):

        self.__t1 = 0.0

        self.__t2 = 0.0

        self.__t3 = 0.0

        self.__t4 = 0.0

        self.__t5 = 0.0

        self.__t6 = 0.0

        if "T1" in kwargs:
            self.T1 = kwargs["T1"]

        if "T2" in kwargs:
            self.T2 = kwargs["T2"]

        if "T3" in kwargs:
            self.T3 = kwargs["T3"]

        if "T4" in kwargs:
            self.T4 = kwargs["T4"]

        if "T5" in kwargs:
            self.T5 = kwargs["T5"]

        if "T6" in kwargs:
            self.T6 = kwargs["T6"]

    def __str__(self):

        message = "T1 = {:3.2f}\r\nT2 = {:3.2f}\r\nT3 = {:3.2f}\r\nT4 = {:3.2f}\r\nT5 = {:3.2f}"\
            .format(self.T1, self.T2, self.T3, self.T4, self.T5)

        return message

    __repr__ = __str__

#endregion

#region Private Methods

    def __update(self):

        pass

#endregion

#region Public Methods

    def scale(self, S1: float, S2: float, S3: float, S4: float, S5: float, S6: float):
        """Scale the joint vector.

        Args:
            S1 (float): Scaling coefficient
            S2 (float): Scaling coefficient
            S3 (float): Scaling coefficient
            S4 (float): Scaling coefficient
            S5 (float): Scaling coefficient
            S6 (float): Scaling coefficient

        Returns:
            tuple: _description_
        """

        return JPosition(\
            T1=self.T1 * S1, T2=self.T2 * S2,\
            T3=self.T3 * S3, T4=self.T4 * S4,\
            T5=self.T5 * S5, T6=self.T6 * S6)

    def to_steps(self, j_pos):
        """To steps.

        Args:
            j_pos (JPosition): Joint position in steps.

        Returns:
            tuple: Tuple of recalculated values.
        """
        return tuple([j_pos.T1 * SteppersCoefficients.t1_const,\
                      j_pos.T2 * SteppersCoefficients.t2_const,\
                      j_pos.T3 * SteppersCoefficients.t3_const,\
                      j_pos.T4 * SteppersCoefficients.t4_const,\
                      j_pos.T5 * SteppersCoefficients.t5_const,\
                      j_pos.T6 * SteppersCoefficients.t6_const])


    def from_steps(self, j_pos):
        """From steps.

        Args:
            j_pos (JPosition): Joint position in radians.

        Returns:
            tuple: Tuple of recalculated values.
        """
        return tuple([j_pos.T1 / SteppersCoefficients.t1_const,\
                      j_pos.T2 / SteppersCoefficients.t2_const,\
                      j_pos.T3 / SteppersCoefficients.t3_const,\
                      j_pos.T4 / SteppersCoefficients.t4_const,\
                      j_pos.T5 / SteppersCoefficients.t5_const,\
                      j_pos.T6 / SteppersCoefficients.t6_const])

#endregion
