cdef class Attribute(object):

    cpdef int continuousAttributeSize(self)
    cpdef list continuousAttributes(self)
    cpdef object getValue(self)
