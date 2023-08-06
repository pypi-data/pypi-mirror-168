from Classification.Attribute.DiscreteAttribute cimport DiscreteAttribute
from Classification.Attribute.DiscreteIndexedAttribute cimport DiscreteIndexedAttribute
from Classification.Performance.ConfusionMatrix cimport ConfusionMatrix
from Classification.Performance.DetailedClassificationPerformance cimport DetailedClassificationPerformance


cdef class Classifier(object):

    cpdef train(self,
                InstanceList trainSet,
                Parameter parameters):
        pass

    cpdef bint discreteCheck(self, Instance instance):
        """
        Checks given instance's attribute and returns true if it is a discrete indexed attribute, false otherwise.

        PARAMETERS
        ----------
        instance Instance to check.

        RETURNS
        -------
        bool
            True if instance is a discrete indexed attribute, false otherwise.
        """
        cdef int i
        for i in range(instance.attributeSize()):
            if isinstance(instance.getAttribute(i), DiscreteAttribute) and not isinstance(instance.getAttribute(i),
                                                                                          DiscreteIndexedAttribute):
                return False
        return True

    cpdef Performance test(self, InstanceList testSet):
        """
        TestClassification an instance list with the current model.

        PARAMETERS
        ----------
        testSet : InstaceList
            Test data (list of instances) to be tested.

        RETURNS
        -------
        Performance
            The accuracy (and error) of the model as an instance of Performance class.
        """
        cdef list class_labels
        cdef ConfusionMatrix confusion
        cdef int i
        cdef Instance instance
        class_labels = testSet.getUnionOfPossibleClassLabels()
        confusion = ConfusionMatrix(class_labels)
        for i in range(testSet.size()):
            instance = testSet.get(i)
            confusion.classify(instance.getClassLabel(), self.model.predict(instance))
        return DetailedClassificationPerformance(confusion)

    cpdef Performance singleRun(self,
                                Parameter parameter,
                                InstanceList trainSet,
                                InstanceList testSet):
        """
        Runs current classifier with the given train and test data.

        PARAMETERS
        ----------
        parameter : Parameter
            Parameter of the classifier to be trained.
        trainSet : InstanceList
            Training data to be used in training the classifier.
        testSet : InstanceList
            Test data to be tested after training the model.

        RETURNS
        -------
        Performance
            The accuracy (and error) of the trained model as an instance of Performance class.
        """
        self.train(trainSet, parameter)
        return self.test(testSet)

    cpdef Model getModel(self):
        """
        Accessor for the model.

        RETURNS
        -------
        Model
            Model.
        """
        return self.model
