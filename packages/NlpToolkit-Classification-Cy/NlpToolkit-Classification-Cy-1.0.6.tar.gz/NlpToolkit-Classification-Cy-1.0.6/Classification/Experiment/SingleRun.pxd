from Classification.Experiment.Experiment cimport Experiment
from Classification.Performance.Performance cimport Performance


cdef class SingleRun(object):

    cpdef Performance execute(self, Experiment experiment)
