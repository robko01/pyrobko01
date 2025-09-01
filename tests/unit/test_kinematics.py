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

import unittest

from robko01.kinematics.kinematics import Kinematics
from robko01.kinematics.data.c_position import CPosition
from robko01.kinematics.data.j_position import JPosition
from robko01.kinematics.data.steppers_coefficients import SteppersCoefficients

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

class TestSum(unittest.TestCase):
    """Test the kinematics, JPosition and CPosition
    """

    def test_kinematics(self):
        """Test the kinematics, JPosition and CPosition
        """

        kinematics = Kinematics()
        sc = SteppersCoefficients()

        j1 = JPosition(T1=0.0, T2=0.0, T3=0.0, T4=0.0, T5=0.0)
        self.assertEqual(j1.T1, 0, "T1 Should be 0.0")
        self.assertEqual(j1.T2, 0, "T2 Should be 0.0")
        self.assertEqual(j1.T3, 0, "T3 Should be 0.0")
        self.assertEqual(j1.T4, 0, "T4 Should be 0.0")
        self.assertEqual(j1.T5, 0, "T5 Should be 0.0")

        c1 = kinematics.forward_from_scale(j1.T1, j1.T2, j1.T3, j1.T4, j1.T5)
        self.assertEqual(c1[0], 448.0, "X Should be 448.0")
        self.assertEqual(c1[1], 0.0, "Y Should be 0.0")
        self.assertEqual(c1[2], 190.0, "Z Should be 190.0")
        self.assertEqual(c1[3], 0.0, "P Should be 0.0")
        self.assertEqual(c1[4], 0.0, "R Should be 0.0")

        d1 = CPosition(X=c1[0], Y=c1[1], Z=c1[2], P=c1[3], R=c1[4])
        self.assertEqual(d1.X, 448.0, "X Should be 448.0")
        self.assertEqual(d1.Y, 0.0, "Y Should be 0.0")
        self.assertEqual(d1.Z, 190.0, "Z Should be 190.0")
        self.assertEqual(d1.P, 0.0, "P Should be 0.0")
        self.assertEqual(d1.R, 0.0, "R Should be 0.0")

        d2 = kinematics.forward_from_point(j1)
        self.assertEqual(d2.X, 448.0, "X Should be 448.0")
        self.assertEqual(d2.Y, 0.0, "Y Should be 0.0")
        self.assertEqual(d2.Z, 190.0, "Z Should be 190.0")
        self.assertEqual(d2.P, 0.0, "P Should be 0.0")
        self.assertEqual(d2.R, 0.0, "R Should be 0.0")

        d3 = CPosition(X=448.0, Y=0.0, Z=190.0, P=0.0, R=0.0)
        self.assertEqual(d3.X, 448.0, "X Should be 448.0")
        self.assertEqual(d3.Y, 0.0, "Y Should be 0.0")
        self.assertEqual(d3.Z, 190.0, "Z Should be 190.0")
        self.assertEqual(d3.P, 0.0, "P Should be 0.0")
        self.assertEqual(d3.R, 0.0, "R Should be 0.0")

        j2 = kinematics.inverse_from_point(d3)
        rj2 = j2.scale(
            kinematics.C, kinematics.C,
            kinematics.C, kinematics.C,
            kinematics.C, kinematics.C)
        self.assertEqual(rj2.T1, 0, "T1 Should be 0.0")
        self.assertEqual(rj2.T2, 0, "T2 Should be 0.0")
        self.assertEqual(rj2.T3, 0, "T3 Should be 0.0")
        self.assertEqual(rj2.T4, 0, "T4 Should be 0.0")
        self.assertEqual(rj2.T5, 0, "T5 Should be 0.0")

        j3 = kinematics.inverse_from_scale(d2.X, d2.Y, d2.Z, d2.P, d2.R)
        self.assertEqual(j3[0], 0, "T1 Should be 0.0")
        self.assertEqual(j3[1], 0, "T2 Should be 0.0")
        self.assertEqual(j3[2], 0, "T3 Should be 0.0")
        self.assertEqual(j3[3], 0, "T4 Should be 0.0")
        self.assertEqual(j3[4], 0, "T5 Should be 0.0")

        j2 = JPosition(T1=j3[0], T2=j3[1], T3=j3[2], T4=j3[3], T5=j3[4])
        self.assertEqual(j2.T1, 0, "T1 Should be 0.0")
        self.assertEqual(j2.T2, 0, "T2 Should be 0.0")
        self.assertEqual(j2.T3, 0, "T3 Should be 0.0")
        self.assertEqual(j2.T4, 0, "T4 Should be 0.0")
        self.assertEqual(j2.T5, 0, "T5 Should be 0.0")

        j4 = j2.scale(
            kinematics.C, kinematics.C,
            kinematics.C, kinematics.C,
            kinematics.C, kinematics.C)
        self.assertEqual(j4.T1, 0, "T1 Should be 0.0")
        self.assertEqual(j4.T2, 0, "T2 Should be 0.0")
        self.assertEqual(j4.T3, 0, "T3 Should be 0.0")
        self.assertEqual(j4.T4, 0, "T4 Should be 0.0")
        self.assertEqual(j4.T5, 0, "T5 Should be 0.0")

        j5 = j2.scale(sc.t1_const, sc.t2_const, sc.t3_const, sc.t4_const, sc.t5_const, 0.0)
        self.assertEqual(j5.T1, 0, "T1 Should be 0.0")
        self.assertEqual(j5.T2, 0, "T2 Should be 0.0")
        self.assertEqual(j5.T3, 0, "T3 Should be 0.0")
        self.assertEqual(j5.T4, 0, "T4 Should be 0.0")
        self.assertEqual(j5.T5, 0, "T5 Should be 0.0")

if __name__ == "__main__":
    unittest.main()
