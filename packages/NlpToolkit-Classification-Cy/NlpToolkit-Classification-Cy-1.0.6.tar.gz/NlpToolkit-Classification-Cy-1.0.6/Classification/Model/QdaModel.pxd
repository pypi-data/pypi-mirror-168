from Classification.Instance.Instance cimport Instance
from Classification.Model.GaussianModel cimport GaussianModel


cdef class QdaModel(GaussianModel):

    cdef dict __W, w, w0

    cpdef double calculateMetric(self, Instance instance, str Ci)
