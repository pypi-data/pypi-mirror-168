from flexnetsim.controller import *
import pytest
import os


class TestController:

    def test_constructor(self):
        c = Controller()

    def test_setters(self):
        c = Controller()
        c.network = Network()
        with pytest.raises(AttributeError):
            c.network = "net"

    def test_getters(self):
        c = Controller()
        absolute_path = os.path.abspath(__file__)
        current_folder = os.path.dirname(absolute_path)
        current_directory = os.path.dirname(current_folder)
        file = os.path.join(current_directory, 'test', 'NSFNet.json')
        c.network = Network(file)
        net = c.network
        assert net.is_connected(0, 2) == 2

    def test_allocator(self):
        def first_fit_algorithm(src: int, dst: int, b: Bitrate, c: Connection, n: Network, path):
            numberOfSlots = b.get_number_of_slots(0)
            link_ids = path[src][dst][0]
            general_link = []
            for _ in range(n.get_link(0).slots_number()):
                general_link.append(False)
            for link in link_ids:
                link = n.get_link(link)
                for slot in range(link.slots_number()):
                    general_link[slot] = general_link[slot] or link.get_slot(
                        slot)
            currentNumberSlots = 0
            currentSlotIndex = 0

            for j in range(len(general_link)):
                if not general_link[j]:
                    currentNumberSlots += 1
                else:
                    currentNumberSlots = 0
                    currentSlotIndex = j + 1
                if currentNumberSlots == numberOfSlots:
                    for k in link_ids:
                        c.add_link(
                            k, from_slot=currentSlotIndex, to_slot=currentSlotIndex+currentNumberSlots)
                    return Controller.status.ALLOCATED, c
            return Controller.status.NOT_ALLOCATED, c

        c = Controller()
        absolute_path = os.path.abspath(__file__)
        current_folder = os.path.dirname(absolute_path)
        current_directory = os.path.dirname(current_folder)
        file = os.path.join(current_directory, 'test', 'NSFNet.json')
        c.network = Network(file)
        c.allocator = first_fit_algorithm
        file = os.path.join(current_directory, 'test', 'routes.json')
        c.set_paths(file)
        b = Bitrate(10)
        b.add_modulation("BPSK", 2, 10000)
        c.assignConnection(0, 1, b, 1)
        assert c.assignConnection(0, 1, b, 2) == Controller.status.ALLOCATED
        b = Bitrate(10)
        b.add_modulation("BPSK", 2000, 10000)
        assert c.assignConnection(
            0, 1, b, 3) == Controller.status.NOT_ALLOCATED
        assert c.network.is_slot_used(0, slot_pos=0)
        assert c.network.is_slot_used(0, slot_pos=1)
        assert c.network.is_slot_used(0, slot_pos=2)
        assert c.network.is_slot_used(0, slot_pos=3)
        assert not c.network.is_slot_used(0, slot_pos=4)
        assert not c.network.is_slot_used(0, slot_pos=5)
        assert not c.network.is_slot_used(0, slot_pos=6)
        assert c.allocator != None

        c.unassignConnection(2)
        assert c.network.is_slot_used(0, slot_pos=0)
        assert c.network.is_slot_used(0, slot_pos=1)
        assert not c.network.is_slot_used(0, slot_pos=2)
        assert not c.network.is_slot_used(0, slot_pos=3)
        assert not c.network.is_slot_used(0, slot_pos=4)
        assert not c.network.is_slot_used(0, slot_pos=5)
        assert not c.network.is_slot_used(0, slot_pos=6)

        c.unassignConnection(1)
        assert not c.network.is_slot_used(0, slot_pos=0)
        assert not c.network.is_slot_used(0, slot_pos=1)
        assert not c.network.is_slot_used(0, slot_pos=2)
        assert not c.network.is_slot_used(0, slot_pos=3)
        assert not c.network.is_slot_used(0, slot_pos=4)
        assert not c.network.is_slot_used(0, slot_pos=5)
        assert not c.network.is_slot_used(0, slot_pos=6)
