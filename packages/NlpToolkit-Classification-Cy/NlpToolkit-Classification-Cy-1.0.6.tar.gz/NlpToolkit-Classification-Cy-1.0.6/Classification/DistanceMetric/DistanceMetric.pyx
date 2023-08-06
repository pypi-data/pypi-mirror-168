from Classification.Instance.Instance cimport Instance


cdef class DistanceMetric(object):

    cpdef double distance(self,
                          Instance instance1,
                          Instance instance2):
        pass
