from enum import Enum


class Event:
    """
    The Event class represents the event that happens inside the digital
    transmission system or computer network of the Simulator in terms of
    clients requesting to establish connections (thus needing resources) known as
    an "arrival" or closing the connection thereafter (thus freeing resources)
    known as a "departure".

    Note that, as the Simulator uses Event Based Simulation, this class' 
    implementation is a key-piece for the simulator's execution.

    Attributes:
        type (Event.event type): an event variable which describes the kind of Event taking two possible values: ARRIVE or DEPARTURE.

        id_connection (int): the Id (identifier) of the Connection regarding the current Event.

        time (int): the time at which the current Event has occurred.


    The Event class contains two main methods for setting it's variables' values,
    both being in the constuctor method: the default constructor with default initialized 
    values and another if arguments are given. Each attribute has it's own property gettter.
    """

    event = Enum("event", "ARRIVE DEPARTURE")

    def __init__(self, type=None, time=-1, id_connection=-1):
        """
        Init method of class Event

        Args:
            type (Event.event type): an event variable which describes the kind of Event taking two possible values: ARRIVE or DEPARTURE.

            id_connection (int): the Id (identifier) of the Connection regarding the current Event.

            time (int): the time at which the current Event has occurred.
        """
        self.__time = time
        self.__id_connection = id_connection
        if type == None:
            self.__type = Event.event.ARRIVE
        else:
            self.__type = type

    @property
    def type(self):
        """
        Getter for the type attribute
        """
        return self.__type

    @property
    def time(self):
        """
        Getter for the time attribute
        """
        return self.__time

    @property
    def id_connection(self):
        """
        Getter for the id_connection attribute
        """
        return self.__id_connection
