from Classification.StatisticalTest.StatisticalTestResultType import StatisticalTestResultType


cdef class PairedTest(object):

    cpdef StatisticalTestResult compare(self,
                                        ExperimentPerformance classifier1,
                                        ExperimentPerformance classifier2):
        pass

    cpdef int compareWithAlpha(self,
                               ExperimentPerformance classifier1,
                               ExperimentPerformance classifier2,
                               double alpha):
        cdef StatisticalTestResult test_result1, test_result2
        test_result1 = self.compare(classifier1, classifier2)
        test_result2 = self.compare(classifier2, classifier1)
        test_result_type1 = test_result1.oneTailed(alpha)
        test_result_type2 = test_result2.oneTailed(alpha)
        if test_result_type1 is StatisticalTestResultType.REJECT:
            return 1
        else:
            if test_result_type2 is StatisticalTestResultType.REJECT:
                return -1
            else:
                return 0
