from flexnetsim.node import *
import pytest


class TestNode:

    def test_constructor(self):
        Node()
        Node(0)
        Node(1, "Test node 1")

    def test_getting_id(self):
        node1 = Node()
        assert node1.id == -1

        node2 = Node(id=2)
        assert node2.id == 2

    def test_setting_id(self):
        node1 = Node()
        node1.id = 3
        assert node1.id == 3

        node2 = Node()
        node2.id = 4
        assert node2.id == 4
        with pytest.raises(ValueError):
            node2.id = 5
        ##############################
        node3 = Node()
        node3.id = 10
        assert (node3.id == 5) == False
        ##############################

    def test_setting_label(self):
        node1 = Node()
        node1.label = "testing node"
        assert node1.label == "testing node"
