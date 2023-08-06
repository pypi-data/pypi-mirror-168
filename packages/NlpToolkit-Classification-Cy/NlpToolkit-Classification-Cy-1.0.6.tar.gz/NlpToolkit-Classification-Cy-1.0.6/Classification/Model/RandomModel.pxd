from Classification.Instance.Instance cimport Instance
from Classification.Model.Model cimport Model


cdef class RandomModel(Model):

    cdef list __class_labels

    cpdef str predict(self, Instance instance)
    cpdef dict predictProbability(self, Instance instance)
