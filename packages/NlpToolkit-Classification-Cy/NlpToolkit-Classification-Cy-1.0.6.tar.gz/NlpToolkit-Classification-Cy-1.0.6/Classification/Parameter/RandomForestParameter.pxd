from Classification.Parameter.BaggingParameter cimport BaggingParameter


cdef class RandomForestParameter(BaggingParameter):

    cdef int __attribute_subset_size

    cpdef int getAttributeSubsetSize(self)
