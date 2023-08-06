cdef class DiscreteAttribute(Attribute):

    def __init__(self, value: str):
        """
        Constructor for a discrete attribute.

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
        str
            value
        """
        return self.__value

    def __str__(self) -> str:
        """
        Converts value to String.

        RETURNS
        -------
        str
            String representation of value.
        """
        if self.__value == ",":
            return "comma"
        return self.__value

    cpdef int continuousAttributeSize(self):
        return 0

    cpdef list continuousAttributes(self):
        return []
