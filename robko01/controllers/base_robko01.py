

from robko01.controllers.base import AbstractController
from robko01 import exceptions


class BaseRobko01(AbstractController):
    """Existing concrete base used across controllers.

    This class now subclasses :class:`AbstractController` so it becomes the
    canonical base type for all controllers in the package. It keeps the
    original attributes and provides default method stubs that raise
    appropriate package exceptions. Concrete controllers should override
    these methods.
    """

#region Attributes

#endregion


#region Properties



    # --- AbstractController method stubs ---
    def connect(self) -> None:
        """Open connection to the robot/hardware.

        By default this raises ControllerConnectionError; subclasses should
        implement real connection logic.
        """
        raise exceptions.ControllerConnectionError("connect() not implemented")

    def disconnect(self) -> None:
        """Close connection to the device and cleanup resources."""
        raise exceptions.ControllerError("disconnect() not implemented")

    def is_connected(self) -> bool:
        """Return True if controller is currently connected."""
        return False

    def move_relative(self, positions):
        """Move robot joints by relative amounts.

        Subclasses must implement this.
        """
        raise exceptions.ControllerProtocolError("move_relative() not implemented")

    def current_position(self):
        """Return the current position as a tuple of ints."""
        raise exceptions.ControllerError("current_position() not implemented")

    def set_timeout(self, seconds: float) -> None:
        """Set controller/communication timeout (store only).

        Note: actual read/send operations are performed by the communicator
        layer. Controllers may use this value when creating/configuring the
        communicator, but raw read/send methods are not part of the
        controller abstraction.
        """
        self._timeout = seconds
    # communicator-level methods (send_raw/read) removed from controller
    # base class. Communicators provide these operations and should be
    # mocked directly in unit tests.

#endregion
