cdef class ValidatedModel(Model):

    cpdef ClassificationPerformance testClassifier(self, InstanceList data):
        """
        The testClassifier method takes an InstanceList as an input and returns an accuracy value as
        ClassificationPerformance.

        PARAMETERS
        ----------
        data : InstanceList
            InstanceList to test.

        RETURNS
        -------
        ClassificationPerformance
            Accuracy value as ClassificationPerformance.
        """
        cdef int total, count, i
        total = data.size()
        count = 0
        for i in range(data.size()):
            if data.get(i).getClassLabel() == self.predict(data.get(i)):
                count = count + 1
        return ClassificationPerformance(count / total)
