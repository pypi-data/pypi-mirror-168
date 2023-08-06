cdef class FeatureSubSet(object):

    cdef list __indexList

    cpdef int size(self)
    cpdef int get(self, int index)
    cpdef bint contains(self, int featureNo)
    cpdef add(self, int featureNo)
    cpdef remove(self, int index)
