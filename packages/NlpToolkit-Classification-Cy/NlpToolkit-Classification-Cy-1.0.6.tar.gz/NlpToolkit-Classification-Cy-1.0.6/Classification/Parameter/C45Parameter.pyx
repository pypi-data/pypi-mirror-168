from Classification.Parameter.Parameter cimport Parameter


cdef class C45Parameter(Parameter):

    cdef bint __prune
    cdef double __cross_validation_ratio

    def __init__(self,
                 seed: int,
                 prune: bool,
                 crossValidationRatio: float):
        """
        Parameters of the C4.5 univariate decision tree classifier.

        PARAMETERS
        ----------
        seed : int
            Seed is used for random number generation.
        prune : bool
            Boolean value for prune.
        crossValidationRatio : float
            Double value for cross crossValidationRatio ratio.
        """
        super().__init__(seed)
        self.__prune = prune
        self.__cross_validation_ratio = crossValidationRatio

    cpdef bint isPrune(self):
        """
        Accessor for the prune.

        RETURNS
        -------
        bool
            Prune.
        """
        return self.__prune

    cpdef double getCrossValidationRatio(self):
        """
        Accessor for the crossValidationRatio.

        RETURNS
        -------
        float
            crossValidationRatio.
        """
        return self.__cross_validation_ratio
