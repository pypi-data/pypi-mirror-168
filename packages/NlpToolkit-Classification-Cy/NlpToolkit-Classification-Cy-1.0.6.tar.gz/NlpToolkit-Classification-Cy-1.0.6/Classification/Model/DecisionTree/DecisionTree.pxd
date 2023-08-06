from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Model.DecisionTree.DecisionNode cimport DecisionNode
from Classification.Model.ValidatedModel cimport ValidatedModel
from Classification.Instance.Instance cimport Instance


cdef class DecisionTree(ValidatedModel):

    cdef DecisionNode __root

    cpdef pruneNode(self, DecisionNode node, InstanceList pruneSet)
    cpdef prune(self, InstanceList pruneSet)
    cpdef dict predictProbability(self, Instance instance)
    cpdef str predict(self, Instance instance)
