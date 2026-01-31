#!/usr/bin/env python
# -*- coding: utf8 -*-

"""

Robko 01 - Python Control Software

Copyright (C) [2026] [Orlin Dimitrov]

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

# Lazy import for pymodbus to avoid import-time failures when optional
# dependency is not installed.
_pymodbus = None

def _get_pymodbus():
    global _pymodbus
    if _pymodbus is None:
        try:
            import pymodbus as _p
        except Exception as exc:
            raise ImportError("pymodbus is required for Modbus TCP: pip install pymodbus") from exc
        _pymodbus = _p
    return _pymodbus

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2026, Orlin Dimitrov"
"""Copyright holder"""

__credits__ = []
"""Credits"""

__license__ = "GPLv3"
"""License
@see http://www.gnu.org/licenses/"""


__maintainer__ = "Orlin Dimitrov"
"""Name of the maintainer."""

__email__ = "robko01@8bitclub.com"
"""E-mail of the author."""

__status__ = "Debug"
"""File status."""

#endregion

class Robko01(Robko01Base):
    """Modbus TCP controller implementation (pymodbus)."""

#region Constructor

    def __init__(self, **kwargs):

        super().__init__()

        self.__logger = get_logger(__name__)
        """Logger."""

        host = kwargs.get("host")
        if not host:
            raise ValueError("Modbus TCP requires 'host'.")

        port = int(kwargs.get("port", 502))
        timeout = float(kwargs.get("timeout", 5))

        slave_id = kwargs.get("slave_id", kwargs.get("slave", 1))
        self.__slave_id = int(slave_id)

        pymodbus = _get_pymodbus()
        ModbusTcpClient = pymodbus.client.ModbusTcpClient

        self.__client = ModbusTcpClient(
            host=host,
            port=port,
            timeout=timeout,
        )

#endregion

#region Private Helpers

    def __to_signed(self, value):
        return value - 65536 if value > 32767 else value

    def __to_unsigned(self, value):
        return int(value) & 0xFFFF

    def __read_registers(self, address, count):
        result = self.__client.read_holding_registers(
            address=address, count=count, slave=self.__slave_id
        )
        if result.isError():
            raise RuntimeError(f"Modbus read error: {result}")
        return result.registers

    def __write_register(self, address, value):
        result = self.__client.write_register(
            address=address, value=value, slave=self.__slave_id
        )
        if result.isError():
            raise RuntimeError(f"Modbus write error: {result}")
        return result

    def __write_registers(self, address, values):
        result = self.__client.write_registers(
            address=address, values=values, slave=self.__slave_id
        )
        if result.isError():
            raise RuntimeError(f"Modbus write error: {result}")
        return result

    def __normalize_positions(self, target_position):
        if isinstance(target_position, (list, tuple)):
            if len(target_position) == 6:
                return [int(v) for v in target_position]
            if len(target_position) == 12:
                return [int(target_position[i]) for i in range(0, 12, 2)], [int(target_position[i]) for i in range(1, 12, 2)]
        raise ValueError("Target position must be a list of 6 or 12 values.")

#endregion

#region Public Methods

    def connect(self):
        return self.__client.connect()

    def disconnect(self):
        self.__client.close()

    def is_connected(self) -> bool:
        if hasattr(self.__client, "is_socket_open"):
            return bool(self.__client.is_socket_open())
        return False

    def stop(self):
        return self.__write_register(21, 1)

    def disable(self):
        return self.__write_register(12, 0)

    def enable(self):
        return self.__write_register(12, 1)

    def clear(self):
        self.__logger.warning("Clear is not supported by Modbus TCP. No action taken.")
        return None

    def set_speeds(self, speeds):
        if len(speeds) != 6:
            raise ValueError("Speeds must contain 6 values.")
        return self.__write_registers(14, [int(v) for v in speeds])

    def move_absolute(self, target_position):
        speeds = None
        if isinstance(target_position, (list, tuple)) and len(target_position) == 12:
            positions, speeds = self.__normalize_positions(target_position)
        else:
            positions = self.__normalize_positions(target_position)

        if speeds:
            safe_speeds = [abs(int(v)) for v in speeds]
            self.set_speeds(safe_speeds)

        unsigned_positions = [self.__to_unsigned(p) for p in positions]
        self.__write_registers(6, unsigned_positions)
        return self.__write_register(20, 1)

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
        busy = self.__read_registers(13, 1)[0]
        return 0x3F if busy else 0

    def current_position(self):
        positions = self.__read_registers(0, 6)
        positions = [self.__to_signed(p) for p in positions]
        expanded = []
        for pos in positions:
            expanded.extend([int(pos), 0])
        return expanded

    def get_inputs(self):
        return 0

    def set_outputs(self, value: int):
        return None

#endregion
