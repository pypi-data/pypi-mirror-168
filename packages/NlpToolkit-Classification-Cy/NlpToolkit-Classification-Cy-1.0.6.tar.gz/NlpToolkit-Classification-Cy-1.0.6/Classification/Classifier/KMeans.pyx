from Classification.Classifier.Classifier cimport Classifier
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.InstanceList.Partition cimport Partition
from Classification.Model.KMeansModel cimport KMeansModel
from Math.DiscreteDistribution cimport DiscreteDistribution
from Classification.Parameter.Parameter cimport Parameter


cdef class KMeans(Classifier):

    cpdef train(self,
                InstanceList trainSet,
                Parameter parameters):
        cdef DiscreteDistribution prior_distribution
        cdef InstanceList class_means
        cdef Partition class_lists
        cdef int i
        prior_distribution = trainSet.classDistribution()
        class_means = InstanceList()
        class_lists = Partition(trainSet)
        for i in range(class_lists.size()):
            class_means.add(class_lists.get(i).average())
        self.model = KMeansModel(priorDistribution=prior_distribution,
                                 classMeans=class_means,
                                 distanceMetric=parameters.getDistanceMetric())
