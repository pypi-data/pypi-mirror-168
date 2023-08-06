import copy
from Classification.Parameter.MultiLayerPerceptronParameter cimport MultiLayerPerceptronParameter

from Classification.Parameter.ActivationFunction import ActivationFunction

cdef class AutoEncoderModel(NeuralNetworkModel):

    def __init__(self,
                 trainSet: InstanceList,
                 validationSet: InstanceList,
                 parameters: MultiLayerPerceptronParameter):
        """
        The AutoEncoderModel method takes two InstanceLists as inputs; train set and validation set. First it allocates
        the weights of W and V matrices using given MultiLayerPerceptronParameter and takes the clones of these
        matrices as the bestW and bestV. Then, it gets the epoch and starts to iterate over them. First it shuffles the
        train set and tries to find the new W and V matrices. At the end it tests the autoencoder with given validation
        set and if its performance is better than the previous one, it reassigns the bestW and bestV matrices. Continue
        to iterate with a lower learning rate till the end of an episode.

        PARAMETERS
        ----------
        trainSet : InstanceList
            InstanceList to use as train set.
        validationSet : InstanceList
            InstanceList to use as validation set.
        parameters : MultiLayerPerceptronParameter
            MultiLayerPerceptronParameter is used to get the parameters.
        """
        cdef Matrix best_w, best_v, delta_v, delta_w
        cdef Performance best_performance, current_performance
        cdef int epoch, i, j
        cdef double learning_rate
        cdef Vector hidden, hidden_biased, r_minus_y, one_minus_hidden, tmp_h, tmp_hidden
        super().__init__(trainSet)
        self.K = trainSet.get(0).continuousAttributeSize()
        self.__allocateWeights(parameters.getHiddenNodes(), parameters.getSeed())
        best_w = copy.deepcopy(self.__W)
        best_v = copy.deepcopy(self.__V)
        best_performance = Performance(1000000000)
        epoch = parameters.getEpoch()
        learning_rate = parameters.getLearningRate()
        for i in range(epoch):
            trainSet.shuffle(parameters.getSeed())
            for j in range(trainSet.size()):
                self.createInputVector(trainSet.get(j))
                self.r = trainSet.get(j).toVector()
                hidden = self.calculateHidden(self.x, self.__W, ActivationFunction.SIGMOID)
                hidden_biased = hidden.biased()
                self.y = self.__V.multiplyWithVectorFromRight(hidden_biased)
                r_minus_y = self.r.difference(self.y)
                delta_v = Matrix(r_minus_y, hidden_biased)
                one_minus_hidden = self.calculateOneMinusHidden(hidden)
                tmp_h = self.__V.multiplyWithVectorFromLeft(r_minus_y)
                tmp_h.remove(0)
                tmp_hidden = one_minus_hidden.elementProduct(hidden.elementProduct(tmp_h))
                delta_w = Matrix(tmp_hidden, self.x)
                delta_v.multiplyWithConstant(learning_rate)
                self.__V.add(delta_v)
                delta_w.multiplyWithConstant(learning_rate)
                self.__W.add(delta_w)
            current_performance = self.testAutoEncoder(validationSet)
            if current_performance.getErrorRate() < best_performance.getErrorRate():
                best_performance = current_performance
                best_w = copy.deepcopy(self.__W)
                best_v = copy.deepcopy(self.__V)
        self.__W = best_w
        self.__V = best_v

    cpdef __allocateWeights(self,
                            int H,
                            int seed):
        """
        The allocateWeights method takes an integer number and sets layer weights of W and V matrices according to given
        number.

        PARAMETERS
        ----------
        H : int
            Integer input.
        """
        self.__W = self.allocateLayerWeights(H, self.d + 1, seed)
        self.__V = self.allocateLayerWeights(self.K, H + 1, seed)

    cpdef Performance testAutoEncoder(self, InstanceList data):
        """
        The testAutoEncoder method takes an InstanceList as an input and tries to predict a value and finds the
        difference with the actual value for each item of that InstanceList. At the end, it returns an error rate by
        finding the mean of total errors.

        PARAMETERS
        ----------
        data : InstanceList
            InstanceList to use as validation set.

        RETURNS
        -------
        Performance
            Error rate by finding the mean of total errors.
        """
        cdef int total, i
        cdef double error
        total = data.size()
        error = 0.0
        for i in range(total):
            self.y = self.__predictInput(data.get(i))
            self.r = data.get(i).toVector()
            error += self.r.difference(self.y).dotProductWithSelf()
        return Performance(error / total)

    cpdef Vector __predictInput(self, Instance instance):
        """
        The predictInput method takes an Instance as an input and calculates a forward single hidden layer and returns
        the predicted value.

        PARAMETERS
        ----------
        instance : Instance
            Instance to predict.

        RETURNS
        -------
        Vector
            Predicted value.
        """
        self.createInputVector(instance)
        self.calculateForwardSingleHiddenLayer(W=self.__W,
                                               V=self.__V,
                                               activationFunction=ActivationFunction.SIGMOID)
        return self.y

    cpdef calculateOutput(self):
        """
        The calculateOutput method calculates a forward single hidden layer.
        """
        self.calculateForwardSingleHiddenLayer(W=self.__W,
                                               V=self.__V,
                                               activationFunction=ActivationFunction.SIGMOID)
