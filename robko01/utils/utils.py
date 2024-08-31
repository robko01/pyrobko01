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

from struct import unpack

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

def scale(value, in_min, in_max, out_min, out_max):
    """Scale value.

    Args:
        value (float): Value for scaling.
        in_min (float): Input value minimum.
        in_max (float): Input value maximum.
        out_min (float): Output value minimum.
        out_max (float): Output value maximum.

    Returns:
        float: Scaled value.
    """
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def scale_speeds(position, speed):
    """Proportional speed scales.

    Args:
        position (list): Point in joint space.
        speed (float): scalar.

    Returns:
        list: Result.
    """
    positions = []

    for key, value in enumerate(position):

        if key % 2 == 0:
            positions.append(value)

    max_pos = max(positions)

    speeds = []

    for key, value in enumerate(positions):

        if max_pos == 0:
            speeds.append(100)

        else:
            speeds.append(abs(scale(value, 0, max_pos, 0, speed)))

    pos_index = 0
    speed_index = 0

    for key, value in enumerate(position):

        if key % 2 == 0:
            position[key] = positions[pos_index]
            pos_index += 1

        else:
            position[key] = speeds[speed_index]
            speed_index += 1

    return position

def int_to_bin(in_value):
    """Convert Integer to Binary.

    Args:
        in_value (int): Integer value

    Returns:
        str: String binary format.
    """
    value = unpack("B", in_value)
    value = int(value[0])
    value = "{0:08b}".format(value)

    return value
