from Classification.Model.Model cimport Model
from Classification.Performance.ClassificationPerformance cimport ClassificationPerformance
from Classification.InstanceList.InstanceList cimport InstanceList


cdef class ValidatedModel(Model):

    cpdef ClassificationPerformance testClassifier(self, InstanceList data)
