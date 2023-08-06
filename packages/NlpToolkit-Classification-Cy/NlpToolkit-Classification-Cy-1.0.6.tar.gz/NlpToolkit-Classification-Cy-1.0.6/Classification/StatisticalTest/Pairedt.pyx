from Classification.StatisticalTest.PairedTest cimport PairedTest
from Classification.Performance.ExperimentPerformance cimport ExperimentPerformance
from Classification.StatisticalTest.StatisticalTestNotApplicable import StatisticalTestNotApplicable
from Classification.StatisticalTest.StatisticalTestResult cimport StatisticalTestResult
from Math.Distribution cimport Distribution
import math


cdef class Pairedt(PairedTest):

    cpdef __testStatistic(self,
                          ExperimentPerformance classifier1,
                          ExperimentPerformance classifier2):
        cdef list difference
        cdef int i
        cdef double total, mean, standard_deviation
        if classifier1.numberOfExperiments() != classifier2.numberOfExperiments():
            raise StatisticalTestNotApplicable("In order to apply a paired test, you need to have the same number of "
                                               "experiments in both algorithms.")
        difference = []
        total = 0
        for i in range(classifier1.numberOfExperiments()):
            difference.append(classifier1.getErrorRate(i) - classifier2.getErrorRate(i))
            total += difference[i]
        mean = total / classifier1.numberOfExperiments()
        total = 0
        for i in range(classifier1.numberOfExperiments()):
            total += (difference[i] - mean) * (difference[i] - mean)
        standard_deviation = math.sqrt(total / (classifier1.numberOfExperiments() - 1))
        if standard_deviation == 0:
            raise StatisticalTestNotApplicable("Variance is 0.")
        return math.sqrt(classifier1.numberOfExperiments()) * mean / standard_deviation

    cpdef StatisticalTestResult compare(self,
                                        ExperimentPerformance classifier1,
                                        ExperimentPerformance classifier2):
        cdef double statistic
        cdef int degree_of_freedom
        statistic = self.__testStatistic(classifier1, classifier2)
        degree_of_freedom = classifier1.numberOfExperiments() - 1
        return StatisticalTestResult(Distribution.tDistribution(statistic, degree_of_freedom), False)
