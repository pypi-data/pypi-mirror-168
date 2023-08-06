from Classification.DistanceMetric.DistanceMetric cimport DistanceMetric
from Classification.Instance.Instance cimport Instance


cdef class EuclidianDistance(DistanceMetric):

    cpdef double distance(self, Instance instance1, Instance instance2)
