from Classification.Model.Model cimport Model
from Classification.Instance.Instance cimport Instance
from Math.DiscreteDistribution cimport DiscreteDistribution


cdef class DummyModel(Model):

    cdef DiscreteDistribution distribution

    cpdef str predict(self, Instance instance)
    cpdef dict predictProbability(self, Instance instance)
