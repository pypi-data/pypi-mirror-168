from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Parameter.Parameter cimport Parameter
from Classification.Instance.Instance cimport Instance
from Classification.Performance.Performance cimport Performance
from Classification.Model.Model cimport Model


cdef class Classifier(object):

    cdef Model model

    cpdef train(self, InstanceList trainSet, Parameter parameters)
    cpdef bint discreteCheck(self, Instance instance)
    cpdef Performance test(self, InstanceList testSet)
    cpdef Performance singleRun(self, Parameter parameter, InstanceList trainSet, InstanceList testSet)
    cpdef Model getModel(self)
