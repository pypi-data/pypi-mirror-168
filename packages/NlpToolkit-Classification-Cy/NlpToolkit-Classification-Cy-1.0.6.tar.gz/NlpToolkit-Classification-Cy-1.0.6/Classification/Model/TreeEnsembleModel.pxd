from Classification.Model.Model cimport Model
from Classification.Instance.Instance cimport Instance


cdef class TreeEnsembleModel(Model):

    cdef list __forest

    cpdef str predict(self, Instance instance)
    cpdef dict predictProbability(self, Instance instance)
