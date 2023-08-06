from Classification.Performance.ExperimentPerformance cimport ExperimentPerformance
from Classification.StatisticalTest.StatisticalTestResult cimport StatisticalTestResult


cdef class PairedTest(object):

    cpdef StatisticalTestResult compare(self, ExperimentPerformance classifier1, ExperimentPerformance classifier2)
    cpdef int compareWithAlpha(self, ExperimentPerformance classifier1, ExperimentPerformance classifier2, double alpha)
