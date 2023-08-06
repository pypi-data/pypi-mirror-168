from Classification.Classifier.Classifier cimport Classifier
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Model.DummyModel cimport DummyModel
from Classification.Parameter.Parameter cimport Parameter


cdef class Dummy(Classifier):

    cpdef train(self,
                InstanceList trainSet,
                Parameter parameters):
        """
        Training algorithm for the dummy classifier. Actually dummy classifier returns the maximum occurring class in
        the training data, there is no training.

        PARAMETERS
        ----------
        trainSet: InstanceList
            Training data given to the algorithm.
        parameters: Parameter
            Parameter of the Dummy algorithm.
        """
        self.model = DummyModel(trainSet)
