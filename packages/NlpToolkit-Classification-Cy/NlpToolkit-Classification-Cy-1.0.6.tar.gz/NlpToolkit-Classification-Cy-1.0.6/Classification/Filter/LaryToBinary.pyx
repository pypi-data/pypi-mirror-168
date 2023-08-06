from Classification.Attribute.AttributeType import AttributeType
from Classification.Attribute.BinaryAttribute cimport BinaryAttribute
from Classification.DataSet.DataSet cimport DataSet
from Classification.DataSet.DataDefinition cimport DataDefinition
from Classification.Filter.LaryFilter cimport LaryFilter
from Classification.Instance.Instance cimport Instance


cdef class LaryToBinary(LaryFilter):

    def __init__(self, dataSet: DataSet):
        """
        Constructor for L-ary discrete to binary discrete filter.

        PARAMETERS
        ----------
        dataSet : DataSet
            The instances whose L-ary discrete attributes will be converted to binary discrete attributes.
        """
        super().__init__(dataSet)

    cpdef convertInstance(self, Instance instance):
        """
        Converts discrete attributes of a single instance to binary discrete version using 1-of-L encoding. For example,
        if an attribute has values red, green, blue; this attribute will be converted to 3 binary attributes where
        red will have the value true false false, green will have the value false true false, and blue will have the
        value false false true.

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
                        instance.addAttribute(BinaryAttribute(False))
                    else:
                        instance.addAttribute(BinaryAttribute(True))
        self.removeDiscreteAttributesFromInstance(instance, size)

    cpdef convertDataDefinition(self):
        """
        Converts the data definition with L-ary discrete attributes, to data definition with binary discrete attributes.
        """
        cdef DataDefinition dataDefinition
        cdef int size, i, j
        dataDefinition = self.dataSet.getDataDefinition()
        size = dataDefinition.attributeCount()
        for i in range(size):
            if len(self.attribute_distributions[i]):
                for j in range(len(self.attribute_distributions[i])):
                    dataDefinition.addAttribute(AttributeType.BINARY)
        self.removeDiscreteAttributesFromDataDefinition(size)
