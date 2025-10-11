"""Communicator base protocol.

Lightweight ABC that describes the communicator surface used by controllers.
This makes it easy to mock communicators in tests.
"""
from abc import ABC, abstractmethod


class CommunicatorBase(ABC):

#region Constructor

    def __init__(self) -> None:
        super().__init__()

        self.__timeout = 5
        """Timeout in second.
        """

#endregion

#region Properties

    @property
    def timeout(self):
        """Timeout

        Returns:
            float: Timeout value.
        """
        return self.__timeout

    @timeout.setter
    def timeout(self, value):
        """Timeout

        Args:
            value (float): Timeout value.
        """
        self.__timeout = value

#endregion

#region Public Methods

    @abstractmethod
    def connect(self) -> None:
        """Connect to the device.
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from device.
        """
        pass

    @abstractmethod
    def reset(self):
        """Reset target device.
        """
        pass

    @abstractmethod
    def send(self, payload):
        """Send
        """
        pass

    @abstractmethod
    def receive(self):
        """Receive
        """
        pass

    @abstractmethod
    def send_frame(self, req_frame):
        """Send frame.

        Args:
            req_frame (bytes): Request frame.
        """
        pass

#endregion
