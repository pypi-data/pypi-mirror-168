from Classification.Instance.CompositeInstance cimport CompositeInstance


cdef class GaussianModel(ValidatedModel):

    cpdef double calculateMetric(self,
                                 Instance instance,
                                 str Ci):
        pass

    cpdef str predict(self, Instance instance):
        """
        The predict method takes an Instance as an input. First it gets the size of prior distribution and loops this
        size times. Then it gets the possible class labels and and calculates metric value. At the end, it returns the
        class which has the maximum value of metric.

        PARAMETERS
        ----------
        instance : Instance
            Instance to predict.

        RETURNS
        -------
        str
            The class which has the maximum value of metric.
        """
        cdef double max_metric, metric
        cdef str predicted_class, Ci
        cdef int size, i
        max_metric = -10000000
        if isinstance(instance, CompositeInstance):
            predicted_class = instance.getPossibleClassLabels()[0]
            size = len(instance.getPossibleClassLabels())
        else:
            predicted_class = self.prior_distribution.getMaxItem()
            size = len(self.prior_distribution)
        for i in range(size):
            if isinstance(instance, CompositeInstance):
                Ci = instance.getPossibleClassLabels()[i]
            else:
                Ci = self.prior_distribution.getItem(i)
            if self.prior_distribution.containsItem(Ci):
                metric = self.calculateMetric(instance, Ci)
                if metric > max_metric:
                    max_metric = metric
                    predicted_class = Ci
        return predicted_class