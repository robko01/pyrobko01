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

from robko01.communicators.serial.communicator import Communicator as SerCom
from robko01.communicators.tcp.communicator import Communicator as TCPCom
from robko01.communicators.udp.communicator import Communicator as UDPCom

from robko01.controllers.orlin369.robko01 import Robko01 as Orko01
from robko01.controllers.tu_gabrovo.protocol.package_manager import PackageManager as GabkoPM
from robko01.controllers.tu_gabrovo.robko01 import Robko01 as Gabko01

from robko01.controllers.dummy.robko01 import Robko01 as Dummy

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

class ControllerFactory:
    """Controller factory.
    """

    @staticmethod
    def create(**kwargs):
        """Create instance of controller.

        Returns:
            Any: Instance of controller.
        """
        timeout = 1
        controller = None
        controller_name = None
        interface = None
        communicator = None

        if "cname" in kwargs:
            controller_name = kwargs["cname"]

        if "interface" in kwargs:
            interface = kwargs["interface"]

        if "timeout" in kwargs:
            timeout = kwargs["timeout"]
            timeout = int(timeout)

        if interface is None:
            raise ValueError("Communication type can not be None.")

        elif interface == "serial":
            if not kwargs["port"].isnumeric():
                communicator = SerCom(kwargs["port"], timeout=timeout)          
        elif interface == "tcp":
            if kwargs["port"].isnumeric() and kwargs["host"] is not None:
                communicator = TCPCom(kwargs["host"], int(kwargs["port"]), timeout=timeout)
        elif interface == "udp":
            if kwargs["port"].isnumeric() and kwargs["host"] is not None:
                communicator = UDPCom(kwargs["host"], int(kwargs["port"]), timeout=timeout)
        elif interface == "dummy":
            communicator=object()
        else:
            raise ValueError(f"Communication type is not supported: {interface}")

        if controller_name is None:
            raise ValueError("Controller type can not be None.")

        elif controller_name == "dummy":
            controller = Dummy(communicator)

        elif controller_name == "orlin369":
            controller = Orko01(communicator)

        elif controller_name == "tugab":
            controller = Gabko01(GabkoPM(kwargs))

        else:
            raise NotImplementedError(f"The specified controller name does not have implementation: {controller_name}")

        return controller
