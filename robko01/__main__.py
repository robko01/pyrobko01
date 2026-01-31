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

import sys
import argparse
import signal
import traceback

from robko01.utils.logger import crate_log_file, get_logger

from robko01.tasks.task_manager import TaskManager

from robko01.controllers.controller_factory import ControllerFactory

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

TASK_MANAGER = None

# Create log.
crate_log_file()
LOGGER = get_logger(__name__)

def interrupt_handler(signum, frame):
    """Interrupt handler."""

    global TASK_MANAGER, LOGGER

    if signum == 2:
        LOGGER.warning("Stopped by interrupt.")

    elif signum == 15:
        LOGGER.warning("Stopped by termination.")

    else:
        LOGGER.warning(f"Signal handler called. Signal: {signum}; Frame: {frame}")

    if TASK_MANAGER is not None:
        TASK_MANAGER.stop()

def main():
    """Main function.
    """

    global TASK_MANAGER, LOGGER

    # Add signal handler.
    signal.signal(signal.SIGINT, interrupt_handler)
    signal.signal(signal.SIGTERM, interrupt_handler)

    # Create parser.
    parser = argparse.ArgumentParser()

    parser.add_argument("--task", type=str, default="task_ui_qt", help="Builtin program")
    # parser.add_argument("--port", type=str, default="COM4", help="Serial port or TCP port.")
    # parser.add_argument("--host", type=str, default=None, help="Host/IP of the robot.")
    parser.add_argument("--port", type=str, default="10182", help="Serial port or TCP port.")
    parser.add_argument("--host", type=str, default="remote1.robko01.loc", help="Host/IP of the robot.")
    parser.add_argument("--interface", type=str, default="udp", help="Controller type")
    parser.add_argument("--cname", type=str, default="super", help="Controller type")
    parser.add_argument("--timeout", type=str, default="10", help="Timeout seconds")

    # Take arguments.
    args = parser.parse_args()

    controller = ControllerFactory.create(**vars(args))

    if controller is None:
        raise ValueError("Controller has been specified not properly.")

    TASK_MANAGER = TaskManager(controller=controller)

    names = TASK_MANAGER.list_tasks()
    for name in names:
        LOGGER.info("Found task: %s", name)

    TASK_MANAGER.start(args.task)

    TASK_MANAGER.stop()

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        LOGGER.error(traceback.format_exc())
