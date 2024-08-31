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

class BaseRobko01:
    """Some description that tells you it's abstract,
    often listing the methods you're expected to supply."""

#region Attributes

#endregion

#region Constructor

    def __init__(self):
        self._sync_interval = 0.05
        """Sync time.
        """

        self._synchronous = True
        """Sync mode.
        """

        self._time_to_stop = False
        """Time to stop flag.
        """

        self._communicator = None
        """Communicator instance.
        """

        self._timeout = 50
        """Timeout value.
        """

#endregion

#region Properties

    @property
    def time_to_stop(self):
        """Time to stop.

        Returns:
            float: Time to stop.
        """
        return self._time_to_stop

    @property
    def synchronous(self):
        """Returns Host URL of the service.

        Returns:
            str: Host URL of the service.
        """
        return self._synchronous

    @synchronous.setter
    def synchronous(self, synchronous):
        """Set Host URL of the service.

        Args:
            synchronous (str): Host URL of the service.
        """
        self._synchronous = synchronous

#endregion
