from Sampling.StratifiedKFoldCrossValidation cimport StratifiedKFoldCrossValidation
from Classification.Experiment.Experiment cimport Experiment
from Classification.Experiment.MxKFoldRun cimport MxKFoldRun
from Classification.Performance.ExperimentPerformance cimport ExperimentPerformance


cdef class StratifiedMxKFoldRun(MxKFoldRun):

    def __init__(self,
                 M: int,
                 K: int):
        """
        Constructor for StratifiedMxKFoldRun class. Basically sets K parameter of the K-fold cross-validation and M for
        the number of times.

        PARAMETERS
        ----------
        M : int
            number of cross-validation times.
        K : int
            K of the K-fold cross-validation.
        """
        super().__init__(M, K)

    cpdef ExperimentPerformance execute(self, Experiment experiment):
        """
        Execute the Stratified MxK-fold cross-validation with the given classifier on the given data set using the given
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
        cdef int j
        cdef StratifiedKFoldCrossValidation cross_validation
        result = ExperimentPerformance()
        for j in range(self.M):
            cross_validation = StratifiedKFoldCrossValidation(instance_lists=experiment.getDataSet().getClassInstances(),
                                                             K=self.K,
                                                             seed=experiment.getParameter().getSeed())
            self.runExperiment(classifier=experiment.getClassifier(),
                               parameter=experiment.getParameter(),
                               experimentPerformance=result,
                               crossValidation=cross_validation)
        return result
