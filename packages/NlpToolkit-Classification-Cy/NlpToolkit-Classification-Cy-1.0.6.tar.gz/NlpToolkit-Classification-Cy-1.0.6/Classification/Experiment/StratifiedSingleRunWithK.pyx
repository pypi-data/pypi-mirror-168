from Sampling.StratifiedKFoldCrossValidation cimport StratifiedKFoldCrossValidation
from Classification.Experiment.Experiment cimport Experiment
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Performance.Performance cimport Performance


cdef class StratifiedSingleRunWithK:

    cdef int __K

    def __init__(self, K: int):
        """
        Constructor for StratifiedSingleRunWithK class. Basically sets K parameter of the K-fold cross-validation.

        PARAMETERS
        ----------
        K : int
            K of the K-fold cross-validation.
        """
        self.__K = K

    cpdef Performance execute(self, Experiment experiment):
        """
        Execute Stratified Single K-fold cross-validation with the given classifier on the given data set using the
        given parameters.

        PARAMETERS
        ----------
        experiment : Experiment
            Experiment to be run.

        RETURNS
        -------
        Performance
            A Performance instance.
        """
        cdef StratifiedKFoldCrossValidation cross_validation
        cdef InstanceList train_set, test_set
        cross_validation = StratifiedKFoldCrossValidation(instance_lists=experiment.getDataSet().getClassInstances(),
                                                         K=self.__K,
                                                         seed=experiment.getParameter().getSeed())
        train_set = InstanceList(cross_validation.getTrainFold(0))
        test_set = InstanceList(cross_validation.getTestFold(0))
        return experiment.getClassifier().singleRun(parameter=experiment.getParameter(),
                                                    trainSet=train_set,
                                                    testSet=test_set)
