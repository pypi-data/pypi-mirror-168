from Classification.Attribute.Attribute cimport Attribute
from Classification.Instance.Instance cimport Instance


cdef class DecisionCondition(object):

    cdef int __attribute_index
    cdef str __comparison
    cdef Attribute __value

    cpdef satisfy(self, Instance instance)