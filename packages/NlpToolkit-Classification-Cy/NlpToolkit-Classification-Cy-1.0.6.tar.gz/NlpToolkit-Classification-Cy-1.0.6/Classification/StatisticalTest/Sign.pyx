from Classification.StatisticalTest.PairedTest cimport PairedTest
from Classification.Performance.ExperimentPerformance cimport ExperimentPerformance
from Classification.StatisticalTest.StatisticalTestNotApplicable import StatisticalTestNotApplicable
from Classification.StatisticalTest.StatisticalTestResult cimport StatisticalTestResult
import math


cdef class Sign(PairedTest):

    cpdef int __binomial(self,
                         int m,
                         int n):
        if n == 0 or m == n:
            return 1
        else:
            return math.factorial(m) // (math.factorial(n) * math.factorial(m - n))

    cpdef StatisticalTestResult compare(self,
                                        ExperimentPerformance classifier1,
                                        ExperimentPerformance classifier2):
        cdef int plus, minus, i, total
        cdef double p_value
        if classifier1.numberOfExperiments() != classifier2.numberOfExperiments():
            raise StatisticalTestNotApplicable("In order to apply a paired test, you need to have the same number of "
                                               "experiments in both algorithms.")
        plus = 0
        minus = 0
        for i in range(classifier1.numberOfExperiments()):
            if classifier1.getErrorRate(i) < classifier2.getErrorRate(i):
                plus = plus + 1
            else:
                if classifier1.getErrorRate(i) > classifier2.getErrorRate(i):
                    minus = minus + 1
        total = plus + minus
        p_value = 0
        if total == 0:
            raise StatisticalTestNotApplicable("Variance is 0.")
        for i in range(plus + 1):
            p_value += self.__binomial(total, i) / math.pow(2, total)
        return StatisticalTestResult(p_value, False)
