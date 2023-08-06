from Sampling.CrossValidation cimport CrossValidation
from Sampling.KFoldCrossValidation cimport KFoldCrossValidation
from Classification.Classifier.Classifier cimport Classifier
from Classification.Experiment.Experiment cimport Experiment
from Classification.Experiment.SingleRun cimport SingleRun
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Parameter.Parameter cimport Parameter
from Classification.Performance.Performance cimport Performance


cdef class SingleRunWithK(SingleRun):

    cdef int __K

    def __init__(self, K: int):
        """
        Constructor for SingleRunWithK class. Basically sets K parameter of the K-fold cross-validation.

        PARAMETERS
        ----------
        K : int
            K of the K-fold cross-validation.
        """
        self.__K = K

    cpdef runExperiment(self,
                        Classifier classifier,
                        Parameter parameter,
                        CrossValidation crossValidation):
        cdef InstanceList train_set, test_set
        train_set = InstanceList(crossValidation.getTrainFold(0))
        test_set = InstanceList(crossValidation.getTestFold(0))
        return classifier.singleRun(parameter=parameter,
                                    trainSet=train_set,
                                    testSet=test_set)

    cpdef Performance execute(self, Experiment experiment):
        """
        Execute Single K-fold cross-validation with the given classifier on the given data set using the given
        parameters.

        PARAMETERS
        -----
        experiment : Experiment
            Experiment to be run.

        RETURNS
        -------
        Performance
            A Performance instance.
        """
        cdef KFoldCrossValidation crossValidation
        cross_validation = KFoldCrossValidation(instance_list=experiment.getDataSet().getInstances(),
                                               K=self.__K,
                                               seed=experiment.getParameter().getSeed())
        return self.runExperiment(classifier=experiment.getClassifier(),
                                  parameter=experiment.getParameter(),
                                  crossValidation=cross_validation)
