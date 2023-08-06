from Math.Matrix cimport Matrix
from Math.Vector cimport Vector
from Math.DiscreteDistribution cimport DiscreteDistribution

from Classification.Classifier.Classifier cimport Classifier
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.InstanceList.Partition cimport Partition
from Classification.Model.LdaModel cimport LdaModel
from Classification.Parameter.Parameter cimport Parameter

import math


cdef class Lda(Classifier):

    cpdef train(self,
                InstanceList trainSet,
                Parameter parameters):
        """
        Training algorithm for the linear discriminant analysis classifier (Introduction to Machine Learning, Alpaydin,
        2015).

        PARAMETERS
        ----------
        trainSet : InstanceList
            Training data given to the algorithm.
        parameters : Parameter
            Parameter of the Lda algorithm.
        """
        cdef dict w0, s
        cdef DiscreteDistribution prior_distribution
        cdef Partition class_lists
        cdef Matrix covariance, class_covariance
        cdef int i
        cdef Vector average_vector, wi
        cdef str Ci
        cdef double w0i
        w0 = {}
        w = {}
        prior_distribution = trainSet.classDistribution()
        class_lists = Partition(trainSet)
        covariance = Matrix(trainSet.get(0).continuousAttributeSize(), trainSet.get(0).continuousAttributeSize())
        for i in range(class_lists.size()):
            average_vector = Vector(class_lists.get(i).continuousAverage())
            class_covariance = class_lists.get(i).covariance(average_vector)
            class_covariance.multiplyWithConstant(class_lists.get(i).size() - 1)
            covariance.add(class_covariance)
        covariance.divideByConstant(trainSet.size() - class_lists.size())
        covariance.inverse()
        for i in range(class_lists.size()):
            Ci = class_lists.get(i).getClassLabel()
            average_vector = Vector(class_lists.get(i).continuousAverage())
            wi = covariance.multiplyWithVectorFromRight(average_vector)
            w[Ci] = wi
            w0i = -0.5 * wi.dotProduct(average_vector) + math.log(prior_distribution.getProbability(Ci))
            w0[Ci] = w0i
        self.model = LdaModel(prior_distribution, w, w0)
