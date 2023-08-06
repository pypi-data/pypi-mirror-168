cdef class FeatureSubSet(object):

    def __init__(self, indexList=None):
        """
        A constructor that sets the indexList {@link ArrayList}.

        PARAMETERS
        ----------
        indexList
            An ArrayList consists of integer indices.
        """
        if indexList is None:
            self.__indexList = []
        else:
            if isinstance(indexList, list):
                self.__indexList = indexList
            elif isinstance(indexList, int):
                self.__indexList = [i for i in range(indexList)]

    cpdef int size(self):
        """
        The size method returns the size of the indexList.

        RETURNS
        -------
        int
            The size of the indexList.
        """
        return len(self.__indexList)

    cpdef int get(self, int index):
        """
        The get method returns the item of indexList at given index.

        PARAMETERS
        ----------
        index : int
            Index of the indexList to be accessed.

        RETURNS
        -------
        int
            The item of indexList at given index.
        """
        return self.__indexList[index]

    cpdef bint contains(self, int featureNo):
        """
        The contains method returns True, if indexList contains given input number and False otherwise.

        PARAMETERS
        ----------
        featureNo : int
            Feature number that will be checked.

        RETURNS
        -------
        bool
            True, if indexList contains given input number.
        """
        return featureNo in self.__indexList

    cpdef add(self, int featureNo):
        """
        The add method adds given Integer to the indexList.

        PARAMETERS
        ----------
        featureNo : int
            Integer that will be added to indexList.
        """
        self.__indexList.append(featureNo)

    cpdef remove(self, int index):
        """
        The remove method removes the item of indexList at the given index.

        PARAMETERS
        ----------
        index : int
            Index of the item that will be removed.
        """
        self.__indexList.pop(index)
