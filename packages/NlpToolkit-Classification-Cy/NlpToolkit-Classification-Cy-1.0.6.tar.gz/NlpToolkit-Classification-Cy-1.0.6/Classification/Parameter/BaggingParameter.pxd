from Classification.Parameter.Parameter cimport Parameter


cdef class BaggingParameter(Parameter):

    cdef int ensemble_size

    cpdef int getEnsembleSize(self)
