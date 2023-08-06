class Connection():
    """
    This class contains the information regarding the connections that are made between the nodes on a network during the allocation process.

    Args:
        id (int): the id of the new connection object.
    """

    def __init__(self, id: int = None):
        self.__id = id
        self.__links = []
        self.__slots = []
        if id == None:
            raise AttributeError(
                "You must pass a list of slots, or a from_slot and to slot integers.")

    def __add_link_from_vector(self, id: int, slots: list):
        """
        Adds a new link to the Connection object. The link id is added to the links vector, and the slots to the slots vector.

        Args:
            id (int): the id of the new link added to the connection object.
            slots (list): the vector that contains the position of the slots.
        """
        self.__links.append(id)
        self.__slots.append(slots)

    def __add_link_from_from_to(self, id: int, from_slot: int, to_slot: int):
        """
        Adds a new link to the Connection object. The link id is added to the links vector, and the slots in the range fromSlot-toSlot are added to the slots vector.

        Args:
            id (int): the id of the new link added to the connection object.
            from_slot (int): the position of the first slot to be taken on the link.
            to_slot (int): the position of the last slot to be taken on the link.
        """
        self.__links.append(id)
        self.__slots.append([])
        for i in range(from_slot, to_slot):
            self.__slots[-1].append(i)

    def add_link(self, id: int, *,  slots: list = None, from_slot: int = None, to_slot: int = None):
        """
        Adds a new link to the Connection object. The link id is added to the links vector, and the slotsare added to the slots vector. You must use one of these two options:
        * Use only slots parameter
        * Use only from_slot and to_slot parameters

        Args:
            id (int): the id of the new link added to the connection object.
            slots (list): the vector that contains the position of the slots.
            from_slot (int): the position of the first slot to be taken on the link.
            to_slot (int): the position of the last slot to be taken on the link.
        """
        if from_slot == None and to_slot == None and slots != None:
            self.__add_link_from_vector(id, slots)
        elif from_slot != None and to_slot != None and slots == None:
            self.__add_link_from_from_to(id, from_slot, to_slot)
        else:
            raise AttributeError(
                "You must pass a list of slots, or a from_slot and to slot integers separately.")

    @property
    def links(self):
        """
        A list with the link IDs belonging to this connection.
        """
        return self.__links

    @property
    def slots(self):
        """
        A 2D-list with the slot IDs belonging to this connection. First dimension represents the link, whilst second dimension the slots used.
        """
        return self.__slots

    @property
    def id(self):
        """
        The ID of this connection.
        """
        return self.__id
