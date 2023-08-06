from Classification.DistanceMetric.DistanceMetric cimport DistanceMetric
from Classification.Parameter.Parameter cimport Parameter


cdef class KMeansParameter(Parameter):

    cdef DistanceMetric distance_metric

    cpdef DistanceMetric getDistanceMetric(self)

