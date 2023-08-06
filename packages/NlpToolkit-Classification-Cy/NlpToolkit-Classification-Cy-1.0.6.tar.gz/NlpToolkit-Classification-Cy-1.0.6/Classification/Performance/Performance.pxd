cdef class Performance(object):

    cdef double error_rate

    cpdef double getErrorRate(self)
