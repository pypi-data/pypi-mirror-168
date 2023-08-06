from Classification.InstanceList.InstanceList cimport InstanceList


cdef class InstanceListOfSameClass(InstanceList):

    cdef str __classLabel

    cpdef str getClassLabel(self)
