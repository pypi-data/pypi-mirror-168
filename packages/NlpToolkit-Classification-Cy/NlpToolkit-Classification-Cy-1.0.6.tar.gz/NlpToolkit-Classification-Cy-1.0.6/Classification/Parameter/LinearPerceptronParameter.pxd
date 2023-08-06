from Classification.Parameter.Parameter cimport Parameter


cdef class LinearPerceptronParameter(Parameter):

    cdef double learning_rate
    cdef double eta_decrease
    cdef double cross_validation_ratio
    cdef int __epoch

    cpdef double getLearningRate(self)
    cpdef double getEtaDecrease(self)
    cpdef double getCrossValidationRatio(self)
    cpdef int getEpoch(self)
