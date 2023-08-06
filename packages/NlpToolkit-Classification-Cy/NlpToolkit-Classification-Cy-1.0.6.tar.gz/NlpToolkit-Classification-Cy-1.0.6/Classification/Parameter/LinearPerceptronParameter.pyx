cdef class LinearPerceptronParameter(Parameter):

    def __init__(self,
                 seed: int,
                 learningRate: float,
                 etaDecrease: float,
                 crossValidationRatio: float,
                 epoch: int):
        """
        Parameters of the linear perceptron algorithm.

        PARAMETERS
        ----------
        seed : int
            Seed is used for random number generation.
        learningRate : float
            Double value for learning rate of the algorithm.
        etaDecrease : float
            Double value for decrease in eta of the algorithm.
        crossValidationRatio : float
            Double value for cross validation ratio of the algorithm.
        epoch : int
            Integer value for epoch number of the algorithm.
        """
        super().__init__(seed)
        self.learning_rate = learningRate
        self.eta_decrease = etaDecrease
        self.cross_validation_ratio = crossValidationRatio
        self.__epoch = epoch

    cpdef double getLearningRate(self):
        """
        Accessor for the learningRate.

        RETURNS
        -------
        float
            The learningRate.
        """
        return self.learning_rate

    cpdef double getEtaDecrease(self):
        """
        Accessor for the etaDecrease.

        RETURNS
        -------
        float
            The etaDecrease.
        """
        return self.eta_decrease

    cpdef double getCrossValidationRatio(self):
        """
        Accessor for the crossValidationRatio.

        RETURNS
        ----------
        float
            The crossValidationRatio.
        """
        return self.cross_validation_ratio

    cpdef int getEpoch(self):
        """
        Accessor for the epoch.

        RETURNS
        -------
        int
            The epoch.
        """
        return self.__epoch
