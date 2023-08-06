from Math.DiscreteDistribution cimport DiscreteDistribution
from Classification.Instance.Instance cimport Instance
from Classification.Model.ValidatedModel cimport ValidatedModel


cdef class GaussianModel(ValidatedModel):

    cdef DiscreteDistribution prior_distribution

    cpdef double calculateMetric(self, Instance instance, str Ci)
    cpdef str predict(self, Instance instance)