#distutils: language = c++
#distutils: extra_compile_args = ["-std=c++11"]

from flexnetsim.random.pyuniformvariable cimport UniformVariable

cdef class pyUniformVariable:
    cdef UniformVariable *uniptr
    def __cinit__(self,unsigned int seed, double parameter1):
        if type(self) is pyUniformVariable:
            self.uniptr = new UniformVariable(seed, parameter1)
    def getNextValue(self):
        return self.uniptr.getNextValue()
    def getNextIntValue(self):
        return self.uniptr.getNextIntValue()