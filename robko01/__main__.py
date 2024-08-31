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

task_manager = None

# Create log.
crate_log_file()
logger = get_logger(__name__)

def interrupt_handler(signum, frame):
    """Interrupt handler."""

    global task_manager, logger

    if signum == 2:
        logger.warning("Stopped by interrupt.")

    elif signum == 15:
        logger.warning("Stopped by termination.")

    else:
        logger.warning("Signal handler called. Signal: {}; Frame: {}".format(signum, frame))

    if task_manager is not None:
        task_manager.stop()

def main():
    """Main function.
    """

    global task_manager, logger

    # Add signal handler.
    signal.signal(signal.SIGINT, interrupt_handler)
    signal.signal(signal.SIGTERM, interrupt_handler)

    # Create parser.
    parser = argparse.ArgumentParser()

    parser.add_argument("--task", type=str, default="task_ui_qt", help="Builtin program")
    parser.add_argument("--port", type=str, default="COM4", help="Serial port or TCP port.")
    parser.add_argument("--host", type=str, default=None, help="Host/IP of the robot.")
    parser.add_argument("--cname", type=str, default="orlin369", help="Controller type")
    parser.add_argument("--em", type=str, default="f", help="Step mode")

    # Take arguments.
    args = parser.parse_args()

    controller = ControllerFactory.create(**vars(args))

    if controller is None:
        raise ValueError("Controller has been specified not properly.")

    task_manager = TaskManager(controller=controller)

    names = task_manager.list_tasks()
    for name in names:
        logger.info("Found task: %s", name)

    task_manager.start(args.task)

    task_manager.stop()

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        logger.error(traceback.format_exc())
