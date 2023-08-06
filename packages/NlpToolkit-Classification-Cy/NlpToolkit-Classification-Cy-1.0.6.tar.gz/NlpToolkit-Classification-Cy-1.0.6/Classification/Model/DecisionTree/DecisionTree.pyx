from Classification.Instance.CompositeInstance cimport CompositeInstance
from Classification.Performance.ClassificationPerformance cimport ClassificationPerformance


cdef class DecisionTree(ValidatedModel):

    def __init__(self, root: DecisionNode):
        """
        Constructor that sets root node of the decision tree.

        PARAMETERS
        ----------
        root : DecisionNode
            DecisionNode type input.
        """
        self.__root = root

    cpdef str predict(self, Instance instance):
        """
        The predict method  performs prediction on the root node of given instance, and if it is null, it returns the
        possible class labels. Otherwise it returns the returned class labels.

        PARAMETERS
        ----------
        instance : Instance
            Instance make prediction.

        RETURNS
        -------
        str
            Possible class labels.
        """
        cdef str predicted_class
        predicted_class = self.__root.predict(instance)
        if predicted_class is None and isinstance(instance, CompositeInstance):
            predicted_class = instance.getPossibleClassLabels()
        return predicted_class

    cpdef dict predictProbability(self, Instance instance):
        return self.__root.predictProbabilityDistribution(instance)

    cpdef pruneNode(self,
                    DecisionNode node,
                    InstanceList pruneSet):
        """
        The prune method takes a DecisionNode and an InstanceList as inputs. It checks the classification performance
        of given InstanceList before pruning, i.e making a node leaf, and after pruning. If the after performance is
        better than the before performance it prune the given InstanceList from the tree.

        PARAMETERS
        ----------
        node : DecisionNode
            DecisionNode that will be pruned if conditions hold.
        pruneSet : InstanceList
            Small subset of tree that will be removed from tree.
        """
        cdef ClassificationPerformance before, after
        if node.leaf:
            return
        before = self.testClassifier(pruneSet)
        node.leaf = True
        after = self.testClassifier(pruneSet)
        if after.getAccuracy() < before.getAccuracy():
            node.leaf = False
            for child in node.children:
                self.pruneNode(child, pruneSet)

    cpdef prune(self, InstanceList pruneSet):
        """
        The prune method takes an InstanceList and  performs pruning to the root node.

        PARAMETERS
        ----------
        pruneSet : InstanceList
            InstanceList to perform pruning.
        """
        self.pruneNode(self.__root, pruneSet)
