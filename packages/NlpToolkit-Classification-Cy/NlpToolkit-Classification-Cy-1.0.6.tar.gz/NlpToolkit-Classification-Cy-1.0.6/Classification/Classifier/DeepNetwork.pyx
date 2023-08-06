from Classification.Classifier.Classifier cimport Classifier
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.InstanceList.Partition cimport Partition
from Classification.Model.DeepNetworkModel cimport DeepNetworkModel
from Classification.Parameter.Parameter cimport Parameter


cdef class DeepNetwork(Classifier):

    cpdef train(self,
                InstanceList trainSet,
                Parameter parameters):
        """
        Training algorithm for deep network classifier.

        PARAMETERS
        ----------
        trainSet : InstanceList
            Training data given to the algorithm.
        parameters : DeepNetworkParameter
            Parameters of the deep network algorithm. crossValidationRatio and seed are used as parameters.
        """
        cdef Partition partition
        partition = Partition(instanceList=trainSet,
                              ratio=parameters.getCrossValidationRatio(),
                              seed=parameters.getSeed(),
                              stratified=True)
        self.model = DeepNetworkModel(trainSet=partition.get(1),
                                      validationSet=partition.get(0),
                                      parameters=parameters)
