cdef extern from "exp_variable.cpp":
    pass

cdef extern from "exp_variable.hpp":
    cdef cppclass ExpVariable:
        ExpVariable()
        ExpVariable(unsigned int seed, double parameter1) except +
        double getNextValue()
