from typing import DefaultDict
from .bitrate import Bitrate
from .network import Network
from .controller import Controller
from .event import Event
import time
from .random.pyunivariable import pyUniformVariable
from .random.pyexpvariable import pyExpVariable



class Simulator():

    def __init__(self, network_filename: str = None, path_filename: str = None,  bitrate_filename: str = None):

        self.__network_filename = network_filename
        self.__path_filename = path_filename
        self.__bitrate_filename = bitrate_filename

        self.__events = []
        self.__controller = Controller()
        self.__current_event = None
        # vector
        self.__bit_rates = []

        self.__initReady = None
        self.__lambdaS = None
        self.__mu = None
        self.__seedArrive = None
        self.__seedDeparture = None
        self.__seedSrc = None
        self.__seedDst = None
        self.__seedBitRate = None
        self.__numberOfConnections = None
        self.__numberOfEvents = None
        self.__goalConnections = None
        self.__nextEventTime = None
        self.__arrival_variable = None
        self.__departure_variable = None
        self.__source_variable = None
        self.__destination_variable = None
        self.__bitrate_variable = None
        self.__rtn_allocation = None

        self.__src = None
        self.__dst = None
        # int
        self.__bitRate = None

        # vector
        self.__bitRatesDefault = []
        self.__allocatedConnections = None
        self.__columnWidth = None
        # time
        self.__clock = None
        self.__starting_time = None
        self.__check_time = None
        self.__time_duration = None

        self.default_values()

        if(network_filename == None and path_filename == None and bitrate_filename == None):
            self.default_bit_rates()
            self.__allocatedConnections = 0

        elif(network_filename != None and path_filename != None):

            self.__controller.network = Network(self.__network_filename)
            self.__controller.set_paths(self.__path_filename)

            self.default_bit_rates()

            self.__allocatedConnections = 0

        elif(network_filename != None and path_filename != None and bitrate_filename != None):
            self.__controller.network(Network(self.__network_filename))
            self.__controller.set_paths(self.__path_filename)
            self.__bitRatesDefault = Bitrate().read_bit_rate_file(self.__path_filename)
            self.__allocatedConnections = 0

        else:
            print("You do not have been submitted the parameters correctly")

    def default_values(self):
        self.__initReady = False
        self.__lambdaS = 3
        self.__mu = 10
        self.__seedArrive = 12345
        self.__seedDeparture = 12345
        self.__seedSrc = 12345
        self.__seedDst = 12345
        self.__seedBitRate = 12345
        self.__numberOfConnections = 0
        self.__numberOfEvents = 0
        self.__goalConnections = 10000
        self.__columnWidth = 10

    @property
    def lambdaS(self):
        """
        Get or set the attribute lambda.
        """
        return self.__lambdaS

    @lambdaS.setter
    def lambdaS(self, lambdaS):
        if(self.__initReady):
            print("You can not set mu parameter AFTER calling init simulator "
                  "method.")
            return
        self.__lambdaS = lambdaS

    @property
    def mu(self):
        """
        Get or set the attribute mu.
        """
        return self.__mu

    @mu.setter
    def mu(self, mu):
        if(self.__initReady):
            print("You can not set mu parameter AFTER calling init simulator "
                  "method.")
            return
        self.__mu = mu

    @property
    def seedArrive(self):
        """
        Get or set the attribute seedArrive.
        """
        return self.__seedArrive

    @seedArrive.setter
    def seedArrive(self, seedArrive):
        if(self.__initReady):
            print("You can not set mu parameter AFTER calling init simulator "
                  "method.")
            return
        self.__seedArrive = seedArrive

    @property
    def seedDeparture(self):
        """
        Get or set the attribute seedDeparture.
        """
        return self.__seedDeparture

    @seedDeparture.setter
    def seedDeparture(self, seedDeparture):
        if(self.__initReady):
            print("You can not set mu parameter AFTER calling init simulator "
                  "method.")
            return
        self.__seedDeparture = seedDeparture

    @property
    def seedBitRate(self):
        """
        Get or set the attribute seedBitRate.
        """
        return self.__seedBitRate

    @seedBitRate.setter
    def seedBitRate(self, seedBitRate):
        if(self.__initReady):
            print("You can not set mu parameter AFTER calling init simulator "
                  "method.")
            return
        self.__seedBitRate = seedBitRate

    @property
    def goalConnections(self):
        """
        Get or set the attribute goalConnections.
        """
        return self.__goalConnections

    @goalConnections.setter
    def goalConnections(self, goalConnections):
        if(self.__initReady):
            print("You can not set mu parameter AFTER calling init simulator "
                  "method.")
            return
        self.__goalConnections = goalConnections

    @property
    def bitRates(self):
        """
        Get or set the attribute bitRates.
        """
        return self.__bitRates

    @bitRates.setter
    def bitRates(self, bitRates):
        if(self.__initReady):
            print("You can not set mu parameter AFTER calling init simulator "
                  "method.")
            return
        self.__bitRates = bitRates

    def default_bit_rates(self):
        auxB = Bitrate(10.0)
        auxB.add_modulation("BPSK", 1, 5520)
        self.__bitRatesDefault.append(auxB)

        auxB = Bitrate(40.0)
        auxB.add_modulation("BPSK", 4, 5520)
        self.__bitRatesDefault.append(auxB)

        auxB = Bitrate(100.0)
        auxB.add_modulation("BPSK", 8, 5520)
        self.__bitRatesDefault.append(auxB)

        auxB = Bitrate(400.0)
        auxB.add_modulation("BPSK", 32, 5520)
        self.__bitRatesDefault.append(auxB)

        auxB = Bitrate(1000.0)
        auxB.add_modulation("BPSK", 80, 5520)
        self.__bitRatesDefault.append(auxB)

    def print_initial_info(self):
        print("Nodes:\t %s" % self.__controller.network.node_counter)

        print("Links:\t %s" % self.__controller.network.link_counter)

        print("Goal Connections:\t %s" % self.__goalConnections)

        print("Lambda:\t %s" % self.__lambdaS)

        print("Mu:\t %s" % self.__mu)

        # print("Algorithm:\t %s" % self.__controller.__allocator.__name)

        # Header
        print("="*97)
        print("| \t Progress \t", end='')
        print("| \t Arrives \t", end='')
        print("| \t Blocking \t", end='')
        print("| \t Time(s) \t|")
        print("="*97)

        self.__starting_time = time.time()

    def print_row(self, percentage: int):
        self.__check_time = time.time()
        self.__time_duration = self.__check_time - self.__starting_time
        self.__time_duration = round(self.__time_duration, 2)

        # print("-"*97)
        text = "| \t"
        if(percentage < 100):
            text += str(percentage) + " % \t\t"
        else:
            text += str(percentage) + " % \t"

        text += "| \t"
        text += str(self.__numberOfConnections-1)

        if(len(str(self.__numberOfConnections)) <= 6):
            text += " \t\t"
        else:
            text += " \t"

        blocking = 1 - self.__allocatedConnections / self.__numberOfConnections

        text += "| \t"
        text += "{:.1e}".format(blocking)

        text += " \t"

        # if(len(str(blocking)) < 6):
        #     text += " \t\t"
        # else:
        #     text += " \t"

        text += "| \t"
        text += str(self.__time_duration)

        if(len(str(self.__time_duration)) < 6):
            text += " \t\t"
        else:
            text += " \t"

        text += "|"

        print(text)
        if(percentage == 100):
            print("-"*97)

    def event_routine(self):
        self.__current_event = self.__events[0]
        self.__rtn_allocation = None
        self.__clock = self.__current_event.time
        if self.__current_event.type == Event.event.ARRIVE:
            next_event_time = self.__clock + \
                self.__arrival_variable.getNextValue()
            for pos in range(len(self.__events)-1, -1, -1):
                if self.__events[pos].time < next_event_time:
                    self.__events.insert(pos+1, Event(
                        Event.event.ARRIVE, next_event_time, self.__numberOfConnections))
                    self.__numberOfConnections += 1
                    break

            self.__src = self.__source_variable.getNextIntValue()
            self.__dst = self.__destination_variable.getNextIntValue()
            while self.__dst == self.__src:
                self.__dst = self.__destination_variable.getNextIntValue()
            self.__bitRate = self.__bitrate_variable.getNextIntValue()
            self.__rtn_allocation = self.__controller.assignConnection(
                int(self.__src), int(self.__dst), self.__bitRates[int(self.__bitRate)], self.__current_event.id_connection)
            if self.__rtn_allocation == Controller.status.ALLOCATED:
                next_event_time = self.__clock + \
                    self.__departure_variable.getNextValue()
                for pos in range(len(self.__events)-1, -1, -1):
                    if self.__events[pos].time < next_event_time:
                        self.__events.insert(pos+1, Event(
                            Event.event.DEPARTURE, next_event_time, self.__current_event.id_connection))
                        break
                self.__allocatedConnections += 1
        elif self.__current_event.type == Event.event.DEPARTURE:
            self.__controller.unassignConnection(
                self.__current_event.id_connection)
        self.__events.pop(0)

        return self.__rtn_allocation

    def init(self):
        self.__initReady = True
        self.__clock = 0
        self.__bitRates = self.__bitRatesDefault
        self.__arrival_variable = pyExpVariable(
            self.__seedArrive, self.__lambdaS)
        self.__departure_variable = pyExpVariable(
            self.__seedDeparture, self.__mu)
        self.__source_variable = pyUniformVariable(
            self.__seedSrc, self.__controller.network.node_counter-1)
        self.__destination_variable = pyUniformVariable(
            self.__seedDst, self.__controller.network.node_counter-1)
        self.__bitrate_variable = pyUniformVariable(
            self.__seedBitRate, len(self.__bitRates)-1)
        self.__events.append(Event(
            Event.event.ARRIVE, self.__arrival_variable.getNextValue(), self.__numberOfConnections))
        self.__numberOfConnections += 1
        return

    def run(self):
        timesToShow = 20
        arrivesByCycle = self.goalConnections / timesToShow
        self.print_initial_info()
        i = 1
        while(i <= timesToShow):
            while(self.__numberOfConnections <= i*arrivesByCycle):
                self.event_routine()
            self.print_row((100/timesToShow) * i)
            i += 1

    def time_duration(self):
        return self.__time_duration

    def get_Blocking_Probability(self):
        blocking = round(1 - self.__allocatedConnections /
                         self.__numberOfConnections, 2)
        return blocking

    def set_allocation_algorithm(self, alloc_alg):
        self.__controller.allocator = alloc_alg
