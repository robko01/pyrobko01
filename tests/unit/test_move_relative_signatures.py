import pytest
from unittest.mock import MagicMock

from robko01.controllers.dummy.robko01 import Robko01 as DummyRob
from robko01.controllers.orlin369.robko01 import Robko01 as OrlinRob
from robko01.controllers.valentin_nikolov.robko01 import Robko01 as ValRob
from robko01.controllers.tu_gabrovo.robko01 import Robko01 as TugRob


@pytest.mark.parametrize(
    "controller_cls",
    [DummyRob, OrlinRob, ValRob, TugRob],
)
def test_move_relative_supports_both_signatures(controller_cls):
    # create instance without running __init__ to avoid communicator wiring
    inst = controller_cls.__new__(controller_cls)

    # attach a mock implementation for the internal implementation
    mock_impl = MagicMock(return_value="ok")
    inst._move_relative_impl = mock_impl

    # unified signature: pass a 12-element positions list
    positions = [0] * 12
    positions[0] = 100
    positions[1] = 50

    result1 = inst.move_relative(positions)
    assert mock_impl.called
    # accept either a single positions list call (new API) or
    # legacy per-joint calls (tu_gabrovo implementation)
    call_args = mock_impl.call_args
    args, kwargs = call_args
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        assert list(args[0]) == positions
    else:
        # legacy call: expect joint, delay, steps tuple matching first joint
        assert len(args) >= 3
        assert args[0] == 0
        assert args[1] == 50
        assert args[2] == 100

    mock_impl.reset_mock()

    # legacy signature: joint, delay, steps
    res2 = inst.move_relative(0, 50, 100)
    assert mock_impl.called

