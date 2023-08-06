from Classification.Experiment.Experiment cimport Experiment
from Classification.Performance.ExperimentPerformance cimport ExperimentPerformance


cdef class MultipleRun(object):

    cpdef ExperimentPerformance execute(self, Experiment experiment)
