from Classification.Attribute.Attribute cimport Attribute


cdef class DiscreteAttribute(Attribute):

    cdef str __value

    cpdef object getValue(self)
    cpdef int continuousAttributeSize(self)
    cpdef list continuousAttributes(self)
