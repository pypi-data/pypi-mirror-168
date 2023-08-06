import numpy as np


class Link():
    """
    The Link class is used to represent a Link between two Nodes in an Optical Fiber Network inside the simulator.

    Args:
        id (int): The desired Id number used to identify the Link. By default -1.

        length (float): The desired length (assumed in meters [m]) of the Link.

        slots (int): The desired amount of slots availabel for connection allocations for the Link to have.
    """

    def __init__(self, id=-1, length=100.0, slots=320):
        self.__id = id

        if length <= 0:
            raise ValueError("Cannot create a link with non-positive length.")
        else:
            self.__length = length

        if slots < 1:
            raise ValueError("Cannot create a link with ", slots, " slots.")
        else:
            self.__slots = np.zeros(slots, dtype=bool)

        self.__src = -1
        self.__dst = -1

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        if self.__id != -1:
            raise ValueError(
                "Cannot set Id to a Link with Id different than -1.")
        else:
            self.__id = id

    @property
    def length(self):
        return self.__length

    @length.setter
    def length(self, length):
        if (length <= 0):
            raise ValueError("Cannot set a link with non-positive length.")
        self.__length = length

    @property
    def slots(self):
        return self.__slots

    @property
    def src(self):
        return self.__src

    @src.setter
    def src(self, src):
        self.__src = src

    @property
    def dst(self):
        return self.__dst

    @dst.setter
    def dst(self, dst):
        self.__dst = dst

    def slots_number(self):
        return len(self.__slots)

    def set_slots(self, slots: int):
        if (slots < 1):
            raise ValueError("Cannot set a link with ", slots, " slots.")

        if (np.any(self.__slots)):
            raise ValueError(
                "Cannot change slots number if at least one slot is active.")

        np.resize(self.__slots, slots)

    def get_slot(self, pos: int):
        if (pos < 0) or (pos >= self.slots_number()):
            raise ValueError("Cannot get slot in position out of bounds.")
        return self.__slots[pos]

    def set_slot(self, pos: int, value: bool):
        if (pos < 0 or pos >= self.slots_number()):
            raise ValueError("Cannot set slot in position out of bounds.")

        if(self.get_slot(pos) == value):
            raise ValueError("Slot already setted in desired state.")

        self.__slots[pos] = value
