from Classification.Instance.Instance cimport Instance
from Classification.Model.GaussianModel cimport GaussianModel


cdef class LdaModel(GaussianModel):

    cdef dict w0
    cdef dict w

    cpdef double calculateMetric(self, Instance instance, str Ci)
