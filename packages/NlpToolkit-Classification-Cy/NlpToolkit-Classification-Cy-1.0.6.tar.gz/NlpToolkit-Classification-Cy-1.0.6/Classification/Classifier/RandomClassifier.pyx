from Classification.Classifier.Classifier cimport Classifier
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Model.RandomModel cimport RandomModel
from Classification.Parameter.Parameter cimport Parameter


cdef class RandomClassifier(Classifier):

    cpdef train(self,
                InstanceList trainSet,
                Parameter parameters):
        """
        Training algorithm for random classifier.

        PARAMETERS
        ----------
        trainSet : InstanceList
            Training data given to the algorithm.
        """
        self.model = RandomModel(classLabels=list(trainSet.classDistribution().keys()),
                                 seed=parameters.getSeed())
