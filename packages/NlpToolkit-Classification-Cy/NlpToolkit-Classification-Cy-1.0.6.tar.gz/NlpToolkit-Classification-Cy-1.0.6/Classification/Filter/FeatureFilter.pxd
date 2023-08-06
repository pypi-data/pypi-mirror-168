from Classification.Instance.Instance cimport Instance
from Classification.DataSet.DataSet cimport DataSet


cdef class FeatureFilter(object):

    cdef DataSet dataSet

    cpdef convertInstance(self, Instance instance)
    cpdef convertDataDefinition(self)
    cpdef convert(self)
