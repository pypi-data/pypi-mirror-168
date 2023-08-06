from Classification.Instance.Instance cimport Instance


cdef class Model(object):

    cpdef str predict(self, Instance instance)
    cpdef dict predictProbability(self, Instance instance)
