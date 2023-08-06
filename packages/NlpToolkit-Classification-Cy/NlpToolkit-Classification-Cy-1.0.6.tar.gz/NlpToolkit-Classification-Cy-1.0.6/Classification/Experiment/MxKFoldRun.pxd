from Classification.Experiment.Experiment cimport Experiment
from Classification.Experiment.KFoldRun cimport KFoldRun
from Classification.Performance.ExperimentPerformance cimport ExperimentPerformance


cdef class MxKFoldRun(KFoldRun):

    cdef int M

    cpdef ExperimentPerformance execute(self, Experiment experiment)