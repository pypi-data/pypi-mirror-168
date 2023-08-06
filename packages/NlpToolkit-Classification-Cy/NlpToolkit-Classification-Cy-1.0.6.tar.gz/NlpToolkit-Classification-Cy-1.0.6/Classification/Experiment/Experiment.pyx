cdef class Experiment(object):

    def __init__(self,
                 classifier: Classifier,
                 parameter: Parameter,
                 dataSet: DataSet):
        """
        Constructor for a specific machine learning experiment

        PARAMETERS
        ----------
        classifier : Classifier
            Classifier used in the machine learning experiment
        parameter : Parameter
            Parameter(s) of the classifier.
        dataSet : DataSet
            DataSet on which the classifier is run.
        """
        self.__classifier = classifier
        self.__parameter = parameter
        self.__dataSet = dataSet

    cpdef Classifier getClassifier(self):
        """
        Accessor for the classifier attribute.

        RETURNS
        -------
        Classifier
            Classifier attribute.
        """
        return self.__classifier

    cpdef Parameter getParameter(self):
        """
        Accessor for the parameter attribute.

        RETURNS
        -------
        Parameter
            Parameter attribute.
        """
        return self.__parameter

    cpdef DataSet getDataSet(self):
        """
        Accessor for the dataSet attribute.

        RETURNS
        -------
        DataSet
            DataSet attribute.
        """
        return self.__dataSet

    cpdef Experiment featureSelectedExperiment(self, FeatureSubSet featureSubSet):
        """
        Construct and returns a feature selection experiment.

        PARAMETERS
        ----------
        featureSubSet : FeatureSubSet
            Feature subset used in the feature selection experiment

        RETURNS
        -------
        Experiment
            Experiment constructed
        """
        return Experiment(classifier=self.__classifier,
                          parameter=self.__parameter,
                          dataSet=self.__dataSet.getSubSetOfFeatures(featureSubSet))
