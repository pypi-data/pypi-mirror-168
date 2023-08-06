cdef class MultiLayerPerceptronParameter(LinearPerceptronParameter):

    def __init__(self,
                 seed: int,
                 learningRate: float,
                 etaDecrease: float,
                 crossValidationRatio: float,
                 epoch: int,
                 hiddenNodes: int,
                 activationFunction: object):
        """
        Parameters of the multi layer perceptron algorithm.

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
        hiddenNodes : int
            Integer value for the number of hidden nodes.
        activationFunction : ActivationFunction
            Activation function.
        """
        super().__init__(seed, learningRate, etaDecrease, crossValidationRatio, epoch)
        self.__hidden_nodes = hiddenNodes
        self.__activation_function = activationFunction

    cpdef int getHiddenNodes(self):
        """
        Accessor for the hiddenNodes.

        RETURNS
        -------
        int
            The hiddenNodes.
        """
        return self.__hidden_nodes

    cpdef object getActivationFunction(self):
        """
        Accessor for the activation function.

        RETURNS
        -------
        ActivationFunction
            The activation function.
        """
        return self.__activation_function
