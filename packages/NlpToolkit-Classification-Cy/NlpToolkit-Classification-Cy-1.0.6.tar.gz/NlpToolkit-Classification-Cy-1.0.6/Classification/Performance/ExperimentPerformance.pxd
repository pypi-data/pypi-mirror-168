from Classification.Performance.Performance cimport Performance
from Classification.Performance.ClassificationPerformance cimport ClassificationPerformance
from Classification.Performance.DetailedClassificationPerformance cimport DetailedClassificationPerformance


cdef class ExperimentPerformance:

    cdef list __results
    cdef bint __contains_details
    cdef bint __classification

    cpdef initWithFile(self, str fileName)
    cpdef add(self, Performance performance)
    cpdef int numberOfExperiments(self)
    cpdef double getErrorRate(self, int index)
    cpdef double getAccuracy(self, int index)
    cpdef Performance meanPerformance(self)
    cpdef ClassificationPerformance meanClassificationPerformance(self)
    cpdef DetailedClassificationPerformance meanDetailedPerformance(self)
    cpdef Performance standardDeviationPerformance(self)
    cpdef ClassificationPerformance standardDeviationClassificationPerformance(self)
    cpdef bint isBetter(self, ExperimentPerformance experimentPerformance)
