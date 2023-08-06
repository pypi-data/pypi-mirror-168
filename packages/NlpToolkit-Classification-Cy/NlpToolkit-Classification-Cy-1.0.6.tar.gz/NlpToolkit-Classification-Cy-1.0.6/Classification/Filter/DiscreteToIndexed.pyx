from Classification.Attribute.DiscreteIndexedAttribute cimport DiscreteIndexedAttribute
from Classification.DataSet.DataSet cimport DataSet
from Classification.Filter.LaryFilter cimport LaryFilter
from Classification.Instance.Instance cimport Instance


cdef class DiscreteToIndexed(LaryFilter):

    def __init__(self, dataSet: DataSet):
        """
        Constructor for discrete to indexed filter.

        PARAMETERS
        ----------
        dataSet : DataSet
            The dataSet whose instances whose discrete attributes will be converted to indexed attributes
        """
        super().__init__(dataSet)

    cpdef convertInstance(self, Instance instance):
        """
        Converts discrete attributes of a single instance to indexed version.

        PARAMETERS
        ----------
        instance : Instance
            The instance to be converted.
        """
        cdef int size, i, index
        size = instance.attributeSize()
        for i in range(size):
            if len(self.attribute_distributions[i]) > 0:
                index = self.attribute_distributions[i].getIndex(instance.getAttribute(i).__str__())
                instance.addAttribute(DiscreteIndexedAttribute(instance.getAttribute(i).__str__(), index,
                                                               len(self.attribute_distributions[i])))
        self.removeDiscreteAttributesFromInstance(instance, size)
