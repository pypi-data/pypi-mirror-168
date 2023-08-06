from Classification.Attribute.Attribute cimport Attribute


cdef class ContinuousAttribute(Attribute):

    cdef double __value

    cpdef object getValue(self)
    cpdef setValue(self, double value)
    cpdef int continuousAttributeSize(self)
    cpdef list continuousAttributes(self)
