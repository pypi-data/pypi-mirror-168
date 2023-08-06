from flexnetsim.network import *
import pytest
import os
import math


class TestNetwork:

    def test_constructor(self):
        Network()

    def test_constructor_json(self):
        absolute_path = os.path.abspath(__file__)
        current_folder = os.path.dirname(absolute_path)
        current_directory = os.path.dirname(current_folder)
        file = os.path.join(current_directory, 'test', 'NSFNet.json')
        Network(file)

    def test_get_node_position(self):
        n1 = Network()
        with pytest.raises(ValueError):
            n1.add_node(Node(10))
        n1.add_node(Node(0))

        assert n1.get_node(0).id == 0
        with pytest.raises(ValueError):
            n1.get_node(-1)
        with pytest.raises(ValueError):
            n1.get_node(-50)

    def test_get_link_postion(self):
        n1 = Network()
        with pytest.raises(ValueError):
            n1.add_link(Link(10))
        n1.add_link(Link(0))
        assert n1.get_link(0).id == 0
        with pytest.raises(ValueError):
            n1.get_link(-1)
        with pytest.raises(ValueError):
            n1.get_link(-50)

    def test_copy_constructor(self):
        n1 = Network()
        n1.add_node(Node(0))
        n1.add_link(Link(0))
        n2 = Network(n1)
        assert n1.get_node(0).id == n2.get_node(0).id
        assert n1.get_link(0).id == n2.get_link(0).id
        with pytest.raises(ValueError):
            n1.get_node(-1).id == n2.get_node(-1).id

    def test_connect(self):
        net1 = Network()
        net1.add_node(Node(0))
        n1_pos = net1.get_node(0).id
        net1.add_node(Node(1))
        n2_pos = net1.get_node(1).id
        net1.add_link(Link(0))
        l1_pos = net1.get_link(0).id
        net1.connect(n1_pos, l1_pos, n2_pos)
        with pytest.raises(ValueError):
            net1.connect(-1, l1_pos, n2_pos)
        with pytest.raises(ValueError):
            net1.connect(n1_pos, l1_pos, 3)
        with pytest.raises(ValueError):
            net1.connect(n1_pos, 2, n2_pos)

        assert net1.is_connected(n1_pos, n2_pos) == 0
        assert net1.link_counter == 1
        assert net1.node_counter == 2

        net2 = Network()
        net2.add_node(Node(0))
        with pytest.raises(ValueError):
            net2.connect(0, 0, -1)
        with pytest.raises(ValueError):
            net2.connect(0, 0, 0)

    def test_json_constructor(self):
        absolute_path = os.path.abspath(__file__)
        current_folder = os.path.dirname(absolute_path)
        current_directory = os.path.dirname(current_folder)
        file = os.path.join(current_directory, 'test', 'NSFNet.json')
        n1 = Network(file)

    def test_use_slot(self):
        net1 = Network()
        l1 = Link(0, 70, 200)
        net1.add_link(l1)
        assert l1.get_slot(100) == False
        with pytest.raises(ValueError):
            net1.use_slot(-10, slot_pos=100)
        with pytest.raises(ValueError):
            net1.use_slot(0, slot_pos=200)
        with pytest.raises(ValueError):
            net1.use_slot(0, slot_pos=-1)
        with pytest.raises(ValueError):
            net1.use_slot(0, slot_from=-1, slot_to=10)
        with pytest.raises(ValueError):
            net1.use_slot(0, slot_from=320, slot_to=321)
        with pytest.raises(ValueError):
            net1.use_slot(0, slot_from=0, slot_to=-1)
        with pytest.raises(ValueError):
            net1.use_slot(0, slot_from=0, slot_to=321)
        with pytest.raises(ValueError):
            net1.use_slot(0, slot_from=0, slot_to=0)

        net1.use_slot(0, slot_pos=100)
        assert l1.get_slot(100) == True
        assert net1.get_link(0).get_slot(100) == True

        net2 = Network()
        l2 = Link(0, 70, 200)
        net2.add_link(l2)
        assert l2.get_slot(100) == False
        net2.use_slot(0, slot_from=100, slot_to=104)
        with pytest.raises(ValueError):
            net2.use_slot(-10, slot_from=100, slot_to=104)
        with pytest.raises(ValueError):
            net2.use_slot(0, slot_from=104, slot_to=100)
        assert l2.get_slot(100) == True
        assert net2.get_link(0).get_slot(100) == True
        assert net2.get_link(0).get_slot(101) == True
        assert net2.get_link(0).get_slot(102) == True
        assert net2.get_link(0).get_slot(103) == True

    def test_json_of_nsfnet(self):
        absolute_path = os.path.abspath(__file__)
        current_folder = os.path.dirname(absolute_path)
        current_directory = os.path.dirname(current_folder)
        file = os.path.join(current_directory, 'test', 'NSFNet.json')
        net = Network(file)
        adjacency_matrix = [
            [-1, 0, 2, -1, -1, -1, -1, 4, -1, -1, -1, -1, -1, -1],
            [1, -1, 6, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [3, 7, -1, -1, -1, 10, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, 9, -1, -1, 12, -1, -1, -1, -1, -1, 14, -1, -1, -1],
            [-1, -1, -1, 13, -1, 16, 18, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, 11, -1, 17, -1, -1, -1, -1, 20, -1, -1, -1, 22],
            [-1, -1, -1, -1, 19, -1, -1, 24, -1, -1, -1, -1, -1, -1],
            [5, -1, -1, -1, -1, -1, 25, -1, 26, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, 27, -1, 28, -1, 30, 32, -1],
            [-1, -1, -1, -1, -1, 21, -1, -1, 29, -1, -1, -1, -1, -1],
            [-1, -1, -1, 15, -1, -1, -1, -1, -1, -1, -1, 34, 36, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, 31, -1, 35, -1, -1, 38],
            [-1, -1, -1, -1, -1, -1, -1, -1, 33, -1, 37, -1, -1, 40],
            [-1, -1, -1, -1, -1, 23, -1, -1, -1, -1, -1, 39, 41, -1]
        ]
        for i in range(14):
            for j in range(14):
                assert(net.is_connected(i, j) == adjacency_matrix[i][j])

    def test_connect_link(self):
        net = Network()
        n1 = Node(0)
        n2 = Node(1)
        l1 = Link(0, 70, 200)
        assert(l1.src == -1)
        assert(l1.dst == -1)

        net.add_node(n1)
        net.add_node(n2)
        net.add_link(l1)
        net.connect(0, 0, 1)
        assert l1.src == n1.id
        assert l1.dst == n2.id

    def test_metric_features(self):
        net_clean = Network()
        absolute_path = os.path.abspath(__file__)
        current_folder = os.path.dirname(absolute_path)
        current_directory = os.path.dirname(current_folder)
        file = os.path.join(current_directory, 'test', 'NSFNet.json')
        net = Network(file)
        with pytest.raises(ValueError):
            net_clean.average_neighborhood()
        with pytest.raises(ValueError):
            net_clean.normal_average_neighborhood()
        with pytest.raises(ValueError):
            net_clean.nodal_variance()

        print(net.nodal_variance())

        assert math.isclose(net.average_neighborhood(), 3, rel_tol=0.01)
        assert math.isclose(
            net.normal_average_neighborhood(), 0.23, rel_tol=0.01)
        assert math.isclose(net.nodal_variance(), 0.2857, rel_tol=0.01)

    def test_unuse_slots(self):
        net = Network()
        link = Link(0, 70, 200)
        net.add_link(link)
        net.use_slot(0, slot_pos=0)
        net.use_slot(0, slot_from=190, slot_to=199)

        with pytest.raises(ValueError):
            net.unuse_slot(-1, slot_pos=0)
        with pytest.raises(ValueError):
            net.unuse_slot(3, slot_pos=0)
        with pytest.raises(ValueError):
            net.unuse_slot(-1, slot_to=199, slot_from=190)
        with pytest.raises(ValueError):
            net.unuse_slot(3, slot_from=190, slot_to=199)

        with pytest.raises(ValueError):
            net.unuse_slot(0, slot_from=201, slot_to=205)
        with pytest.raises(ValueError):
            net.unuse_slot(0, slot_from=0, slot_to=-1)
        with pytest.raises(ValueError):
            net.unuse_slot(0, slot_from=2, slot_to=1)
        with pytest.raises(ValueError):
            net.unuse_slot(0, slot_pos=-1)

        with pytest.raises(ValueError):
            net.unuse_slot(0, slot_from=190, slot_to=190)

        net.unuse_slot(0, slot_to=199, slot_from=190)
        net.unuse_slot(0, slot_pos=0)

    def test_is_slot_used(self):
        net = Network()
        link = Link(0, 70, 200)
        net.add_link(link)
        net.use_slot(0, slot_pos=0)
        net.use_slot(0, slot_from=190, slot_to=199)

        assert net.is_slot_used(0, slot_from=190, slot_to=199) == True
        assert net.is_slot_used(0, slot_pos=0) == True
        assert net.is_slot_used(0, slot_from=180, slot_to=185) == False
        assert net.is_slot_used(0, slot_pos=10) == False

        with pytest.raises(ValueError):
            net.is_slot_used(-1, slot_pos=0)
        with pytest.raises(ValueError):
            net.is_slot_used(3, slot_pos=0)
        with pytest.raises(ValueError):
            net.is_slot_used(-1, slot_from=190, slot_to=199)
        with pytest.raises(ValueError):
            net.is_slot_used(-3, slot_from=190, slot_to=199)

        with pytest.raises(ValueError):
            net.is_slot_used(0, slot_from=201, slot_to=205)
        with pytest.raises(ValueError):
            net.is_slot_used(0, slot_from=190, slot_to=-1)
        with pytest.raises(ValueError):
            net.is_slot_used(0, slot_from=190, slot_to=205)
        with pytest.raises(ValueError):
            net.is_slot_used(0, slot_pos=-1)

        with pytest.raises(ValueError):
            net.is_slot_used(0, slot_from=190, slot_to=190)
        with pytest.raises(ValueError):
            net.is_slot_used(0, slot_from=191, slot_to=190)

    def test_argument_errors(self):
        net = Network()
        link = Link(0, 70, 200)
        net.add_link(link)
        with pytest.raises(ValueError):
            net.use_slot(0, slot_pos=0, slot_to=50)
        with pytest.raises(ValueError):
            net.use_slot(0, slot_pos=190, slot_from=190, slot_to=199)

        net.use_slot(0, slot_pos=0)
        net.use_slot(0, slot_from=190, slot_to=199)

        with pytest.raises(ValueError):
            net.is_slot_used(0, slot_pos=0, slot_to=50)
        with pytest.raises(ValueError):
            net.is_slot_used(0, slot_pos=0, slot_to=50)
        with pytest.raises(ValueError):
            net.unuse_slot(0, slot_pos=0, slot_to=199)
        with pytest.raises(ValueError):
            net.unuse_slot(0, slot_pos=0, slot_from=190, slot_to=199)
