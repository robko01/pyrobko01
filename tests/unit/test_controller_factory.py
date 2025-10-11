import pytest

from robko01.controllers.controller_factory import ControllerFactory


class DummyComm:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


def test_create_dummy_controller():
    ctrl = ControllerFactory.create(interface="serial", port="0", cname="dummy", timeout="1")
    assert ctrl is not None


def test_create_orlin_with_mocked_serial(monkeypatch):
    # Replace the serial communicator class with a dummy one to avoid hardware
    from robko01.controllers import controller_factory as cf

    monkeypatch.setattr(cf, 'SerCom', DummyComm)

    ctrl = ControllerFactory.create(interface="serial", port="COM5", cname="orlin369", timeout="1")
    assert ctrl is not None


def test_bad_interface_raises():
    with pytest.raises(ValueError):
        ControllerFactory.create(interface=None, port="0", cname="dummy", timeout="1")


def test_unsupported_controller_raises():
    with pytest.raises(NotImplementedError):
        ControllerFactory.create(interface="serial", port="COM5", cname="unknown", timeout="1")
