from Classification.FeatureSelection.FeatureSubSet cimport FeatureSubSet
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.DataSet.DataDefinition cimport DataDefinition
from Classification.Instance.Instance cimport Instance


cdef class DataSet(object):

    cdef InstanceList __instances
    cdef DataDefinition __definition

    cpdef initWithFile(self, str fileName)
    cpdef bint __checkDefinition(self, Instance instance)
    cpdef __setDefinition(self, Instance instance)
    cpdef int sampleSize(self)
    cpdef int classCount(self)
    cpdef int attributeCount(self)
    cpdef int discreteAttributeCount(self)
    cpdef int continuousAttributeCount(self)
    cpdef str getClasses(self)
    cpdef str info(self, str dataSetName)
    cpdef addInstance(self, Instance current)
    cpdef addInstanceList(self, list instanceList)
    cpdef list getInstances(self)
    cpdef list getClassInstances(self)
    cpdef InstanceList getInstanceList(self)
    cpdef DataDefinition getDataDefinition(self)
    cpdef DataSet getSubSetOfFeatures(self, FeatureSubSet featureSubSet)
    cpdef writeToFile(self, str outFileName)
