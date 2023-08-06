from Classification.Attribute.DiscreteAttribute cimport DiscreteAttribute


cdef class DiscreteIndexedAttribute(DiscreteAttribute):

    cdef int __index
    cdef int __maxIndex

    cpdef int getIndex(self)
    cpdef int getMaxIndex(self)
    cpdef int continuousAttributeSize(self)
    cpdef list continuousAttributes(self)
