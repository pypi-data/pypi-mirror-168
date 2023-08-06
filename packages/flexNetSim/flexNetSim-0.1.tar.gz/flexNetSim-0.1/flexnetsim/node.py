class Node:
    """
    The Node class is used to represent a Node in an Optical Fiber Network inside the simulator.

    Args:
        id (int): The desired Id number used to identify the Node. By default -1.

        label (str): The desired Label used to add extra information to the node.

    """

    def __init__(self, id=-1, label=None):

        self.__id = id
        self.__label = label

    @property
    def id(self):
        """
        Returns the id of the node.

        Args:
            id (int): identificator number of the node.
        """
        return self.__id

    @id.setter
    def id(self, id):
        if self.id != -1:
            raise ValueError(
                "Cannot set Id to a Node with Id different than -1.")
        self.__id = id

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, label):
        self.__label = label
