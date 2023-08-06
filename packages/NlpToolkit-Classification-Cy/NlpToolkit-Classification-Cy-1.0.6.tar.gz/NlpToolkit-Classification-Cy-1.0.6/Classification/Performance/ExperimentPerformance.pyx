import math
from Classification.Performance.ConfusionMatrix cimport ConfusionMatrix


cdef class ExperimentPerformance:

    def __init__(self):
        """
        A constructor which creates a new list of Performance as results.
        """
        self.__results = []
        self.__contains_details = True
        self.__classification = True

    def __gt__(self, other) -> bool:
        accuracy1 = self.meanClassificationPerformance().getAccuracy()
        accuracy2 = other.meanClassificationPerformance().getAccuracy()
        return accuracy1 > accuracy2

    def __lt__(self, other) -> bool:
        accuracy1 = self.meanClassificationPerformance().getAccuracy()
        accuracy2 = other.meanClassificationPerformance().getAccuracy()
        return accuracy1 < accuracy2

    cpdef initWithFile(self, str fileName):
        """
        A constructor that takes a file name as an input and takes the inputs from that file assigns these inputs to the
        errorRate and adds them to the results list as a new Performance.

        PARAMETERS
        ----------
        fileName : str
            String input.
        """
        cdef str line
        cdef list lines
        self.__contains_details = False
        inputFile = open(fileName, "r", encoding='utf8')
        lines = inputFile.readlines()
        inputFile.close()
        for line in lines:
            self.__results.append(Performance(float(line)))

    cpdef add(self, Performance performance):
        """
        The add method takes a Performance as an input and adds it to the results list.

        PARAMETERS
        ----------
        performance : Performance
            Performance input.
        """
        if not isinstance(performance, DetailedClassificationPerformance):
            self.__contains_details = False
        if not isinstance(performance, ClassificationPerformance):
            self.__classification = False
        self.__results.append(performance)

    cpdef int numberOfExperiments(self):
        """
        The numberOfExperiments method returns the size of the results {@link ArrayList}.

        RETURNS
        -------
        int
            The results list.
        """
        return len(self.__results)

    cpdef double getErrorRate(self, int index):
        """
        The getErrorRate method takes an index as an input and returns the errorRate at given index of results list.

        PARAMETERS
        ----------
        index : int
            Index of results list to retrieve.

        RETURNS
        -------
        float
            The errorRate at given index of results list.
        """
        return self.__results[index].getErrorRate()

    cpdef double getAccuracy(self, int index):
        """
        The getAccuracy method takes an index as an input. It returns the accuracy of a Performance at given index
        of results list.

        PARAMETERS
        ----------
        index : int
            Index of results list to retrieve.

        RETURNS
        -------
        float
            The accuracy of a Performance at given index of results list.
        """
        return self.__results[index].getAccuracy()

    cpdef Performance meanPerformance(self):
        """
        The meanPerformance method loops through the performances of results list and sums up the errorRates of each
        then returns a new Performance with the mean of that summation.

        RETURNS
        -------
        Performance
            A new Performance with the mean of the summation of errorRates.
        """
        cdef double sum_error
        cdef Performance performance
        sum_error = 0
        for performance in self.__results:
            sum_error += performance.getErrorRate()
        return Performance(sum_error / len(self.__results))

    cpdef ClassificationPerformance meanClassificationPerformance(self):
        """
        The meanClassificationPerformance method loops through the performances of results list and sums up
        the accuracy of each classification performance, then returns a new classificationPerformance with the mean of
        that summation.

        RETURNS
        -------
        ClassificationPerformance
            A new classificationPerformance with the mean of that summation.
        """
        cdef double sum_accuracy
        cdef ClassificationPerformance performance
        if len(self.__results) == 0 or not self.__classification:
            return None
        sum_accuracy = 0
        for performance in self.__results:
            sum_accuracy += performance.getAccuracy()
        return ClassificationPerformance(sum_accuracy / len(self.__results))

    cpdef DetailedClassificationPerformance meanDetailedPerformance(self):
        """
        The meanDetailedPerformance method gets the first confusion matrix of results list.
        Then, it adds new confusion matrices as the DetailedClassificationPerformance of other elements of results
        ArrayList' confusion matrices as a DetailedClassificationPerformance.

        RETURNS
        -------
        DetailedCassificationPerformance
            A new DetailedClassificationPerformance with the ConfusionMatrix sum.
        """
        cdef ConfusionMatrix sum_matrix
        cdef int i
        if len(self.__results) == 0 or not self.__contains_details:
            return None
        sum_matrix = self.__results[0].getConfusionMatrix()
        for i in range(1, len(self.__results)):
            sum_matrix.addConfusionMatrix(self.__results[i].getConfusionMatrix())
        return DetailedClassificationPerformance(sum_matrix)

    cpdef Performance standardDeviationPerformance(self):
        """
        The standardDeviationPerformance method loops through the Performances of results list and returns
        a new Performance with the standard deviation.

        RETURNS
        -------
        Performance
            A new Performance with the standard deviation.
        """
        cdef double sum_error_rate
        cdef Performance average_performance, performance
        sum_error_rate = 0
        average_performance = self.meanPerformance()
        for performance in self.__results:
            sum_error_rate += math.pow(performance.getErrorRate() - average_performance.getErrorRate(), 2)
        return Performance(math.sqrt(sum_error_rate / (len(self.__results) - 1)))

    cpdef ClassificationPerformance standardDeviationClassificationPerformance(self):
        """
        The standardDeviationClassificationPerformance method loops through the Performances of results list and
        returns a new ClassificationPerformance with standard deviation.

        RETURNS
        -------
        ClassificationPerformance
            A new ClassificationPerformance with standard deviation.
        """
        cdef double sum_accuracy, sum_error_rate
        cdef ClassificationPerformance averageClassificationPerformance, performance
        if len(self.__results) == 0 or not self.__classification:
            return None
        sum_accuracy = 0
        sum_error_rate = 0
        averageClassificationPerformance = self.meanClassificationPerformance()
        for performance in self.__results:
            sum_accuracy += math.pow(performance.getAccuracy() - averageClassificationPerformance.getAccuracy(), 2)
            sum_error_rate += math.pow(performance.getErrorRate() - averageClassificationPerformance.getErrorRate(), 2)
        return ClassificationPerformance(math.sqrt(sum_accuracy / (len(self.__results) - 1)))

    cpdef bint isBetter(self, ExperimentPerformance experimentPerformance):
        """
        The isBetter method  takes an ExperimentPerformance as an input and returns true if the result of compareTo
        method is positive and false otherwise.

        PARAMETERS
        ----------
        experimentPerformance : ExperimentPerformance
            ExperimentPerformance input.

        RETURNS
        -------
        bool
            True if the experiment performance is better than the given experiment performance.
        """
        return self > experimentPerformance
