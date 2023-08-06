from Classification.DataSet.DataSet cimport DataSet


cdef class TrainedFeatureFilter(FeatureFilter):

    cpdef train(self):
        pass

    def __init__(self, dataSet: DataSet):
        """
        Constructor that sets the dataSet.

        PARAMETERS
        ----------
        dataSet : DataSet
            DataSet that will bu used.
        """
        super().__init__(dataSet)
