cdef class StatisticalTestResult(object):

    cdef double __pValue
    cdef bint __only_two_tailed

    cpdef object oneTailed(self, double alpha)
    cpdef object twoTailed(self, double alpha)
    cpdef double getPValue(self)
