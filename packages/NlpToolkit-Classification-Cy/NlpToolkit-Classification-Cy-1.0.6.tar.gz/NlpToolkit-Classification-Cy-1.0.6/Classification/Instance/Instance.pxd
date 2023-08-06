from Classification.Attribute.Attribute cimport Attribute
from Math.Vector cimport Vector
from Classification.FeatureSelection.FeatureSubSet cimport FeatureSubSet


cdef class Instance(object):

    cdef str __class_label
    cdef list __attributes

    cpdef addDiscreteAttribute(self, str value)
    cpdef addContinuousAttribute(self, double value)
    cpdef addAttribute(self, Attribute attribute)
    cpdef addVectorAttribute(self, Vector vector)
    cpdef removeAttribute(self, int index)
    cpdef removeAllAttributes(self)
    cpdef Attribute getAttribute(self, int index)
    cpdef int attributeSize(self)
    cpdef int continuousAttributeSize(self)
    cpdef list continuousAttributes(self)
    cpdef str getClassLabel(self)
    cpdef Instance getSubSetOfFeatures(self, FeatureSubSet featureSubSet)
    cpdef Vector toVector(self)

