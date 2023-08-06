from Classification.DistanceMetric.DistanceMetric cimport DistanceMetric
from Classification.Instance.Instance cimport Instance
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Model.Model cimport Model


cdef class KnnModel(Model):

    cdef InstanceList __data
    cdef int __k
    cdef DistanceMetric __distance_metric

    cpdef str predict(self, Instance instance)
    cpdef dict predictProbability(self, Instance instance)
    cpdef InstanceList nearestNeighbors(self, Instance instance)
