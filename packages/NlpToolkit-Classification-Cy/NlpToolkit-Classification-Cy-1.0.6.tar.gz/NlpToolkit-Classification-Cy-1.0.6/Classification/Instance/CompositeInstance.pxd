from Classification.Instance.Instance cimport Instance


cdef class CompositeInstance(Instance):

    cdef list __possible_class_labels

    cpdef list getPossibleClassLabels(self)
    cpdef setPossibleClassLabels(self, list possibleClassLabels)
