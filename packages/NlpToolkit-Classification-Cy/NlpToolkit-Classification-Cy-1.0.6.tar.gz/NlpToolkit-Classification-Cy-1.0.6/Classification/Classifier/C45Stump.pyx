from Classification.Classifier.Classifier cimport Classifier
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Model.DecisionTree.DecisionNode cimport DecisionNode
from Classification.Model.DecisionTree.DecisionTree cimport DecisionTree
from Classification.Parameter.Parameter cimport Parameter


cdef class C45Stump(Classifier):

    cpdef train(self,
                InstanceList trainSet,
                Parameter parameters):
        """
        Training algorithm for C4.5 Stump univariate decision tree classifier.

        PARAMETERS
        ----------
        trainSet : InstanceList
            Training data given to the algorithm.
        parameters: Parameter
            Parameter of the C45Stump algorithm.
        """
        self.model = DecisionTree(DecisionNode(data=trainSet,
                                               isStump=True))
