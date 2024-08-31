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

from joystick import JoystickController
import time

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

#endregion

dead_zone = 0.2
max_speed = 150

def l_scale(target, in_limit, out_limit):
    """Linear scaling function.
    Args:
        target (float): Input scalar.
        in_limit (list): List of two elements with input minimum and maximum.
        out_limit ([type]): List of two elements with output minimum and maximum.
    Returns:
        float: Output scaled value.
    """

    return (target - in_limit[0]) * (out_limit[1] - out_limit[0]) / \
        (in_limit[1] - in_limit[0]) + out_limit[0]


speeds = {}
def jsc_update_cb(button_data, axis_data, hat_data):

    speeds = [0, 0, 0, 0, 0, 0]


    axis_length = 6

    for index in range(axis_length):

        # Does the axis exists?
        if index in axis_data:
            pos = axis_data[index]

            # Does the axis is out of the dead zone?
            if abs(pos) >= dead_zone:
                speeds[index] = l_scale(pos, [-1.0, 1.0], [-max_speed, max_speed])
                speeds[index] = int(speeds[index])

    print(speeds)

    # print(button_data)
    # print(axis_data)

def main():

    jsc = JoystickController()
    jsc.update_cb(jsc_update_cb)

    update_rate = 0.2
    t0 = 0
    t1 = 0
    while True:
        t1 = time.time()
        delta = t1 - t0
        if delta >= update_rate:
            t0 = t1
            jsc.update()

if __name__ == "__main__":
    main()
