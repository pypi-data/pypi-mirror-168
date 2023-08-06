import os
import sys
from .network import Network
from .connection import Connection
from .bitrate import Bitrate
from enum import Enum
import json


class Controller:
    """
    This class allows you to create the object Controller and manipulate it by
    its methods. The importance of this object is that it handles connection
    requests generated inside the Simulator by executing an allocation algorithm
    from the Allocator object on the network. Once the process is completed, it
    returns the result to the simulator. The Controller is the link between the
    Simulator and the Network.

    Attributes:
        network (Network): Object that contains all the information about the network, 
        nodes, routes, path length and slots.

        allocator (Allocator): The Allocator object handles the assignment of connections 
        inside a Network.

        path (list(list(list))): Paths in the network. These are represented by three lists
        [source][destination][path]. Source and destination are Nodes, and [path] is the path
        between this two nodes, these nodes may have zero or more available paths. For example:
        source node = 2, destination node = 5, and path number 2. The result is the path [2,4,6,8,5].

        connections (list(Connection)): List of Connection objects. Connection contains the 
        information regarding the connections that are made between the nodes on a network 
        during the allocation process.


        allocationStatus (status): Result of the allocation process, whether the
        allocation was succesful or not. This is type allocationStatus, there are
        three states: ALLOCATED, NOT_ALLOCATED, NA (not assigned).

    """
    status = Enum("status", "ALLOCATED NOT_ALLOCATED NA")

    def __init__(self, network: Network = None):
        """
        Init method of class Controller.

        Args:
            network (:obj: Network, optional): Network object with all the information about the network, 
            nodes, routes, path length and slots.

        """
        self.__network = network
        self.__allocator = None
        self.__path = None
        self.__connections = list()
        self.__allocationStatus = None

    @property
    def network(self):
        """
        Get or set the attribute network. 
        """
        return self.__network

    @network.setter
    def network(self, network):
        if type(network) == Network:
            self.__network = network
        else:
            raise AttributeError("You must pass a Network object")

    @property
    def allocator(self):
        """
        Get or set the attribute allocator. 
        """
        return self.__allocator

    @allocator.setter
    def allocator(self, allocator):
        self.__allocator = allocator

    def assignConnection(self, src, dst, bit_rate, id_connection):
        """
        Assigns a connection between a source and a destination node through
        an allocation method from the Allocator. It creates a connection object
        with idConnection as its id, upon which the connections between nodes are
        generated.

        Args:
            src (int): The source node of the connection

            dst (int): The destination node of the connection

            bit_rate (BitRate): BitRate object of the connection

            id_connection (int): The id of the new connection object. It serves to
            identify the connection within the attribute connections.

        Returns:
            The result of the allocation process, whether the
            allocation was succesful or not. This is type allocationStatus, there are
            three states: ALLOCATED, NOT_ALLOCATED, NA (not assigned).

        """

        connection = Connection(id_connection)
        self.__allocationStatus, connection = self.__allocator(
            src, dst, bit_rate, connection, self.__network, self.__path)
        if self.__allocationStatus == Controller.status.ALLOCATED:
            self.__connections.append(connection)
            for i in range(0, len(connection.links)):
                for j in range(0, len(connection.slots[i])):
                    self.__network.use_slot(
                        connection.links[i], slot_pos=connection.slots[i][j])

        return self.__allocationStatus

    def unassignConnection(self, id_connection):
        """
        Unnasigns the requested connection making the resources that were
        being used become available again. It deactivates the slots that were
        taken in the connection.

        Args:
            id_connection (int): The id of the new connection object. It serves to
            identify the connection within the attribute connections.

        Returns:
            Number zero if unsuccessful.

        """

        for i in range(0, len(self.__connections)):
            if self.__connections[i].id == id_connection:
                for j in range(0, len(self.__connections[i].links)):
                    for k in range(0, len(self.__connections[i].slots[j])):
                        self.__network.unuse_slot(
                            self.__connections[i].links[j], slot_pos=self.__connections[i].slots[j][k])
                self.__connections.pop(i)
                break
        return 0

    # the file is within a folder called json
    def set_paths(self, file_name):
        """
        Sets the path attribute from the routes on a JSON file. From this
        file, the method creates the paths attribute based on an lists of routes. This
        lists contains the source and destination nodes, as well as an list with all
        the existing paths between them. The path attribute is important because it is
        all the nodes and the respective routes that link them.

        In the example below, the network consists of three nodes: 0, 1 and 2. Node
        0 is connected to node 1 directly and through node 2, to which it's directly
        connected as well. Node 2 is connected directly to node one. All the
        connections are unidirectional.

        Args:
            file_name (str): Name of the JSON file that contains the routes. Example of
            this: "routes.json"

        Example:
            code-block:: JSON
            {
                "name": "Example routes between 3 nodes",
                "alias": "example",
                "routes": [
                    {
                    "src": 0,
                    "dst": 1,
                    "paths": [
                        [
                        0,
                        1
                        ],
                        [
                        0,
                        2,
                        1
                        ]
                    ]
                    },
                    {
                    "src": 0,
                    "dst": 2,
                    "paths": [
                        [
                        0,
                        2
                        ]
                    ]
                    },
                    {
                    "src": 2,
                    "dst": 1,
                    "paths": [
                        [
                        2,
                        1
                        ]
                    ]
                    }
                ]
            };

        """

        self.__path = []

        f = open(file_name)
        data = json.load(f)

        numberOfNodes = self.__network.node_counter

        # set list for paths
        for i in range(numberOfNodes):
            self.__path.append([])
            for t in range(numberOfNodes):
                self.__path[i].append([])

        routesNumber = len(data["routes"])

        for i in range(routesNumber):
            pathsNumber = len(data["routes"][i]["paths"])
            src = data["routes"][i]["src"]
            dst = data["routes"][i]["dst"]

            for m in range(pathsNumber):
                self.__path[src][dst].append([])

            for b in range(pathsNumber):
                nodesPathNumber = len(data["routes"][i]["paths"][b])
                lastNode = nodesPathNumber - 1
                for c in range(lastNode):
                    actNode = data["routes"][i]["paths"][b][c]
                    nextNode = data["routes"][i]["paths"][b][c + 1]
                    idLink = self.__network.is_connected(actNode, nextNode)
                    self.__path[src][dst][b].append(idLink)
