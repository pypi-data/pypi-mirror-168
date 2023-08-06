from Classification.Filter.FeatureFilter cimport FeatureFilter


cdef class TrainedFeatureFilter(FeatureFilter):

    cpdef train(self)
