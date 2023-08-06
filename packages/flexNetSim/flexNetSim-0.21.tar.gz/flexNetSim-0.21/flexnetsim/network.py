from .node import Node
from .link import Link
import json


class Network():
    """Class with the network information.

    The Network class is used to represent an Optical Fiber Network architecture,
    made up with connection Links and Nodes, inside the simulator. 
    Hence, Network class requires and implements Link and Node objects.

    The Network class consists of several methods for adding Links and Nodes, for
    connecting them, check connection, use/unuse slots in Links, and getting metrics.

    Attributes:
        link_counter (int): Counter that stores the last Link ID that entered the network. Used for knowing if a new Link can enter the Network.

        node_counter (int): Counter that stores the last Node ID that entered the network. Used for knowing if a new Node can enter the Network.

        nodes (list(:obj: Node)): List of Node objects available in the Network.

        links (list(:obj: Link)): List of Link objects available in the Network.

        links_in (list(:obj: Link)): List of Link objects going into the Nodes ordered by ID. Eg: In a Network with 3 Nodes,
        the links going into Node 0 would be before the links going into Node 1 and Node 2.

        links_out (list(:obj: Link)): List of Link objects going out of the Nodes ordered by Id. Eg: In a Network with 3 Nodes,
        the links going ouy of Node 0 would be before the linkg going out of Node 1 and Node 2.

        nodes_in (list(int)): List of ints representing the accumulative number of links going into the Nodes, where each
        position in the list is the ID of a Node + 1. Eg: In a Network with 3 Nodes, 2 links going into Node 0, 1 into Node 1
        and 2 into Node 2, nodes_in would look like this: [0,2,3,5]. This is used to extract the links from the links_in attribute
        in the is_connected method.

        nodes_out (list(int)): List of ints representing the accumulative number if links going out from the Nodes, where each
        position in the list is the ID of a Node + 1. Eg: In a Network with 3 Nodes, 1 links going out from Node 0, 2 from Node 1
        and 2 from Node 2, nodes_out would look like this: [0,1,3,5]. This is used to extract the links from the links_out attribute
        in the is_connected method.
    """

    def __init__(self, arg=None):
        """
        Init method of class Network

        Args:
            arg (filepath or :obj: Network): either a path to a JSON file or a previously built Network object. Example of
            valid JSON file: "NSFNet.json"

        Example:
            code-block:: JSON
            {
                "name": "4-node bus",
                "alias": "example",
                "nodes": [
                    {
                        "id": 0
                    },
                    {
                        "id": 1
                    },
                    {
                        "id": 2
                    },
                    {
                        "id": 3
                    },
                ],
                "links": [
                    {
                    "id": 0,
                    "src": 0,
                    "dst": 1,
                    "lenght": 1130,
                    "slots": 100
                    },
                    {
                    "id": 1,
                    "src": 0,
                    "dst": 2,
                    "lenght": 1710,
                    "slots": 100
                    },
                    {
                    "id": 3,
                    "src": 1,
                    "dst": 2,
                    "lenght": 700,
                    "slots": 100
                        },
                    ]
            };

        """
        self.__link_counter = 0
        self.__node_counter = 0
        self.__nodes = []
        self.__links = []
        self.__links_in = []
        self.__links_out = []
        self.__nodes_in = []
        self.__nodes_out = []

        self.nodes_in.append(0)
        self.nodes_out.append(0)

        if arg != None:
            if isinstance(arg, Network):
                self.__link_counter = arg.link_counter
                self.__node_counter = arg.node_counter
                self.__nodes = arg.nodes
                self.__links = arg.links
                self.__links_in = arg.links_in
                self.__links_out = arg.links_out
                self.__nodes_in = arg.nodes_in
                self.__nodes_out = arg.nodes_out
            else:
                f = open(arg)
                NSFnet = json.load(f)
                f.close()
                nummber_of_nodes = len(NSFnet["nodes"])
                number_of_links = len(NSFnet["links"])
                for i in range(0, nummber_of_nodes):
                    id = NSFnet["links"][i]["id"]
                    node = Node(id)
                    self.add_node(node)

                for i in range(0, number_of_links):
                    id = NSFnet["links"][i]["id"]
                    length = NSFnet["links"][i]["length"]
                    slots = NSFnet["links"][i]["slots"]
                    link = Link(id, length, slots)
                    self.add_link(link)

                    src = NSFnet["links"][i]["src"]
                    id = NSFnet["links"][i]["id"]
                    dst = NSFnet["links"][i]["dst"]
                    self.connect(src, id, dst)

    @property
    def nodes(self):
        """
        Getter a list of the nodes in the Network
        """
        return self.__nodes

    @property
    def links(self):
        """
        Getter a list of the links in the Network
        """
        return self.__links

    @property
    def node_counter(self):
        """
        Getter and setter for a counter of nodes within the Network
        """
        return self.__node_counter

    @property
    def nodes_in(self):
        """
        Getter of a list representing the links going into a node in the Network
        """
        return self.__nodes_in

    @property
    def nodes_out(self):
        """
        Getter of a list representing the links coming out from a node in the Network
        """
        return self.__nodes_out

    @property
    def link_counter(self):
        """
        Getter and setter for a counter for links within Network
        """
        return self.__link_counter

    @property
    def links_out(self):
        """
        Getter a list of the links coming out from the nodes in the Network
        """
        return self.__links_out

    @property
    def links_in(self):
        """
        Getter a list of the links going into the nodes in the Network
        """
        return self.__links_in

    def get_link(self, link_pos: int):
        """
        Gets the Link object at a index position "pos" inside Links list.

        Args:
            link_pos (int): the position of the Link inside Links list

        Returns:
            :obj: Link: the Link located at the required position.
        """
        if(link_pos < 0) or (link_pos >= len(self.links)):
            raise ValueError("Cannot get Link from a position out of bounds.")
        return self.__links[link_pos]

    def get_node(self, node_pos: int):
        """
        Gets the Node at a index position "pos" inside the Nodes list.

        Args:
            node_pos (int): the position of the Node inside Nodes list.

        Returns:
            :obj: Node: the Node located at the required position.
        """
        if (node_pos < 0) or (node_pos >= len(self.nodes)):
            raise ValueError("Cannot get Node from a position out of bounds.")
        return self.__nodes[node_pos]

    def add_node(self, node: Node):
        """
        Adds a new Node object to the Network object. To add a new Node to a
        Network, the new Node's Id must match the amount of nodes that were already on the network.

        Args:
            :obj: Node: the Node desired to be added into the Network object.
        """
        if node.id != self.node_counter:
            raise ValueError(
                "Cannot add a Node to this network with Id mismatching node counter.")
        self.__node_counter += 1
        self.__nodes.append(node)
        self.__nodes_in.append(0)
        self.__nodes_out.append(0)

    def add_link(self, link: Link):
        """
        Adds a new Link object to the Network object. To add a new Link to a
        Network, the new Link's Id must match the amount of links that were already on the network.

        Args:
            :obj: Link: the Link desired to be added into the Network object.
        """
        if link.id != self.link_counter:
            raise ValueError(
                "Cannot add a Link to this network with Id mismatching link counter.")
        self.__link_counter += 1
        self.__links.append(link)

    def connect(self, src: int, link_pos: int, dst: int):
        """
        The Connect methods establishes an Optical Fiber connection between two Nodes through a Link inside the Network object. 
        The different connections between the different Links and Nodes of the Network build up
        the Network's architecture.

        To connect the two Nodes through a Link, both Link and (the 2) Nodes must already exist inside the Network object, that is,
        they need to have been added previously.

        Args:
            src (int): the Id/position of the source node of the connection.
            link_pos (int): the Id/position of the Link used to connect the nodes.
            dst (int): the Id/position of the destination node of the connection.
        """
        if(src < 0) or (src >= self.node_counter):
            raise ValueError(
                f"Cannot connect src {src} because its ID is not in the network. Number of nodes in network: {self.node_counter}")

        if(dst < 0) or (dst >= self.__node_counter):
            raise ValueError(
                f"Cannot connect dst {dst} because its ID is not in the network. Number of nodes in network: {self.node_counter}")

        if(link_pos < 0) or (link_pos >= self.__link_counter):
            raise ValueError(
                f"Cannot use link {link_pos} because its ID is not in the network. Number of links in network: {self.link_counter}")

        self.__links_out.insert(self.__nodes_out[src], self.__links[link_pos])
        for i in range((src+1), len(self.__nodes_out)):
            self.__nodes_out[i] += 1
        self.__links_in.insert(self.__nodes_in[dst], self.__links[link_pos])
        for i in range((dst+1), len(self.__nodes_in)):
            self.__nodes_in[i] += 1
        self.__links[link_pos].src = src
        self.__links[link_pos].dst = dst

    def is_connected(self, src: int, dst: int):
        """
        The isConnected method checks if the source and destination Nodes are connected through a Link. If there's a connection between the two Nodes
        through a Link, the Id/position of that Link is returned; otherwise, -1 is returned.

        Args:
            src (int): the Id/position of the source node of the connection to be checked.
            dst (int): the Id/position of the destination node of the connection to be checked.
        """
        for i in range(self.nodes_out[src], self.nodes_out[src+1]):
            for j in range(self.nodes_in[dst], self.nodes_in[dst+1]):
                if self.links_out[i].id == self.links_in[j].id:
                    return self.links_out[i].id
        return -1

    def use_slot(self, link_pos: int, *, slot_pos: int = None, slot_from: int = None, slot_to: int = None):
        """
        The useSlot method activates either a single Slot or range of slots inside a Link of a given position inside the Network.

        The range of slots starts from the given position slotFrom and activates all the slots up to the (slotTo - 1) position.

        You must use one of these two options:
        * Use only slot_pos parameter
        * Use only from_slot and to_slot parameters

        Args:
            link_pos (int): the position of the Link inside the links list.
            slot_pos (int): the position of the single Slot to be used/activated inside the slot list.
            link_from (int): the starting position of the Slots to be used/activated inside the slot list.
            link_to (int): the limit before the ending position of the Slots to be used/activated inside the slot list (activates up to the (slotTo - 1)th slot). It's value must be greater than slotFrom.
        """
        if (link_pos < 0) or (link_pos >= len(self.links)):
            raise ValueError("Link position out of bounds")
        if (slot_pos != None) and (slot_from == None) and (slot_to == None):
            if(slot_pos < 0) or (slot_pos >= self.__links[link_pos].slots_number()):
                raise ValueError("Slot position out of bounds.")
            self.__links[link_pos].set_slot(slot_pos, True)

        elif (slot_pos == None) and (slot_from != None) and (slot_to != None):
            if(slot_from < 0) or (slot_from >= self.__links[link_pos].slots_number()):
                raise ValueError("Slot position out of bounds.")
            if(slot_to < 0) or (slot_to >= self.__links[link_pos].slots_number()):
                raise ValueError("Slot position out of bounds.")
            if(slot_from > slot_to):
                raise ValueError(
                    "Initial slot position must be lower than the final slot position.")
            if(slot_from == slot_to):
                raise ValueError("Slot from and slot To cannot be equals.")

            for i in range(slot_from, slot_to):
                self.__links[link_pos].set_slot(i, True)

        else:
            raise ValueError("Incorrect arguments given.")

    def unuse_slot(self, link_pos: int, *, slot_pos: int = None, slot_from: int = None, slot_to: int = None):
        """
        The unuseSlot method deactivates either a single Slot or a range of slots inside a Link of a given position inside the Network.

        The range of slots starts from the given position slotFrom and deactivates all the slots up to the (slotTo - 1) position

        You must use one of these two options:
        * Use only slot_pos parameter
        * Use only from_slot and to_slot parameters

        Args:
            link_pos (int): the position of the Link inside the links list.
            slot_pos (int): the position of the single Slot to be unused/deactivated inside the slot list.
            link_from (int): the starting position of the Slots to be unused/deactivated the slot list.
            link_to (int): the limit before the ending position of the Slots to be unused/deactivated inside the slot list (activates up to the (slotTo - 1)th slot). It's value must be greater than slotFrom.
        """
        if (link_pos < 0) or (link_pos >= len(self.links)):
            raise ValueError("Link position out of bounds")
        if (slot_pos != None) and (slot_from == None) and (slot_to == None):
            if(slot_pos < 0) or (slot_pos >= self.__links[link_pos].slots_number()):
                raise ValueError("Slot position out of bounds.")
            self.__links[link_pos].set_slot(slot_pos, False)

        elif (slot_pos == None) and (slot_from != None) and (slot_to != None):
            if(slot_from < 0) or (slot_from >= self.__links[link_pos].slots_number()):
                raise ValueError("Slot position out of bounds.")
            if(slot_to < 0) or (slot_to >= self.__links[link_pos].slots_number()):
                raise ValueError("Slot position out of bounds.")
            if(slot_from > slot_to):
                raise ValueError(
                    "Initial slot position must be lower than the final slot position.")
            if(slot_from == slot_to):
                raise ValueError("Slot from and slot To cannot be equals.")

            for i in range(slot_from, slot_to):
                self.__links[link_pos].set_slot(i, False)

        else:
            raise ValueError("Incorrect arguments given.")

    def is_slot_used(self, link_pos: int, *, slot_pos: int = None, slot_from: int = None, slot_to: int = None):
        """
        The isSlotUsed method determines whether a single slot or a range of Slots in the specified Link are already being used or not.

        You must use one of these two options:
        * Use only slot_pos parameter
        * Use only from_slot and to_slot parameters

        Args:
            link_pos (int): the position of the specified Link to check it's Slot inside the links list.
            slot_pos (int): the position of the specified Slot to check inside the slots (inside the specified Link).
            link_from (int): the starting position of the Slots to be checked if they are being used inside the slot list.
            link_to (int):the limit before the ending position of the Slots to be checked if they are being used inside the slot list (checks up to the (slotTo - 1)th slot). It's value must be greater than slotFrom.

        Returns:
            bool: The condition of either the specified Slot or the range of Slots. For the single Slot case, if it's active it returns true, otherwise it returns false.
            For the range of Slots case if it finds at least one Slot activated/used then the entire desired range of Slots is considered used and returns true, otherwise they are all unused returns false.
        """
        if (link_pos < 0) or (link_pos >= len(self.links)):
            raise ValueError("Link position out of bounds")
        if (slot_pos != None) and (slot_from == None) and (slot_to == None):
            if(slot_pos < 0) or (slot_pos >= self.__links[link_pos].slots_number()):
                raise ValueError("Slot position out of bounds.")
            return self.__links[link_pos].get_slot(slot_pos)

        elif (slot_pos == None) and (slot_from != None) and (slot_to != None):
            if(slot_from < 0) or (slot_from >= self.__links[link_pos].slots_number()):
                raise ValueError("Slot position out of bounds.")
            if(slot_to < 0) or (slot_to >= self.__links[link_pos].slots_number()):
                raise ValueError("Slot position out of bounds.")
            if(slot_from > slot_to):
                raise ValueError(
                    "Initial slot position must be lower than the final slot position.")
            if(slot_from == slot_to):
                raise ValueError("Slot from and slot To cannot be equals.")

            for i in range(slot_from, slot_to):
                if self.__links[link_pos].get_slot(i):
                    return True
            return False

        else:
            raise ValueError("Incorrect arguments given.")

    def average_neighborhood(self):
        """
        The averageNeighborhood method obtains the Nodal average metric of the Network.

        Returns:
            float: The Nodal neighborhood average metric value.
        """
        if self.node_counter == 0:
            raise ValueError("The network must be have at least one node.")
        result = self.__link_counter/self.__node_counter
        return result

    def normal_average_neighborhood(self):
        """
        The normalAverageNeighborhood method obtains the Normalized/Standarized Nodal average metric of the Network.

        Returns:
            float: The Normalized Nodal neighborhood average metric value, 1 representing Full Connection and 0 representing Null Connection.
        """
        if self.node_counter == 0:
            raise ValueError("The network must be have at least one node.")
        result = self.__link_counter / \
            (self.__node_counter * (self.__node_counter - 1))
        return result

    def nodal_variance(self):
        """
        The nodalVariance method obtains the Nodal Variance given the Nodal Average.

        Returns:
            float: The Nodal Variance value of average neighborhood
        """
        if self.node_counter == 0:
            raise ValueError("The network must be have at least one node.")
        result = 0.0
        average = self.average_neighborhood()
        for i in range(self.__node_counter):
            result += pow((self.__nodes_out[i+1] -
                          self.__nodes_out[i])-average, 2)
        result /= self.__node_counter
        return result
