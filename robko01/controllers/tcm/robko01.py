#!/usr/bin/env python
# -*- coding: utf8 -*-

"""

Robko 01 - Python Control Software

Copyright (C) [2025] [Orlin Dimitrov]

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

from robko01.controllers.base import Robko01Base
from robko01.utils.logger import get_logger

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2025, Orlin Dimitrov"
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

class Robko01(Robko01Base):
    """TCM (Text Command Mode) controller implementation."""

#region Attributes

#endregion

#region Constructor

    def __init__(self, **kwargs):

        super().__init__(kwargs)

        self.__logger = get_logger(__name__)
        """Logger."""

        self.__is_moving_cb = None
        """Is moving callback.
        """

        self.__digital_inputs = 0
        """Digital inputs bitmask (from @READ)."""

        self.__digital_outputs = 0
        """Digital outputs.
        """

        self.__speed = 100
        """Default speed for @STEP when not provided."""

#endregion

#region Private Helpers

    def __parse_response(self, response):
        """Parse TCM response and return first non-empty line."""
        if response is None:
            return ""
        if isinstance(response, (bytes, bytearray)):
            text = response.decode("ascii", errors="ignore")
        else:
            text = str(response)
        for line in text.replace("\r", "\n").split("\n"):
            line = line.strip()
            if line:
                return line
        return ""

    def __send_command(self, command: str) -> str:
        """Send command and return response line."""
        if not command.endswith("\r\n"):
            command = f"{command}\r\n"
        payload = command.encode("ascii")
        self.__logger.debug("Command: %s", payload)
        response = self._communicator.send_frame(payload)
        self.__logger.debug("Response: %s", response)
        return self.__parse_response(response)

    def __extract_duration(self, response: str) -> int:
        if response.startswith("OK DUR:"):
            try:
                return int(response.split(":", 1)[1].strip())
            except ValueError:
                return -1
        return -1

    def __normalize_positions(self, target_position):
        if isinstance(target_position, (list, tuple)):
            if len(target_position) == 6:
                return [int(v) for v in target_position]
            if len(target_position) == 12:
                return [int(target_position[i]) for i in range(0, 12, 2)]
        raise ValueError("Target position must be a list of 6 or 12 values.")

#endregion

#region Public Methods

    def connect(self):
        """Connect to the robot controller.
        """
        self._communicator.connect()

    def disconnect(self):
        """Disconnect from robot controller.
        """
        self._communicator.disconnect()

    def stop(self):
        """Stop robot motion execution.
        """
        return self.__send_command("FREE")

    def disable(self):
        """Disable robot motion execution.
        """
        return self.__send_command("FREE")

    def enable(self):
        """Enable robot motion execution.

        Returns:
            str: Controller response.
        """
        return self.__send_command("@CLOSE")

    def clear(self):
        """Clear robot position.
        """
        return self.__send_command("@RESET")

    def set_speed(self, speed: int):
        """Set global motor speed."""
        self.__speed = int(speed)
        return self.__send_command(f"@SET {self.__speed}")

    def move_absolute(self, target_position):
        """Move absolute to next robot position.
        """

        steps = self.__normalize_positions(target_position)
        speed = self.__speed
        if isinstance(target_position, (list, tuple)) and len(target_position) == 12:
            candidates = [int(v) for v in target_position[1:12:2] if int(v) >= 0]
            if candidates:
                speed = max(candidates)
        if speed <= 0:
            speed = self.__speed
        return self.__send_command(
            f"@STEP {int(speed)} {steps[0]} {steps[1]} {steps[2]} {steps[3]} {steps[4]} {steps[5]}"
        )

    # wrapper supports both unified and legacy signatures
    def move_relative(self, *args):
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            steps = args[0]
        elif len(args) == 3:
            joint, _delay, delta = args
            steps = [0] * 12
            idx = int(joint) * 2
            if 0 <= idx < 12:
                steps[idx] = delta
        else:
            raise TypeError("move_relative expects either positions list or (joint,delay,steps)")

        current = self.current_position()
        current_steps = [current[i] for i in range(0, 12, 2)]
        if len(steps) == 6:
            deltas = steps
        else:
            deltas = [steps[i] for i in range(0, 12, 2)]
        target = [current_steps[i] + int(deltas[i]) for i in range(6)]
        return self.move_absolute(target)

    def is_moving(self):
        """Is moving. Every bit represents an axis.
        """
        result = 0

        if self.__is_moving_cb is not None:
            self.__is_moving_cb(result)

        return result

    def current_position(self):
        """Current robot position.
        """
        response = self.__send_command("@READ")
        values = []
        if response:
            for item in response.split(","):
                item = item.strip()
                if item:
                    try:
                        values.append(int(item))
                    except ValueError:
                        pass
        if len(values) >= 7:
            self.__digital_inputs = values[6]
        positions = values[:6] if len(values) >= 6 else [0] * 6
        expanded = []
        for pos in positions:
            expanded.extend([int(pos), 0])
        return expanded

    def get_inputs(self):
        """Current robot inputs.
        """

        return self.__digital_inputs

    def set_outputs(self, value: int):
        """Set robot outputs.

        Args:
            value (int): Digital outputs bit mask.
        """
        response = None

        if value < 0:
            raise ValueError(f"The value: {value} should be bigger then 0.")

        if value > 255:
            raise ValueError(f"The value: {value} should be less then 255.")

        self.__digital_outputs = value

        return response

    def is_moving_cb(self, callback):
        """Is moving callback.

        Args:
            callback (function): Callable callback function.
        """
        self.__is_moving_cb = callback

    def movej(self, *positions) -> int:
        """Interpolated joint move. Returns duration in ms."""
        if len(positions) == 1 and isinstance(positions[0], (list, tuple)):
            positions = positions[0]
        if len(positions) != 6:
            raise ValueError("movej requires 6 joint positions.")
        response = self.__send_command(
            f"@MOVEJ {int(positions[0])} {int(positions[1])} {int(positions[2])} {int(positions[3])} {int(positions[4])} {int(positions[5])}"
        )
        return self.__extract_duration(response)

    def moveik(self, x=0, y=0, z=0, pitch=0, roll=0, gripper=0) -> int:
        """Inverse kinematics move. Returns duration in ms."""
        response = self.__send_command(
            f"@MOVEIK {int(x)} {int(y)} {int(z)} {int(pitch)} {int(roll)} {int(gripper)}"
        )
        return self.__extract_duration(response)

#endregion
