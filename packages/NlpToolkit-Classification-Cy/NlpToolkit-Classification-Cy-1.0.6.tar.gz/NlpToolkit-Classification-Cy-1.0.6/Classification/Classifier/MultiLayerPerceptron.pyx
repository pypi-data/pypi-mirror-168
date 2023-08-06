from Classification.Classifier.Classifier cimport Classifier
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.InstanceList.Partition cimport Partition
from Classification.Model.MultiLayerPerceptronModel cimport MultiLayerPerceptronModel
from Classification.Parameter.Parameter cimport Parameter


cdef class MultiLayerPerceptron(Classifier):

    cpdef train(self,
                InstanceList trainSet,
                Parameter parameters):
        """
        Training algorithm for the multilayer perceptron algorithm. 20 percent of the data is separated as
        cross-validation data used for selecting the best weights. 80 percent of the data is used for training the
        multilayer perceptron with gradient descent.

        PARAMETERS
        ----------
        trainSet : InstanceList
            Training data given to the algorithm
        parameters : MultiLayerPerceptronParameter
            Parameters of the multilayer perceptron.
        """
        cdef Partition partition
        partition = Partition(instanceList=trainSet,
                              ratio=parameters.getCrossValidationRatio(),
                              seed=parameters.getSeed(),
                              stratified=True)
        self.model = MultiLayerPerceptronModel(trainSet=partition.get(1),
                                               validationSet=partition.get(0),
                                               parameters=parameters)
