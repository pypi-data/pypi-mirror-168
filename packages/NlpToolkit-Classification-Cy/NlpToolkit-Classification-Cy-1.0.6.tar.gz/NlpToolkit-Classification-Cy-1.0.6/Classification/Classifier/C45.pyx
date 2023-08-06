from Classification.Classifier.Classifier cimport Classifier
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.InstanceList.Partition cimport Partition
from Classification.Model.DecisionTree.DecisionNode cimport DecisionNode
from Classification.Model.DecisionTree.DecisionTree cimport DecisionTree
from Classification.Parameter.Parameter cimport Parameter


cdef class C45(Classifier):

    cpdef train(self,
                InstanceList trainSet,
                Parameter parameters):
        """
        Training algorithm for C4.5 univariate decision tree classifier. 20 percent of the data are left aside for
        pruning 80 percent of the data is used for constructing the tree.

        PARAMETERS
        ----------
        trainSet : InstanceList
            Training data given to the algorithm.
        parameters: C45Parameter
            Parameter of the C45 algorithm.
        """
        cdef Partition partition
        cdef DecisionTree tree
        if parameters.isPrune():
            partition = Partition(instanceList=trainSet,
                                  ratio=parameters.getCrossValidationRatio(),
                                  seed=parameters.getSeed(),
                                  stratified=True)
            tree = DecisionTree(DecisionNode(partition.get(1)))
            tree.prune(partition.get(0))
        else:
            tree = DecisionTree(DecisionNode(trainSet))
        self.model = tree
