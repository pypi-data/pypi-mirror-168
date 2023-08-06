from Classification.DistanceMetric.EuclidianDistance cimport EuclidianDistance
from Classification.Parameter.KMeansParameter cimport KMeansParameter


cdef class KnnParameter(KMeansParameter):

    cdef int __k

    def __init__(self,
                 seed: int,
                 k: int,
                 distanceMetric=EuclidianDistance()):
        """
        Parameters of the K-nearest neighbor classifier.

        PARAMETERS
        ----------
        seed : int
            Seed is used for random number generation.
        k : int
            Parameter of the K-nearest neighbor algorithm.
        distanceMetric : DistanceMetric
            Used to calculate the distance between two instances.
        """
        super().__init__(seed, distanceMetric)
        self.__k = k

    cpdef int getK(self):
        """
        Accessor for the k.

        RETURNS
        -------
        int
            Value of the k.
        """
        return self.__k
