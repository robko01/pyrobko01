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

from enum import Enum

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

class OpCode(Enum):
    """Operation codes.
    """

#region Enum

    Ping = 1
    """Ping code.
    """

    Stop = 2
    """Stop robot motion execution.
    """

    Disable = 3
    """Disable motion of the robot.
    """

    Enable = 4
    """Enable motion of the robot.
    """

    Clear = 5
    """Clear robot current position.
    """

    MoveRelative = 6
    """Move relative to next position.
    """

    MoveAbsolute = 7
    """Move absolute to nex position.
    """

    DO = 8
    """Write to Digital Outputs.
    """

    DI = 9
    """Read the digital inputs.
    """

    IsMoving = 10
    """Return state does one or more axises of the robot are moving.
    """

    CurrentPosition = 11
    """Current robot position.
    """

    MoveSpeed = 12
    """Move in speed mode.
    """

#endregion

#region Public Static Methods

    @staticmethod
    def to_text(code):
        """Operation code.

        Args:
            code (OpCode): Operation Code.

        Returns:
            str: Operation code text.
        """

        text = "Unknown"

        if code == OpCode.Ping.value:
            text = "Ping"

        elif code == OpCode.Stop.value:
            text = "Stop"

        elif code == OpCode.Disable.value:
            text = "Disable"

        elif code == OpCode.Enable.value:
            text = "Enable"

        elif code == OpCode.Clear.value:
            text = "Clear"

        elif code == OpCode.MoveRelative.value:
            text = "Move Relative"

        elif code == OpCode.MoveAbsolute.value:
            text = "Move Absolute"

        elif code == OpCode.DO.value:
            text = "Digital Outputs"

        elif code == OpCode.DI.value:
            text = "Digital Inputs"

        elif code == OpCode.IsMoving.value:
            text = "Is Moving"

        elif code == OpCode.CurrentPosition.value:
            text = "Current Position"

        elif code == OpCode.MoveSpeed.value:
            text = "Move Speed"

        else:
            text = f"Not implemented: {code}"

        return text

#endregion
