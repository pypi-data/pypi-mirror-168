cdef extern from "uniform_variable.cpp":
    pass

cdef extern from "uniform_variable.hpp":
    cdef cppclass UniformVariable:
        UniformVariable() except +
        UniformVariable(unsigned int seed, double parameter1) except +
        double getNextValue()
        double getNextIntValue()
