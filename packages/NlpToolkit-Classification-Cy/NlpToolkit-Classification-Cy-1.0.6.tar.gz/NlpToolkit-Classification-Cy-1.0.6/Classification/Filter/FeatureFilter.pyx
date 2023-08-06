from Classification.DataSet.DataSet cimport DataSet


cdef class FeatureFilter(object):

    cpdef convertInstance(self, Instance instance):
        pass

    cpdef convertDataDefinition(self):
        pass

    def __init__(self, dataSet: DataSet):
        """
        Constructor that sets the dataSet.

        PARAMETERS
        ----------
        dataSet : DataSet
            DataSet that will be used.
        """
        self.dataSet = dataSet

    cpdef convert(self):
        """
        Feature converter for a list of instances. Using the abstract method convertInstance, each instance in the
        instance list will be converted.
        """
        cdef list instances
        cdef Instance instance
        instances = self.dataSet.getInstances()
        for instance in instances:
            self.convertInstance(instance)
        self.convertDataDefinition()
