from Classification.Experiment.Experiment cimport Experiment
from Classification.Experiment.KFoldRunSeparateTest cimport KFoldRunSeparateTest
from Classification.Performance.ExperimentPerformance cimport ExperimentPerformance


cdef class StratifiedKFoldRunSeparateTest(KFoldRunSeparateTest):

    cpdef ExperimentPerformance execute(self, Experiment experiment)