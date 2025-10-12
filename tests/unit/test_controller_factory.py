import pytest

from robko01.controllers.controller_factory import ControllerFactory


class DummyComm:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


def test_create_dummy_controller():
    # use the 'dummy' interface so no real communicator is created
    ctrl = ControllerFactory.create(interface="dummy", port="0", cname="dummy", timeout="1")
    assert ctrl is not None
    # Basic protocol conformance: duck-type check for expected methods
    assert hasattr(ctrl, "connect")
    assert hasattr(ctrl, "disconnect")


def test_create_orlin_with_mocked_serial(monkeypatch):
    # Replace the serial communicator class with a dummy one to avoid hardware
    from robko01.controllers import controller_factory as cf

    monkeypatch.setattr(cf, 'SerCom', DummyComm)

    ctrl = ControllerFactory.create(interface="serial", port="COM5", cname="orlin369", timeout="1")
    assert ctrl is not None
    assert hasattr(ctrl, "move_relative")


def test_bad_interface_raises():
    with pytest.raises(ValueError):
        ControllerFactory.create(interface=None, port="0", cname="dummy", timeout="1")


def test_unsupported_controller_raises():
    # Use the 'dummy' interface to avoid trying to open a real serial port
    with pytest.raises(NotImplementedError):
        ControllerFactory.create(interface="dummy", port="COM5", cname="unknown", timeout="1")
