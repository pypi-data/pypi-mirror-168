from Sampling.KFoldCrossValidation cimport KFoldCrossValidation
from Classification.InstanceList.InstanceList cimport InstanceList


cdef class KFoldRun(MultipleRun):

    def __init__(self, K: int):
        """
        Constructor for KFoldRun class. Basically sets K parameter of the K-fold cross-validation.

        PARAMETERS
        ----------
        K : int
            K of the K-fold cross-validation.
        """
        self.K = K

    cpdef runExperiment(self,
                        Classifier classifier,
                        Parameter parameter,
                        ExperimentPerformance experimentPerformance,
                        CrossValidation crossValidation):
        cdef int i
        cdef InstanceList train_set, test_set
        for i in range(self.K):
            train_set = InstanceList(crossValidation.getTrainFold(i))
            test_set = InstanceList(crossValidation.getTestFold(i))
            classifier.train(train_set, parameter)
            experimentPerformance.add(classifier.test(test_set))

    cpdef ExperimentPerformance execute(self, Experiment experiment):
        """
        Execute K-fold cross-validation with the given classifier on the given data set using the given parameters.

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
        cdef KFoldCrossValidation crossValidation
        result = ExperimentPerformance()
        crossValidation = KFoldCrossValidation(instance_list=experiment.getDataSet().getInstances(),
                                               K=self.K,
                                               seed=experiment.getParameter().getSeed())
        self.runExperiment(classifier=experiment.getClassifier(),
                           parameter=experiment.getParameter(),
                           experimentPerformance=result,
                           crossValidation=crossValidation)
        return result
