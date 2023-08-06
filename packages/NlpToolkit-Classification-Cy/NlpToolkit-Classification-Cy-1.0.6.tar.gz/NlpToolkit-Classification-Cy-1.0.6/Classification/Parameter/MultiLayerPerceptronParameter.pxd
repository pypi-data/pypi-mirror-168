from Classification.Parameter.LinearPerceptronParameter cimport LinearPerceptronParameter


cdef class MultiLayerPerceptronParameter(LinearPerceptronParameter):

    cdef int __hidden_nodes
    cdef object __activation_function

    cpdef int getHiddenNodes(self)
    cpdef object getActivationFunction(self)
