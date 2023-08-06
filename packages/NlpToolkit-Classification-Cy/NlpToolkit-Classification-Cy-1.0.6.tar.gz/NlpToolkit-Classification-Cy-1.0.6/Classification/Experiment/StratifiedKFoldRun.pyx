from Sampling.StratifiedKFoldCrossValidation cimport StratifiedKFoldCrossValidation
from Classification.Experiment.Experiment cimport Experiment
from Classification.Experiment.KFoldRun cimport KFoldRun
from Classification.Performance.ExperimentPerformance cimport ExperimentPerformance


cdef class StratifiedKFoldRun(KFoldRun):

    def __init__(self, K: int):
        """
        Constructor for KFoldRun class. Basically sets K parameter of the K-fold cross-validation.

        PARAMETERS
        ----------
        K : int
            K of the K-fold cross-validation.
        """
        super().__init__(K)

    cpdef ExperimentPerformance execute(self, Experiment experiment):
        """
        Execute Stratified K-fold cross-validation with the given classifier on the given data set using the given
        parameters.

        PARAMETERS
        ----------
        experiment : Experiment
            Experiment to be run.

        RETURNS
        -------
        ExperimentPerformance
            An ExperimentPerformance instance.
        """
        cdef ExperimentPerformance result
        cdef StratifiedKFoldCrossValidation cross_validation
        result = ExperimentPerformance()
        cross_validation = StratifiedKFoldCrossValidation(instance_lists=experiment.getDataSet().getClassInstances(),
                                                         K=self.K,
                                                         seed=experiment.getParameter().getSeed())
        self.runExperiment(classifier=experiment.getClassifier(),
                           parameter=experiment.getParameter(),
                           experimentPerformance=result,
                           crossValidation=cross_validation)
        return result
