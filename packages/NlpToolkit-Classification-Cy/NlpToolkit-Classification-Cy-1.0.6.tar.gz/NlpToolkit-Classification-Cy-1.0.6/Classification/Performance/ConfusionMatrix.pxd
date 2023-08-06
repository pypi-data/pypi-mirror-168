cdef class ConfusionMatrix:

    cdef dict __matrix
    cdef list __class_labels

    cpdef classify(self, str actualClass, str predictedClass)
    cpdef addConfusionMatrix(self, ConfusionMatrix confusionMatrix)
    cpdef double sumOfElements(self)
    cpdef double trace(self)
    cpdef double columnSum(self, str predictedClass)
    cpdef double getAccuracy(self)
    cpdef list precision(self)
    cpdef list recall(self)
    cpdef list fMeasure(self)
    cpdef double weightedFMeasure(self)