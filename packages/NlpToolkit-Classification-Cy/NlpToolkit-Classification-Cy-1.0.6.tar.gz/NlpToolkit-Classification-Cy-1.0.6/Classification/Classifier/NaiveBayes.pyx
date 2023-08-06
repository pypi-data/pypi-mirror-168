from Math.DiscreteDistribution cimport DiscreteDistribution
from Math.Vector cimport Vector

from Classification.Attribute.DiscreteAttribute cimport DiscreteAttribute
from Classification.Classifier.Classifier cimport Classifier
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.InstanceList.Partition cimport Partition
from Classification.Model.NaiveBayesModel cimport NaiveBayesModel
from Classification.Parameter.Parameter cimport Parameter


cdef class NaiveBayes(Classifier):

    cpdef trainContinuousVersion(self,
                                 DiscreteDistribution priorDistribution,
                                 Partition classLists):
        """
        Training algorithm for Naive Bayes algorithm with a continuous data set.

        PARAMETERS
        ----------
        priorDistribution : DiscreteDistribution
            Probability distribution of classes P(C_i)
        classLists : Partition
            Instances are divided into K lists, where each list contains only instances from a single class
        """
        cdef dict class_means, class_deviations
        cdef int i
        cdef str class_label
        cdef Vector average_vector, standard_deviation_vector
        class_means = {}
        class_deviations = {}
        for i in range(classLists.size()):
            class_label = classLists.get(i).getClassLabel()
            average_vector = classLists.get(i).average().toVector()
            class_means[class_label] = average_vector
            standard_deviation_vector = classLists.get(i).standardDeviation().toVector()
            class_deviations[class_label] = standard_deviation_vector
        self.model = NaiveBayesModel(priorDistribution)
        if isinstance(self.model, NaiveBayesModel):
            self.model.initForContinuous(class_means, class_deviations)

    cpdef trainDiscreteVersion(self,
                               DiscreteDistribution priorDistribution,
                               Partition classLists):
        """
        Training algorithm for Naive Bayes algorithm with a discrete data set.

        PARAMETERS
        ----------
        priorDistribution : DiscreteDistribution
            Probability distribution of classes P(C_i)
        classLists : Partition
            Instances are divided into K lists, where each list contains only instances from a single class
        """
        cdef dict class_attribute_distributions
        cdef int i
        class_attribute_distributions = {}
        for i in range(classLists.size()):
            class_attribute_distributions[classLists.get(i).getClassLabel()] = \
                classLists.get(i).allAttributesDistribution()
        self.model = NaiveBayesModel(priorDistribution)
        if isinstance(self.model, NaiveBayesModel):
            self.model.initForDiscrete(class_attribute_distributions)

    cpdef train(self,
                InstanceList trainSet,
                Parameter parameters):
        """
        Training algorithm for Naive Bayes algorithm. It basically calls trainContinuousVersion for continuous data
        sets, trainDiscreteVersion for discrete data sets.

        PARAMETERS
        ----------
        trainSet : InstanceList
            Training data given to the algorithm
        """
        cdef DiscreteDistribution prior_distribution
        cdef Partition class_lists
        prior_distribution = trainSet.classDistribution()
        class_lists = Partition(trainSet)
        if isinstance(class_lists.get(0).get(0).getAttribute(0), DiscreteAttribute):
            self.trainDiscreteVersion(prior_distribution, class_lists)
        else:
            self.trainContinuousVersion(prior_distribution, class_lists)
