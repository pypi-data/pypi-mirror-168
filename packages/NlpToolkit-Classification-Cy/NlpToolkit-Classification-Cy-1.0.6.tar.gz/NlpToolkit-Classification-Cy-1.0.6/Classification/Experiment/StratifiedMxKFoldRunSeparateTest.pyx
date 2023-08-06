from Sampling.StratifiedKFoldCrossValidation cimport StratifiedKFoldCrossValidation
from Classification.Experiment.Experiment cimport Experiment
from Classification.Experiment.StratifiedKFoldRunSeparateTest cimport StratifiedKFoldRunSeparateTest
from Classification.InstanceList.Partition cimport Partition
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Performance.ExperimentPerformance cimport ExperimentPerformance


cdef class StratifiedMxKFoldRunSeparateTest(StratifiedKFoldRunSeparateTest):

    cdef int M

    def __init__(self,
                 M: int,
                 K: int):
        """
        Constructor for StratifiedMxKFoldRunSeparateTest class. Basically sets K parameter of the K-fold
        cross-validation and M for the number of times.

        PARAMETERS
        ----------
        M : int
            number of cross-validation times.
        K : int
            K of the K-fold cross-validation.
        """
        super().__init__(K)
        self.M = M

    cpdef ExperimentPerformance execute(self, Experiment experiment):
        cdef ExperimentPerformance result
        cdef int j
        cdef InstanceList instance_list
        cdef Partition partition
        cdef StratifiedKFoldCrossValidation crossValidation
        result = ExperimentPerformance()
        for j in range(self.M):
            instance_list = experiment.getDataSet().getInstanceList()
            partition = Partition(instanceList=instance_list,
                                  ratio=0.25,
                                  seed=experiment.getParameter().getSeed(),
                                  stratified=True)
            cross_validation = StratifiedKFoldCrossValidation(instance_lists=Partition(partition.get(1)).getLists(),
                                                             K=self.K,
                                                             seed=experiment.getParameter().getSeed())
            self.runExperimentSeparate(classifier=experiment.getClassifier(),
                               parameter=experiment.getParameter(),
                               experimentPerformance=result,
                               crossValidation=cross_validation,
                               testSet=partition.get(0))
        return result
