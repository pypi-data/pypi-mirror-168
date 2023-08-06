from Classification.Parameter.LinearPerceptronParameter cimport LinearPerceptronParameter


cdef class DeepNetworkParameter(LinearPerceptronParameter):

    cdef list __hiddenLayers
    cdef object __activationFunction

    cpdef int layerSize(self)
    cpdef int getHiddenNodes(self, int layerIndex)
    cpdef object getActivationFunction(self)
