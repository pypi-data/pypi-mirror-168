from flexnetsim.connection import *
import pytest


class TestConnection:

    def test_constructor(self):
        connection1 = Connection(1)
        with pytest.raises(AttributeError):
            Connection()

    def test_add_link(self):
        connection2 = Connection(1)
        connection2.add_link(2, slots=[1, 2, 3])
        assert connection2.links[0] == 2
        assert connection2.slots[0] == [1, 2, 3]
        connection2.add_link(4, from_slot=5, to_slot=7)
        assert connection2.links[1] == 4
        assert connection2.slots[1] == [5, 6]
        with pytest.raises(AttributeError):
            connection2.add_link(4, slots=[3, 4, 5], from_slot=5, to_slot=7)
