from Classification.Attribute.AttributeType import AttributeType
from Classification.Attribute.ContinuousAttribute cimport ContinuousAttribute
from Classification.DataSet.DataSet cimport DataSet
from Classification.DataSet.DataDefinition cimport DataDefinition
from Classification.Filter.LaryFilter cimport LaryFilter
from Classification.Instance.Instance cimport Instance


cdef class DiscreteToContinuous(LaryFilter):

    def __init__(self, dataSet: DataSet):
        """
        Constructor for discrete to continuous filter.

        PARAMETERS
        ----------
        dataSet : DataSet
            The dataSet whose instances whose discrete attributes will be converted to continuous attributes using
            1-of-L encoding.
        """
        super().__init__(dataSet)

    cpdef convertInstance(self, Instance instance):
        """
        Converts discrete attributes of a single instance to continuous version using 1-of-L encoding. For example, if
        an attribute has values red, green, blue; this attribute will be converted to 3 continuous attributes where
        red will have the value 100, green will have the value 010, and blue will have the value 001.

        PARAMETERS
        ----------
        instance : Instance
            The instance to be converted.
        """
        cdef int size, i, index, j
        size = instance.attributeSize()
        for i in range(size):
            if len(self.attribute_distributions[i]) > 0:
                index = self.attribute_distributions[i].getIndex(instance.getAttribute(i).__str__())
                for j in range(len(self.attribute_distributions[i])):
                    if j != index:
                        instance.addAttribute(ContinuousAttribute(0))
                    else:
                        instance.addAttribute(ContinuousAttribute(1))
        self.removeDiscreteAttributesFromInstance(instance, size)

    cpdef convertDataDefinition(self):
        """
        Converts the data definition with discrete attributes, to data definition with continuous attributes. Basically,
        for each discrete attribute with L possible values, L more continuous attributes will be added.
        """
        cdef DataDefinition data_definition
        cdef int size, i, j
        data_definition = self.dataSet.getDataDefinition()
        size = data_definition.attributeCount()
        for i in range(size):
            if len(self.attribute_distributions[i]) > 0:
                for j in range(len(self.attribute_distributions[i])):
                    data_definition.addAttribute(AttributeType.CONTINUOUS)
        self.removeDiscreteAttributesFromDataDefinition(size)
