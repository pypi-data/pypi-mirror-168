from Classification.Instance.Instance cimport Instance
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Model.DecisionTree.DecisionCondition cimport DecisionCondition
from Classification.Parameter.RandomForestParameter cimport RandomForestParameter


cdef class DecisionNode(object):

    cdef list children
    cdef InstanceList __data
    cdef str __class_label
    cdef bint leaf
    cdef DecisionCondition __condition

    cpdef __entropyForDiscreteAttribute(self, int attributeIndex)
    cpdef __createChildrenForDiscreteIndexed(self, int attributeIndex, int attributeValue,
                                           RandomForestParameter parameter, bint isStump)
    cpdef __createChildrenForDiscrete(self, int attributeIndex, RandomForestParameter parameter, bint isStump)
    cpdef __createChildrenForContinuous(self, int attributeIndex, double splitValue, RandomForestParameter parameter,
                                      bint isStump)
    cpdef str predict(self, Instance instance)
    cpdef dict predictProbabilityDistribution(self, Instance instance)
