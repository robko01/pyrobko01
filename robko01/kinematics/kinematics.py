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

from math import atan, cos, pi, sin, sqrt
from robko01.kinematics.data.c_position import CPosition
from robko01.kinematics.data.j_position import JPosition
from robko01.kinematics.exceptions.unreachable_position import UnreachablePosition

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

class Kinematics():
    """Kinematics model of the robot Robko 01.

    Raises:
        UnreachablePosition: _description_
        UnreachablePosition: _description_
        UnreachablePosition: _description_
        UnreachablePosition: _description_
        UnreachablePosition: _description_
        UnreachablePosition: _description_
        UnreachablePosition: _description_
        UnreachablePosition: _description_
    """
#region Attributes

#endregion

#region Properties

    @property
    def H(self):
        """H of the robot structure.

        Returns:
            float: Value of H.
        """
        return 190.0

    @property
    def L1(self):
        """L1 of the robot structure.

        Returns:
            float: Value of L1.
        """
        return 178.0

    @property
    def L2(self):
        """L2 of the robot structure.

        Returns:
            float: Value of L2.
        """
        return 178.0

    @property
    def LL(self):
        """LL of the robot structure.

        Returns:
            float: Value of LL.
        """
        return 92.0

    @property
    def C(self):
        """C of the robot structure.

        Returns:
            float: Value of C.
        """
        return self.__rad

    @property
    def R1(self):
        """Input R1: 1 or 0
        """
        return 0

#endregion

#region Constructor

    def __init__(self):
        self.__rad = 180.0 / pi

#endregion

#region Private Methods

    def __sgn(self, value):

        sign = 0

        if value > 0:
            sign = 1

        if value < 0:
            sign = -1

        return sign

    def __ll(self, G, G0=38.6):
        """LL length of the projection of the end effector.

        Args:
            G (float): Space between the plates of the fingers.
            G0 (float, optional): Space between the fingers when it is parallel. Defaults to 38.6.

        Returns:
            float: Length of the effector.
        """

        return self.L1 - self.L2 ** 2 - (G - G0 ** 2) / 2.0

#endregion

#region Public Methods

    def forward_from_point(self, p: JPosition):
        """Forward kinematics model.

        Args:
            p (JPosition): Target joint position.

        Returns:
            CPosition: Cartesian result point.
        """

        d = self.forward_from_scale(p.T1, p.T2, p.T3, p.T4, p.T5)

        return CPosition(X=d[0], Y=d[1], Z=d[2], P=d[3], R=d[4])

    def forward_from_scale(self, T1 : float, T2 : float, T3 : float, T4 : float, T5 : float):
        """Forward kinematics model.

        Args:
            T1 (float): Theta 1 for base axis. [rad]
            T2 (float): Theta 2 for shoulder axis. [rad]
            T3 (float): Theta 3 for elbow axis. [rad]
            T4 (float): Theta 4 for left differential axis. [rad]
            T5 (float): Theta 5 for right differential axis. [rad]

        Returns:
            tuple: Cartesian coordinate result values.
        """

        P = (T5 + T4) / 2
        R = (T5 - T4) / 2 - self.R1 * T1

        RR = self.L1 * cos(T2) + self.L2 * cos(T3) + self.LL * cos(P)

        X = RR * cos(T1)
        Y = RR * sin(T1)
        Z = self.H + self.L1 * sin(T2) - self.L2 * sin(T3) - self.LL * sin(P)

        P = P * self.C
        R = R * self.C

        return (X, Y, Z, P, R)

    def inverse_from_point(self, c: CPosition):
        """Inverse kinematics model.

        Args:
            c (CPosition): Cartesian target point.

        Returns:
            JPosition: Joint result point.
        """

        p = self.inverse_from_scale(c.X, c.Y, c.Z, c.P, c.R)

        return JPosition(T1=p[0], T2=p[1], T3=p[2], T4=p[3], T5=p[4])

    def inverse_from_scale(self, X : float, Y : float, Z : float, P : float, R : float):
        """Invers kinematics model.

        Args:
            X (float): X [mm]
            Y (float): Y [mm]
            Z (float): Z [mm]
            P (float): P [rad]
            R (float): R [rad]

        Raises:
            UnreachablePosition: Minimum end point distance to body.
            UnreachablePosition: Cen not reach behind base pivot.
            UnreachablePosition: Max wrist differential rotation 270 degrees.
            UnreachablePosition: Max wrist differential rotation 270 degrees.
            UnreachablePosition: Minimum wrist distance to body.
            UnreachablePosition: Past maximum reach of arm.
            UnreachablePosition: Shoulder range.
            UnreachablePosition: Elbow range.

        Returns:
            tuple: Joint coordinates values.

        """

        RR = 0.0
        Z0 = 0.0

        P = P / self.C
        R = R / self.C

        RR = sqrt(X * X + Y * Y)

        if RR < 2.25:
            raise UnreachablePosition("Minimum end point distance to body.")

        if X == 0:
            T1 = self.__sgn(Y) * pi / 2
        else:
            T1 = atan(Y / X)

        if X < 0:
            raise UnreachablePosition("Cen not reach behind base pivot.")

        T5 = P + R + self.R1 * T1
        T4 = P - R - self.R1 * T1

        if -270.0 / self.C > T4 > 270.0 / self.C:
            raise UnreachablePosition("Max wrist differential rotation 270 degrees.")

        if -270.0 / self.C > T5 > 270.0 / self.C:
            raise UnreachablePosition("Max wrist differential rotation 270 degrees.")

        R0 = RR - self.LL * cos(P)
        Z0 = Z - self.LL * sin(P) - self.H

        if R0 < 2.25:
            raise UnreachablePosition("Minimum wrist distance to body.")

        if R0 == 0:
            B = self.__sgn(Z0) * pi / 2
        else:
            B = atan(Z0 / R0)

        A = R0 * R0 + Z0 * Z0
        A = 4 * self.L1 * self.L1  / A - 1

        if A < 0:
            raise UnreachablePosition("Past maximum reach of arm.")

        A = atan(sqrt(A))

        T2 = A + B
        T3 = B - A

        if -127.0 / self.C > T2 > 127.0 / self.C:
            raise UnreachablePosition("Shoulder range.")

        if (T2 - T3) < 0.0 or (T2 - T3) > 127.0 / self.C:
            raise UnreachablePosition("Elbow range.")

        return (T1, T2, T3, T4, T5)

#endregion
