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

class StatusCode(Enum):
    """Status codes."""

#region Enum

    Ok = 1
    """When everything is OK.
    """

    Error = 2
    """When error occurred.
    """

    Busy = 3
    """When busy in other operation.
    """

    TimeOut = 4
    """Then time for the operation has timed out.
    """

#endregion

#region Static Public Methods

    @staticmethod
    def to_text(status):
        """Convert status code to readable text.

        Args:
            status (StatusCode): Status code.

        Returns:
            str: Status code text description.
        """
        text = ""

        if status == StatusCode.Ok.value:
            text = "OK"

        elif status == StatusCode.Error.value:
            text = "Error"

        elif status == StatusCode.Busy.value:
            text = "Busy"

        elif status == StatusCode.TimeOut.value:
            text = "TimeOut"

        return text

#endregion
