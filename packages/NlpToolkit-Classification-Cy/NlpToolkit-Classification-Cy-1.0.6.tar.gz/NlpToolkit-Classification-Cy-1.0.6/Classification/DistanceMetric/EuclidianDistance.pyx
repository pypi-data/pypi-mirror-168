from Classification.Attribute.ContinuousAttribute cimport ContinuousAttribute
from Classification.Attribute.DiscreteAttribute cimport DiscreteAttribute
import math


cdef class EuclidianDistance(DistanceMetric):

    cpdef double distance(self,
                          Instance instance1,
                          Instance instance2):
        cdef double result
        cdef int i
        result = 0
        for i in range(instance1.attributeSize()):
            if isinstance(instance1.getAttribute(i), DiscreteAttribute) and \
                    isinstance(instance2.getAttribute(i), DiscreteAttribute):
                if instance1.getAttribute(i).getValue() is not None and \
                        instance1.getAttribute(i).getValue() != instance2.getAttribute(i).getValue():
                    result += 1
            else:
                if isinstance(instance1.getAttribute(i), ContinuousAttribute) and \
                        isinstance(instance2.getAttribute(i), ContinuousAttribute):
                    result += math.pow(instance1.getAttribute(i).getValue() - instance2.getAttribute(i).getValue(), 2)
        return result
