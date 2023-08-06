cdef class DiscreteIndexedAttribute(DiscreteAttribute):

    def __init__(self,
                 value: str,
                 index: int,
                 maxIndex: int):
        """
        Constructor for a discrete attribute.

        PARAMETERS
        ----------
        value : str
            Value of the attribute.
        index : int
            Index of the attribute.
        maxIndex : int
            Maximum index of the attribute.
        """
        super().__init__(value)
        self.__index = index
        self.__maxIndex = maxIndex

    cpdef int getIndex(self):
        """
        Accessor method for index.

        RETURNS
        -------
        int
            index.
        """
        return self.__index

    cpdef int getMaxIndex(self):
        """
        Accessor method for maxIndex.

        RETURNS
        -------
        int
            maxIndex.
        """
        return self.__maxIndex

    cpdef int continuousAttributeSize(self):
        return self.__maxIndex

    cpdef list continuousAttributes(self):
        cdef list result
        cdef int i
        result = []
        for i in range(self.__maxIndex):
            if i != self.__index:
                result.append(0.0)
            else:
                result.append(1.0)
        return result
