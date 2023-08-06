from Classification.Performance.Performance cimport Performance


cdef class ClassificationPerformance(Performance):

    cdef double __accuracy

    cpdef double getAccuracy(self)
