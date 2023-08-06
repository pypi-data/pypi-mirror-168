import copy
from Classification.InstanceList.InstanceList cimport InstanceList
from Math.Matrix cimport Matrix
from Math.Vector cimport Vector
from Classification.Performance.ClassificationPerformance cimport ClassificationPerformance

from Classification.Parameter.ActivationFunction import ActivationFunction

cdef class DeepNetworkModel(NeuralNetworkModel):

    def __init__(self,
                 trainSet: InstanceList,
                 validationSet: InstanceList,
                 parameters: DeepNetworkParameter):
        """
        Constructor that takes two InstanceList train set and validation set and DeepNetworkParameter as
        inputs. First it sets the class labels, their sizes as K and the size of the continuous attributes as d of given
        train set and allocates weights and sets the best weights. At each epoch, it shuffles the train set and loops
        through the each item of that train set, it multiplies the weights Matrix with input Vector than applies the
        sigmoid function and stores the result as hidden and add bias. Then updates weights and at the end it compares
        the performance of these weights with validation set. It updates the bestClassificationPerformance and
        bestWeights according to the current situation. At the end it updates the learning rate via etaDecrease value
        and finishes with clearing the weights.

        PARAMETERS
        ----------
        trainSet : InstanceList
            InstanceList to be used as trainSet.
        validationSet : InstanceList
            InstanceList to be used as validationSet.
        parameters : DeepNetworkParameter
            DeepNetworkParameter input.
        """
        cdef list delta_weights, hidden, hidden_biased, best_weights
        cdef ClassificationPerformance best_classification_performance, current_classification_performance
        cdef int epoch, i, j, k
        cdef double learning_rate
        cdef Vector r_minus_y, one_minus_hidden, tmp_h, tmp_hidden
        cdef Matrix m
        super().__init__(trainSet)
        delta_weights = []
        hidden = []
        hidden_biased = []
        self.__activation_function = parameters.getActivationFunction()
        self.__allocateWeights(parameters)
        best_weights = self.__setBestWeights()
        best_classification_performance = ClassificationPerformance(0.0)
        epoch = parameters.getEpoch()
        learning_rate = parameters.getLearningRate()
        for i in range(epoch):
            trainSet.shuffle(parameters.getSeed())
            for j in range(trainSet.size()):
                self.createInputVector(trainSet.get(j))
                hidden.clear()
                hidden_biased.clear()
                delta_weights.clear()
                for k in range(self.__hidden_layer_size):
                    if k == 0:
                        hidden.append(self.calculateHidden(self.x, self.__weights[k], self.__activation_function))
                    else:
                        hidden.append(self.calculateHidden(hidden_biased[k - 1], self.__weights[k], self.__activation_function))
                    hidden_biased.append(hidden[k].biased())
                r_minus_y = self.calculateRMinusY(trainSet.get(j), hidden_biased[self.__hidden_layer_size - 1],
                                                  self.__weights[len(self.__weights) - 1])
                delta_weights.insert(0, Matrix(r_minus_y, hidden_biased[self.__hidden_layer_size - 1]))
                for k in range(len(self.__weights) - 2, -1, -1):
                    if k == len(self.__weights) - 2:
                        tmp_h = self.__weights[k + 1].multiplyWithVectorFromLeft(r_minus_y)
                    else:
                        tmp_h = self.__weights[k + 1].multiplyWithVectorFromLeft(tmp_hidden)
                    tmp_h.remove(0)
                    if self.__activation_function == ActivationFunction.SIGMOID:
                        one_minus_hidden = self.calculateOneMinusHidden(hidden[k])
                        activation_derivative = one_minus_hidden.elementProduct(hidden[k])
                    elif self.__activation_function == ActivationFunction.TANH:
                        one = Vector(hidden[k].size(), 1.0)
                        hidden[k].tanh()
                        activation_derivative = one.difference(hidden[k].elementProduct(hidden[k]))
                    elif self.__activation_function == ActivationFunction.RELU:
                        hidden[k].reluDerivative()
                        activation_derivative = hidden
                    tmp_hidden = tmp_h.elementProduct(activation_derivative)
                    if k == 0:
                        delta_weights.insert(0, Matrix(tmp_hidden, self.x))
                    else:
                        delta_weights.insert(0, Matrix(tmp_hidden, hidden_biased[k - 1]))
                for k in range(len(self.__weights)):
                    delta_weights[k].multiplyWithConstant(learning_rate)
                    self.__weights[k].add(delta_weights[k])
            current_classification_performance = self.testClassifier(validationSet)
            if current_classification_performance.getAccuracy() > best_classification_performance.getAccuracy():
                best_classification_performance = current_classification_performance
                best_weights = self.__setBestWeights()
            learning_rate *= parameters.getEtaDecrease()
        self.__weights.clear()
        for m in best_weights:
            self.__weights.append(m)

    cpdef __allocateWeights(self, DeepNetworkParameter parameters):
        """
        The allocateWeights method takes DeepNetworkParameters as an input. First it adds random weights to the list
        of Matrix} weights' first layer. Then it loops through the layers and adds random weights till the last layer.
        At the end it adds random weights to the last layer and also sets the hiddenLayerSize value.

        PARAMETERS
        ----------
        parameters : DeepNetworkParameter
            DeepNetworkParameter input.
        """
        cdef int i
        self.__weights = []
        self.__weights.append(self.allocateLayerWeights(row=parameters.getHiddenNodes(0),
                                                        column=self.d + 1,
                                                        seed=parameters.getSeed()))
        for i in range(parameters.layerSize() - 1):
            self.__weights.append(self.allocateLayerWeights(row=parameters.getHiddenNodes(i + 1),
                                                            column=parameters.getHiddenNodes(i) + 1,
                                                            seed=parameters.getSeed()))
        self.__weights.append(self.allocateLayerWeights(row=self.K,
                                                        column=parameters.getHiddenNodes(parameters.layerSize() - 1) + 1,
                                                        seed=parameters.getSeed()))
        self.__hidden_layer_size = parameters.layerSize()

    cpdef list __setBestWeights(self):
        """
        The setBestWeights method creates a list of Matrix as bestWeights and clones the values of weights list
        into this newly created list.

        RETURNS
        -------
        list
        A list clones from the weights ArrayList.
        """
        cdef list best_weights
        cdef Matrix m
        best_weights = []
        for m in self.__weights:
            best_weights.append(copy.deepcopy(m))
        return best_weights

    cpdef calculateOutput(self):
        """
        The calculateOutput method loops size of the weights times and calculate one hidden layer at a time and adds
        bias term. At the end it updates the output y value.
        """
        cdef Vector hidden_biased, hidden
        cdef int i
        hidden_biased = None
        for i in range(len(self.__weights) - 1):
            if i == 0:
                hidden = self.calculateHidden(self.x, self.__weights[i], self.__activation_function)
            else:
                hidden = self.calculateHidden(hidden_biased, self.__weights[i], self.__activation_function)
            hidden_biased = hidden.biased()
        self.y = self.__weights[len(self.__weights) - 1].multiplyWithVectorFromRight(hidden_biased)
