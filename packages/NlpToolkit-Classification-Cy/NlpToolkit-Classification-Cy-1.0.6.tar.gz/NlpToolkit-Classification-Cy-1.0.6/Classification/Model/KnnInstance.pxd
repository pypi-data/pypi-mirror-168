from Classification.Instance.Instance cimport Instance


cdef class KnnInstance(object):

    cdef Instance instance
    cdef double distance

    cpdef Instance getInstance(self)
