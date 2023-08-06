import json


class Bitrate():
    def __init__(self, bit_rate):
        self.__bit_rate = bit_rate
        self.__modulation = []
        self.__slots = []
        self.__reach = []

    @property
    def bit_rate(self):
        return self.__bit_rate

    @property
    def modulation(self):
        return self.__modulation

    @property
    def slots(self):
        return self.__slots

    @property
    def reach(self):
        return self.__reach

    def add_modulation(self, modulation: str, slots: int, reach):
        self.modulation.append(modulation)
        self.slots.append(slots)
        self.reach.append(reach)

    def get_modulation(self, pos: int):
        if pos >= len(self.modulation):
            raise ValueError(
                f"Bitrate {self.bit_rate} does not have more than {len(self.modulation)} modulations")

        return self.modulation[pos]

    def get_number_of_slots(self, pos: int):
        if pos >= len(self.slots):
            raise ValueError(
                f"Bitrate {self.bit_rate} does not have more than {len(self.slots)} modulations")
        return self.slots[pos]

    def get_reach(self, pos: int):
        if pos >= len(self.reach):
            raise ValueError(
                f"Bitrate {self.bit_rate} does not have more than {len(self.reach)} modulations")
        return self.reach[pos]

    def read_bit_rate_file(filename: str):
        f = open(filename)
        bit_rate_file = json.load(f)
        f.close()
        vect = []

        for x in bit_rate_file:
            bit_rate = int(x)
            number_of_modulations = len(bit_rate_file[x])

            aux = Bitrate(bit_rate)
            for i in range(number_of_modulations):
                for j in bit_rate_file[x][i].items():
                    modulation = j[0]
                    reach = int(j[1]["reach"])
                    slots = int(j[1]["slots"])

                if (reach < 0) and (slots < 0):
                    raise ValueError(
                        "Value entered for slots and reach is less than zero")

                if reach < 0:
                    raise ValueError(
                        "Value entered for reach is less than zero")

                if slots < 0:
                    raise ValueError(
                        "Value entered for slots is less than zero")

                aux.add_modulation(modulation, slots, reach)

            vect.append(aux)
        return vect
