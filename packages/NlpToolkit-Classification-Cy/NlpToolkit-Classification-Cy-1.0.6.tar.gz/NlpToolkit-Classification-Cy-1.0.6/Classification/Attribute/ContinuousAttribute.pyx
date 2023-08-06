cdef class ContinuousAttribute(Attribute):

    def __init__(self, value: float):
        """
        Constructor for a continuous attribute.

        PARAMETERS
        ----------
        value : str
            Value of the attribute.
        """
        self.__value = value

    cpdef object getValue(self):
        """
        Accessor method for value.

        RETURNS
        -------
        float
            value
        """
        return self.__value

    cpdef setValue(self, double value):
        """
        Mutator method for value

        PARAMETERS
        ----------
        value : float
            New value of value.
        """
        self.__value = value

    def __str__(self) -> str:
        """
        Converts value to {@link String}.

        RETURNS
        -------
        str
            String representation of value.
        """
        return self.__value.__str__()

    cpdef int continuousAttributeSize(self):
        return 1

    cpdef list continuousAttributes(self):
        cdef list result
        result = [self.__value]
        return result
