from Classification.Attribute.ContinuousAttribute cimport ContinuousAttribute
from Classification.DataSet.DataSet cimport DataSet
from Classification.Filter.FeatureFilter cimport FeatureFilter
from Classification.Instance.Instance cimport Instance


cdef class Normalize(FeatureFilter):

    cdef Instance __average_instance
    cdef Instance __standard_deviation_instance

    def __init__(self, dataSet: DataSet):
        """
        Constructor for normalize feature filter. It calculates and stores the mean (m) and standard deviation (s) of
        the sample.

        PARAMETERS
        ----------
        dataSet : DataSet
            Instances whose continuous attribute values will be normalized.
        """
        super().__init__(dataSet)
        self.__average_instance = dataSet.getInstanceList().average()
        self.__standard_deviation_instance = dataSet.getInstanceList().standardDeviation()

    cpdef convertInstance(self, Instance instance):
        """
        Normalizes the continuous attributes of a single instance. For all i, new x_i = (x_i - m_i) / s_i.

        PARAMETERS
        ----------
        instance : Instance
            Instance whose attributes will be normalized.
        """
        cdef int i
        cdef ContinuousAttribute xi, mi, si
        for i in range(instance.attributeSize()):
            if isinstance(instance.getAttribute(i), ContinuousAttribute):
                xi = instance.getAttribute(i)
                mi = self.__average_instance.getAttribute(i)
                si = self.__standard_deviation_instance.getAttribute(i)
                if isinstance(xi, ContinuousAttribute):
                    xi.setValue((xi.getValue() - mi.getValue()) / si.getValue())

    cpdef convertDataDefinition(self):
        pass
