cdef class ClassificationPerformance(Performance):

    def __init__(self,
                 accuracy: float,
                 errorRate: float = -1):
        """
        A constructor that sets the accuracy and errorRate via given input.

        PARAMETERS
        ----------
        accuracy : float
            Double value input.
        errorRate : float
            Double value input.
        """
        if errorRate == -1:
            self.error_rate = 1 - accuracy
        else:
            self.error_rate = errorRate
        self.__accuracy = accuracy

    cpdef double getAccuracy(self):
        """
        Accessor for the accuracy.

        RETURNS
        -------
        float
            Accuracy value.
        """
        return self.__accuracy
