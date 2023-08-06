from Math.Matrix cimport Matrix
from Math.Vector cimport Vector

from Classification.DistanceMetric.DistanceMetric cimport DistanceMetric
from Classification.Instance.Instance cimport Instance


cdef class MahalanobisDistance(DistanceMetric):

    cdef Matrix __covarianceInverse

    def __init__(self, covarianceInverse: Matrix):
        """
        Constructor for the MahalanobisDistance class. Basically sets the inverse of the covariance matrix.

        PARAMETERS
        ----------
        covarianceInverse : Matrix
            Inverse of the covariance matrix.
        """
        self.__covarianceInverse = covarianceInverse

    cpdef double distance(self,
                          Instance instance1,
                          Instance instance2):
        """
        Calculates Mahalanobis distance between two instances. (x^(1) - x^(2)) S (x^(1) - x^(2))^T

        PARAMETERS
        ----------
        instance1 : Instance
            First instance.
        instance2 : Instance
            Second instance.

        RETURNS
        -------
        float
            Mahalanobis distance between two instances.
        """
        cdef Vector v1, v2, v3
        v1 = instance1.toVector()
        v2 = instance2.toVector()
        v1.subtract(v2)
        v3 = self.__covarianceInverse.multiplyWithVectorFromLeft(v1)
        return v3.dotProduct(v1)
