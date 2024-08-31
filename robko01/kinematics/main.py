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

from data.c_position import CPosition
from data.j_position import JPosition
from data.steppers_coefficients import SteppersCoefficients
from kinematics import Kinematics

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

def main():

    kin = Kinematics()
    sc = SteppersCoefficients()

    print("----------------------- Forward Kinematics ---------------------------")
    j1 = JPosition(T1=0.0, T2=0.0, T3=0.0, T4=0.0, T5=0.0)
    print(j1)
    print("")
    d_pos = kin.forward_from_scale(j1.T1, j1.T2, j1.T3, j1.T4, j1.T5)
    d1 = CPosition(X=d_pos[0], Y=d_pos[1], Z=d_pos[2], P=d_pos[3], R=d_pos[4])
    print(d1)
    print("")
    d_pos_2 = kin.forward_from_point(j1)
    print(d_pos_2)
    print("")

    print("----------------------- Inverse Kinematics ---------------------------")
    d2 = CPosition(X=308.0, Y=0.0, Z=100.0, P=0.0, R=0.0)
    print(d2)
    print("")
    print("Radians")
    j_pos_2 = kin.inverse_from_point(d2)
    print(j_pos_2.scale(kin.C, kin.C, kin.C, kin.C, kin.C))
    print("")
    j_pos = kin.inverse_from_scale(d2.X, d2.Y, d2.Z, d2.P, d2.R)
    j2 = JPosition(T1=j_pos[0], T2=j_pos[1], T3=j_pos[2], T4=j_pos[3], T5=j_pos[4])
    print(j2)
    print("")
    print("Degrees")
    j4 = j2.scale(kin.C, kin.C, kin.C, kin.C, kin.C)
    print(j4)
    print("")
    print("Steps")
    j3 = j2.scale(sc.t1_const, sc.t2_const, sc.t3_const, sc.t4_const, sc.t5_const)
    print(j3)
    print("")

if __name__ == "__main__":
    main()
