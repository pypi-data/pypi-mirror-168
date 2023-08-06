cdef class InstanceListOfSameClass(InstanceList):

    def __init__(self, classLabel: str):
        """
        Constructor for creating a new instance list with the same class labels.

        PARAMETERS
        ----------
        classLabel : str
            Class labels of instance list.
        """
        super().__init__()
        self.__classLabel = classLabel

    cpdef str getClassLabel(self):
        """
        Accessor for the class label.

        RETURNS
        -------
        str
            Class label.
        """
        return self.__classLabel
