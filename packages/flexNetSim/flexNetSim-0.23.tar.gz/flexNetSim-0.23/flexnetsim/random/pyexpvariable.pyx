#distutils: language = c++
#distutils: extra_compile_args = ["-std=c++11"]

from flexnetsim.random.pyexponentialvariable cimport ExpVariable

cdef class pyExpVariable:
    cdef ExpVariable *expptr
    def __cinit__(self,unsigned int seed, double parameter1):
        if type(self) is pyExpVariable:
            self.expptr = new ExpVariable(seed, parameter1)
    def getNextValue(self):
        return self.expptr.getNextValue()