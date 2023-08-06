from Classification.FeatureSelection.FeatureSubSet cimport FeatureSubSet


cdef class DataDefinition(object):

    cdef list __attributeTypes

    cpdef int attributeCount(self)
    cpdef int discreteAttributeCount(self)
    cpdef int continuousAttributeCount(self)
    cpdef object getAttributeType(self, int index)
    cpdef addAttribute(self, object attributeType)
    cpdef removeAttribute(self, int index)
    cpdef removeAllAtrributes(self)
    cpdef DataDefinition getSubSetOfFeatures(self, FeatureSubSet featureSubSet)
