from flexnetsim.link import *
import pytest


class TestLink:
    def test_constructor(self):
        Link(5)
        Link(5, 500)
        Link(3, 700, 500)

    def test_id(self):
        l1 = Link()
        assert l1.id == -1

        l2 = Link(id=2)
        assert l2.id == 2

        l3 = Link(id=-10)
        assert l3.id == -10

        l4 = Link()
        l4.id = 10
        with pytest.raises(ValueError):
            l4.id = -10

    def test_length(self):
        with pytest.raises(ValueError):
            Link(length=0)
        with pytest.raises(ValueError):
            Link(length=-50)

        l2 = Link(length=100)
        assert l2.length == 100

        l3 = Link()
        with pytest.raises(ValueError):
            l3.length = -10

        l4 = Link()
        l4.length = 10

    def test_slots(self):
        with pytest.raises(ValueError):
            Link(slots=0)
        with pytest.raises(ValueError):
            Link(slots=-50)

        l2 = Link(slots=400)
        assert (
            l2.slots_number() == 400
        )
        l3 = Link()
        with pytest.raises(ValueError):
            l3.set_slots(0)
        l3.set_slots(10)

        l4 = Link()
        l4.set_slot(0, True)
        with pytest.raises(ValueError):
            l4.set_slots(5)
        with pytest.raises(ValueError):
            l4.set_slot(-1, True)
            l4.set_slot(l4.slots_number, True)
        with pytest.raises(ValueError):
            l4.set_slot(0, True)
        assert len(l4.slots) != 0
        with pytest.raises(ValueError):
            l4.get_slot(-1)
        with pytest.raises(ValueError):
            l4.get_slot(320)

    def test_ends(self):
        l1 = Link()
        l1.src = 2
        l1.dst = 1

        assert l1.src == 2
        assert l1.dst == 1
