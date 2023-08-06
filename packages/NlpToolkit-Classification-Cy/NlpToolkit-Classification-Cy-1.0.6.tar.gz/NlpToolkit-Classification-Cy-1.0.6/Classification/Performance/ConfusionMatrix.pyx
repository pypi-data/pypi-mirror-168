from DataStructure.CounterHashMap cimport CounterHashMap


cdef class ConfusionMatrix:

    def __init__(self, classLabels: list):
        """
        Constructor that sets the class labels list and creates new dictionary matrix

        PARAMETERS
        ----------
        classLabels : list
            list of String.
        """
        self.__class_labels = classLabels
        self.__matrix = {}

    cpdef classify(self,
                   str actualClass,
                   str predictedClass):
        """
        The classify method takes two Strings; actual class and predicted class as inputs. If the matrix dictionary
        contains given actual class String as a key, it then assigns the corresponding object of that key to a
        CounterHashMap, if not it creates a new CounterHashMap. Then, it puts the given predicted class String to the
        counterHashMap and also put this counterHashMap to the matrix dictionary together with the given actual class
        String.

        PARAMETERS
        ----------
        actualClass : str
            String input actual class.
        predictedClass : str
            String input predicted class.
        """
        cdef CounterHashMap counter_hash_map
        if actualClass in self.__matrix:
            counter_hash_map = self.__matrix[actualClass]
        else:
            counter_hash_map = CounterHashMap()
        counter_hash_map.put(predictedClass)
        self.__matrix[actualClass] = counter_hash_map

    cpdef addConfusionMatrix(self, ConfusionMatrix confusionMatrix):
        """
        The addConfusionMatrix method takes a ConfusionMatrix as an input and loops through actual classes of that
        dictionary and initially gets one row at a time. Then it puts the current row to the matrix dictionary together
        with the actual class string.

        PARAMETERS
        ----------
        confusionMatrix : ConfusionMatrix
            ConfusionMatrix input.
        """
        cdef str actual_class
        cdef CounterHashMap row_to_be_added, current_row
        for actual_class in confusionMatrix.__matrix:
            row_to_be_added = confusionMatrix.__matrix[actual_class]
            if actual_class in self.__matrix:
                current_row = self.__matrix[actual_class]
                current_row.add(row_to_be_added)
                self.__matrix[actual_class] = current_row
            else:
                self.__matrix[actual_class] = row_to_be_added

    cpdef double sumOfElements(self):
        """
        The sumOfElements method loops through the keys in matrix dictionary and returns the summation of all the values
        of the keys. I.e: TP+TN+FP+FN.

        RETURNS
        -------
        float
            The summation of values.
        """
        cdef double result
        cdef str actual_class
        result = 0
        for actual_class in self.__matrix:
            result += self.__matrix[actual_class].sumOfCounts()
        return result

    cpdef double trace(self):
        """
        The trace method loops through the keys in matrix dictionary and if the current key contains the actual key,
        it accumulates the corresponding values. I.e: TP+TN.

        RETURNS
        -------
        float
            Summation of values.
        """
        cdef double result
        cdef str actual_class
        result = 0
        for actual_class in self.__matrix:
            if actual_class in self.__matrix[actual_class]:
                result += self.__matrix[actual_class][actual_class]
        return result

    cpdef double columnSum(self, str predictedClass):
        """
        The columnSum method takes a String predicted class as input, and loops through the keys in matrix dictionary.
        If the current key contains the predicted class String, it accumulates the corresponding values. I.e: TP+FP.

        PARAMETERS
        ----------
        predictedClass : str
            String input predicted class.

        RETURNS
        -------
        float
            Summation of values.
        """
        cdef double result
        cdef str actual_class
        result = 0
        for actual_class in self.__matrix:
            if predictedClass in self.__matrix[actual_class]:
                result += self.__matrix[actual_class][predictedClass]
        return result

    cpdef double getAccuracy(self):
        """
        The getAccuracy method returns the result of  TP+TN / TP+TN+FP+FN

        RETURNS
        -------
        list
            the result of  TP+TN / TP+TN+FP+FN
        """
        return self.trace() / self.sumOfElements()

    cpdef list precision(self):
        """
        The precision method loops through the class labels and returns the resulting Array which has the result of
        TP/FP+TP.

        RETURNS
        -------
        list
            The result of TP/FP+TP.
        """
        cdef list result
        cdef int i
        cdef str actual_class
        result = []
        for i in range(len(self.__class_labels)):
            actual_class = self.__class_labels[i]
            if actual_class in self.__matrix:
                result.append(self.__matrix[actual_class][actual_class] / self.columnSum(actual_class))
        return result

    cpdef list recall(self):
        """
        The recall method loops through the class labels and returns the resulting Array which has the result of
        TP/FN+TP.

        RETURNS
        -------
        list
            The result of TP/FN+TP.
        """
        cdef list result
        cdef int i
        cdef str actual_class
        result = []
        for i in range(len(self.__class_labels)):
            actual_class = self.__class_labels[i]
            if actual_class in self.__matrix:
                result.append(self.__matrix[actual_class][actual_class] / self.__matrix[actual_class].sumOfCounts())
        return result

    cpdef list fMeasure(self):
        """
        The fMeasure method loops through the class labels and returns the resulting Array which has the average of
        recall and precision.

        RETURNS
        -------
        list
            The average of recall and precision.
        """
        cdef list precision, recall, result
        cdef int i
        precision = self.precision()
        recall = self.recall()
        result = []
        for i in range(len(self.__class_labels)):
            result.append(2 / (1 / precision[i] + 1 / recall[i]))
        return result

    cpdef double weightedFMeasure(self):
        """
        The weightedFMeasure method loops through the class labels and returns the resulting Array which has the
        weighted average of recall and precision.

        RETURNS
        -------
        float
            The weighted average of recall and precision.
        """
        cdef double total
        cdef int i
        cdef str actual_class
        cdef list f_measure
        f_measure = self.fMeasure()
        total = 0
        for i in range(len(self.__class_labels)):
            actual_class = self.__class_labels[i]
            total += f_measure[i] * self.__matrix[actual_class].sumOfCounts()
        return total / self.sumOfElements()
