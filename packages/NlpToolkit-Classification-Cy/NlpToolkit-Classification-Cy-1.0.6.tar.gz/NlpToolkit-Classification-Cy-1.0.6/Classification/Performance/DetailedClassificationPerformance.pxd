from Classification.Performance.ClassificationPerformance cimport ClassificationPerformance
from Classification.Performance.ConfusionMatrix cimport ConfusionMatrix


cdef class DetailedClassificationPerformance(ClassificationPerformance):

    cdef ConfusionMatrix __confusion_matrix

    cpdef ConfusionMatrix getConfusionMatrix(self)
