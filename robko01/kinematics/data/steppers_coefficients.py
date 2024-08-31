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

class SteppersCoefficients():
    """Stepper motor coefficients.
    """

#region Properties

    @property
    def t1_const(self):
        """T1 scaling coefficient.

        Returns:
            float: Scaling value.
        """
        return 1222.7

    @property
    def t2_const(self):
        """T2 scaling coefficient.

        Returns:
            float: Scaling value.
        """
        return 1161.4

    @property
    def t3_const(self):
        """T3 scaling coefficient.

        Returns:
            float: Scaling value.
        """
        return 680.1

    @property
    def t4_const(self):
        """T4 scaling coefficient.

        Returns:
            float: Scaling value.
        """
        return 244.7

    @property
    def t5_const(self):
        """T5 scaling coefficient.

        Returns:
            float: Scaling value.
        """
        return 244.7

    @property
    def t6_const(self):
        """T6 scaling coefficient.

        Returns:
            float: Scaling value.
        """
        return 27.0

#endregion
