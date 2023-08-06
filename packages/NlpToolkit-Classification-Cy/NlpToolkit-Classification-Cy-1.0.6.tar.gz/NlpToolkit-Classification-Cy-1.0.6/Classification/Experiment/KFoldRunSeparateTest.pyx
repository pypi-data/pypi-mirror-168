from Sampling.KFoldCrossValidation cimport KFoldCrossValidation
from Classification.InstanceList.Partition cimport Partition


cdef class KFoldRunSeparateTest(KFoldRun):

    def __init__(self, K: int):
        """
        Constructor for KFoldRunSeparateTest class. Basically sets K parameter of the K-fold cross-validation.

        PARAMETERS
        ----------
        K : int
            K of the K-fold cross-validation.
        """
        super().__init__(K)

    cpdef runExperimentSeparate(self,
                                Classifier classifier,
                                Parameter parameter,
                                ExperimentPerformance experimentPerformance,
                                CrossValidation crossValidation,
                                InstanceList testSet):
        cdef int i
        cdef InstanceList train_set
        for i in range(self.K):
            train_set = InstanceList(crossValidation.getTrainFold(i))
            classifier.train(train_set, parameter)
            experimentPerformance.add(classifier.test(testSet))

    cpdef ExperimentPerformance execute(self, Experiment experiment):
        """
        Execute K-fold cross-validation with separate test set with the given classifier on the given data set using the
        given parameters.

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
        cdef InstanceList instance_list
        cdef Partition partition
        cdef KFoldCrossValidation cross_validation
        result = ExperimentPerformance()
        instance_list = experiment.getDataSet().getInstanceList()
        partition = Partition(instanceList=instance_list,
                              ratio=0.25,
                              seed=experiment.getParameter().getSeed(),
                              stratified=True)
        cross_validation = KFoldCrossValidation(instance_list=partition.get(1).getInstances(),
                                               K=self.K,
                                               seed=experiment.getParameter().getSeed())
        self.runExperimentSeparate(classifier=experiment.getClassifier(),
                           parameter=experiment.getParameter(),
                           experimentPerformance=result,
                           crossValidation=cross_validation,
                           testSet=partition.get(0))
        return result
