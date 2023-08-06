from flexnetsim.bitrate import *
import pytest
import os
import math


class TestBitrate:

    def test_constructor(self):
        Bitrate(10)

    def test_get_bit_rate(self):
        b1 = Bitrate(10)
        b2 = Bitrate(40)

        assert math.isclose(10, b1.bit_rate, rel_tol=0.01)
        assert math.isclose(40, b2.bit_rate, rel_tol=0.01)

    def test_get_bit_rate_from_file(self):
        absolute_path = os.path.abspath(__file__)
        current_folder = os.path.dirname(absolute_path)
        current_directory = os.path.dirname(current_folder)
        file = os.path.join(current_directory, 'test', 'bitrate.json')

        bs = Bitrate.read_bit_rate_file(file)

        assert math.isclose(10, bs[0].bit_rate, rel_tol=0.01)
        assert bs[0].get_modulation(0) == "BPSK"
        assert math.isclose(5520, bs[0].get_reach(0), rel_tol=0.01)
        assert bs[0].get_number_of_slots(0) == 1

        with pytest.raises(ValueError):
            bs[0].get_modulation(1)

        assert math.isclose(40, bs[1].bit_rate, rel_tol=0.01)

        assert bs[1].get_modulation(0) == "BPSK"
        assert math.isclose(5520, bs[1].get_reach(0), rel_tol=0.01)
        assert bs[1].get_number_of_slots(0) == 4

        assert bs[1].get_modulation(1) == "QPSK"
        assert math.isclose(5520, bs[1].get_reach(1), rel_tol=0.01)
        assert bs[1].get_number_of_slots(1) == 2

        with pytest.raises(ValueError):
            bs[1].get_modulation(2)

        assert math.isclose(100, bs[2].bit_rate, rel_tol=0.01)

        assert bs[2].get_modulation(0) == "BPSK"
        assert math.isclose(5520, bs[2].get_reach(0), rel_tol=0.01)
        assert bs[2].get_number_of_slots(0) == 8

        with pytest.raises(ValueError):
            bs[2].get_modulation(1)

        assert math.isclose(400, bs[3].bit_rate, rel_tol=0.01)

        assert bs[3].get_modulation(0) == "BPSK"
        assert math.isclose(5520, bs[3].get_reach(0), rel_tol=0.01)
        assert bs[3].get_number_of_slots(0) == 32

        with pytest.raises(ValueError):
            bs[3].get_modulation(1)

        assert math.isclose(1000, bs[4].bit_rate, rel_tol=0.01)

        assert bs[4].get_modulation(0) == "BPSK"
        assert math.isclose(5520, bs[4].get_reach(0), rel_tol=0.01)
        assert bs[4].get_number_of_slots(0) == 80

        with pytest.raises(ValueError):
            bs[4].get_modulation(1)

        file = os.path.join(current_directory, 'test', 'bitrate_bad1.json')
        with pytest.raises(ValueError):
            bs = Bitrate.read_bit_rate_file(file)
        file = os.path.join(current_directory, 'test', 'bitrate_bad2.json')
        with pytest.raises(ValueError):
            bs = Bitrate.read_bit_rate_file(file)
        file = os.path.join(current_directory, 'test', 'bitrate_bad3.json')
        with pytest.raises(ValueError):
            bs = Bitrate.read_bit_rate_file(file)

    def test_getter_errors(self):
        b1 = Bitrate(40)
        b1.add_modulation("BPSK", 4, 5520)

        with pytest.raises(ValueError):
            b1.get_modulation(5) == "QPSK"
        with pytest.raises(ValueError):
            b1.get_number_of_slots(5) == 2
        with pytest.raises(ValueError):
            b1.get_reach(5) == 2720
