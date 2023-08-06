from Classification.Filter.FeatureFilter cimport FeatureFilter
from Classification.Instance.Instance cimport Instance


cdef class LaryFilter(FeatureFilter):

    cdef list attribute_distributions

    cpdef removeDiscreteAttributesFromInstance(self, Instance instance, int size)
    cpdef removeDiscreteAttributesFromDataDefinition(self, int size)
