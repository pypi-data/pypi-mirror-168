from Classification.Attribute.ContinuousAttribute cimport ContinuousAttribute
from Classification.Attribute.DiscreteAttribute cimport DiscreteAttribute
from Classification.Attribute.DiscreteIndexedAttribute cimport DiscreteIndexedAttribute


cdef class DecisionCondition(object):

    def __init__(self,
                 attributeIndex: int,
                 value: Attribute,
                 comparison="="):
        """
        A constructor that sets attributeIndex and Attribute value. It also assigns equal sign to the comparison
        character.

        PARAMETERS
        ----------
        attributeIndex : int
            Integer number that shows attribute index.
        value : Attribute
            The value of the Attribute.
        """
        self.__attribute_index = attributeIndex
        self.__comparison = comparison
        self.__value = value

    cpdef satisfy(self, Instance instance):
        """
        The satisfy method takes an Instance as an input.

        If defined Attribute value is a DiscreteIndexedAttribute it compares the index of Attribute of instance at the
        attributeIndex and the index of Attribute value and returns the result.

        If defined Attribute value is a DiscreteAttribute it compares the value of Attribute of instance at the
        attributeIndex and the value of Attribute value and returns the result.

        If defined Attribute value is a ContinuousAttribute it compares the value of Attribute of instance at the
        attributeIndex and the value of Attribute value and returns the result according to the comparison character
        whether it is less than or greater than signs.

        PARAMETERS
        ----------
        instance : Instance
            Instance to compare.

        RETURNS
        -------
        bool
            True if gicen instance satisfies the conditions.
        """
        if isinstance(self.__value, DiscreteIndexedAttribute):
            if self.__value.getIndex() != -1:
                return instance.getAttribute(self.__attribute_index).getIndex() == self.__value.getIndex()
            else:
                return True
        elif isinstance(self.__value, DiscreteAttribute):
            return instance.getAttribute(self.__attribute_index).getValue() == self.__value.getValue()
        elif isinstance(self.__value, ContinuousAttribute):
            if self.__comparison == "<":
                return instance.getAttribute(self.__attribute_index).getValue() <= self.__value.getValue()
            else:
                return instance.getAttribute(self.__attribute_index).getValue() > self.__value.getValue()
        return False
