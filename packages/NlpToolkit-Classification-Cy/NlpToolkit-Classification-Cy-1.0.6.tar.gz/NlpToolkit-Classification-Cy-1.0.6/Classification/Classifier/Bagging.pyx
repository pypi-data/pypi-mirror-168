from Classification.Classifier.Classifier cimport Classifier
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Model.DecisionTree.DecisionNode cimport DecisionNode
from Classification.Model.DecisionTree.DecisionTree cimport DecisionTree
from Classification.Model.TreeEnsembleModel cimport TreeEnsembleModel
from Classification.Parameter.Parameter cimport Parameter
from Sampling.Bootstrap cimport Bootstrap


cdef class Bagging(Classifier):

    cpdef train(self,
                InstanceList trainSet,
                Parameter parameters):
        """
        Bagging bootstrap ensemble method that creates individuals for its ensemble by training each classifier on a
        random redistribution of the training set.
        This training method is for a bagged decision tree classifier. 20 percent of the instances are left aside for
        pruning of the trees 80 percent of the instances are used for training the trees. The number of trees
        (forestSize) is a parameter, and basically the method will learn an ensemble of trees as a model.

        PARAMETERS
        ----------
        trainSet : InstanceList
            Training data given to the algorithm.
        parameters : Parameter
            Parameters of the bagging trees algorithm. ensembleSize returns the number of trees in the bagged forest.
        """
        cdef int forest_size, i
        cdef list forest
        cdef Bootstrap bootstrap
        cdef DecisionTree tree
        forest_size = parameters.getEnsembleSize()
        forest = []
        for i in range(forest_size):
            bootstrap = trainSet.bootstrap(i)
            tree = DecisionTree(DecisionNode(InstanceList(bootstrap.getSample())))
            forest.append(tree)
        self.model = TreeEnsembleModel(forest)
