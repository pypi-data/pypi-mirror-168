from Classification.DistanceMetric.EuclidianDistance cimport EuclidianDistance


cdef class KMeansParameter(Parameter):

    def __init__(self,
                 seed: int,
                 distanceMetric=EuclidianDistance()):
        """
        Parameters of the Rocchio classifier.

        PARAMETERS
        ----------
        seed : int
            Seed is used for random number generation.
        distanceMetric : DistanceMetric
            distance metric used to calculate the distance between two instances.
        """
        super().__init__(seed)
        self.distance_metric = distanceMetric

    cpdef DistanceMetric getDistanceMetric(self):
        """
        Accessor for the distanceMetric.

        RETURNS
        -------
        DistanceMetric
            The distanceMetric.
        """
        return self.distance_metric
