from Classification.StatisticalTest.PairedTest cimport PairedTest
from Classification.Performance.ExperimentPerformance cimport ExperimentPerformance
from Classification.StatisticalTest.StatisticalTestNotApplicable import StatisticalTestNotApplicable
from Classification.StatisticalTest.StatisticalTestResult cimport StatisticalTestResult
from Math.Distribution cimport Distribution
import math


cdef class Paired5x2t(PairedTest):

    cpdef __testStatistic(self, ExperimentPerformance classifier1, ExperimentPerformance classifier2):
        cdef list difference
        cdef int i
        cdef double denominator, mean, variance
        if classifier1.numberOfExperiments() != classifier2.numberOfExperiments():
            raise StatisticalTestNotApplicable("In order to apply a paired test, you need to have the same number of "
                                               "experiments in both algorithms.")
        if classifier1.numberOfExperiments() != 10:
            raise StatisticalTestNotApplicable("In order to apply a 5x2 test, you need to have 10 experiments.")
        difference = []
        for i in range(classifier1.numberOfExperiments()):
            difference.append(classifier1.getErrorRate(i) - classifier2.getErrorRate(i))
        denominator = 0
        for i in range(classifier1.numberOfExperiments() // 2):
            mean = (difference[2 * i] + difference[2 * i + 1]) / 2
            variance = (difference[2 * i] - mean) * (difference[2 * i] - mean) + (difference[2 * i + 1] - mean) \
                       * (difference[2 * i + 1] - mean)
            denominator += variance
        denominator = math.sqrt(denominator / 5)
        if denominator == 0:
            raise StatisticalTestNotApplicable("Variance is 0.")
        return difference[0] / denominator

    cpdef StatisticalTestResult compare(self,
                                        ExperimentPerformance classifier1,
                                        ExperimentPerformance classifier2):
        cdef double statistic
        cdef int degree_of_freedom
        statistic = self.__testStatistic(classifier1, classifier2)
        degree_of_freedom = classifier1.numberOfExperiments() // 2
        return StatisticalTestResult(Distribution.tDistribution(statistic, degree_of_freedom), False)
