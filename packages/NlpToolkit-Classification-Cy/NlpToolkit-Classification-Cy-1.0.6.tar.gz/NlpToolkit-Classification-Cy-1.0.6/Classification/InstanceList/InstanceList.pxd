from Classification.Instance.Instance cimport Instance
from Sampling.Bootstrap cimport Bootstrap
from Classification.Attribute.Attribute cimport Attribute
from Math.DiscreteDistribution cimport DiscreteDistribution
from Math.Vector cimport Vector
from Math.Matrix cimport Matrix


cdef class InstanceList(object):

    cdef list list

    cpdef add(self, Instance instance)
    cpdef addAll(self, list instanceList)
    cpdef int size(self)
    cpdef Instance get(self, int index)
    cpdef sortWrtAttribute(self, int attributeIndex)
    cpdef sort(self)
    cpdef shuffle(self, int seed)
    cpdef Bootstrap bootstrap(self, int seed)
    cpdef list getClassLabels(self)
    cpdef list getDistinctClassLabels(self)
    cpdef list getUnionOfPossibleClassLabels(self)
    cpdef list getAttributeValueList(self, int attributeIndex)
    cpdef Attribute __attributeAverage(self, int index)
    cpdef list continuousAttributeAverage(self, int index)
    cpdef Attribute __attributeStandardDeviation(self, int index)
    cpdef list continuousAttributeStandardDeviation(self, int index)
    cpdef DiscreteDistribution attributeDistribution(self, int index)
    cpdef list attributeClassDistribution(self, int attributeIndex)
    cpdef DiscreteDistribution discreteIndexedAttributeClassDistribution(self, int attributeIndex, int attributeValue)
    cpdef DiscreteDistribution classDistribution(self)
    cpdef list allAttributesDistribution(self)
    cpdef Instance average(self)
    cpdef list continuousAverage(self)
    cpdef Instance standardDeviation(self)
    cpdef list continuousStandardDeviation(self)
    cpdef Matrix covariance(self, Vector average)
    cpdef list getInstances(self)
