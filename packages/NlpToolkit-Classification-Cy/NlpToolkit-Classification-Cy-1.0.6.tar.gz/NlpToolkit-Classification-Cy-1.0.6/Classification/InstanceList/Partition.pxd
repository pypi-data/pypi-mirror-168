from Classification.InstanceList.InstanceList cimport InstanceList


cdef class Partition(object):

    cdef list __multi_list

    cpdef add(self, InstanceList _list)
    cpdef int size(self)
    cpdef InstanceList get(self, int index)
    cpdef list getLists(self)
