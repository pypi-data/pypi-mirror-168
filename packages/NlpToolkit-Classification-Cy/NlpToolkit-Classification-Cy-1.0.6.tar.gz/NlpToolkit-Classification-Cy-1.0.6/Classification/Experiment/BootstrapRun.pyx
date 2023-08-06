from Classification.Experiment.MultipleRun cimport MultipleRun
from Classification.Experiment.Experiment cimport Experiment
from Classification.Performance.ExperimentPerformance cimport ExperimentPerformance
from Sampling.Bootstrap cimport Bootstrap
from Classification.InstanceList.InstanceList cimport InstanceList


cdef class BootstrapRun(MultipleRun):

    cdef int __numberOfBootstraps

    def __init__(self, numberOfBootstraps: int):
        """
        Constructor for BootstrapRun class. Basically sets the number of bootstrap runs.

        PARAMETERS
        ----------
        numberOfBootstraps : int
            Number of bootstrap runs.
        """
        self.__numberOfBootstraps = numberOfBootstraps

    cpdef ExperimentPerformance execute(self, Experiment experiment):
        """
        Execute the bootstrap run with the given classifier on the given data set using the given parameters.

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
        cdef int i
        cdef Bootstrap bootstrap
        cdef InstanceList bootstrapSample
        result = ExperimentPerformance()
        for i in range(self.__numberOfBootstraps):
            bootstrap = Bootstrap(instance_list=experiment.getDataSet().getInstances(),
                                  seed=i + experiment.getParameter().getSeed())
            bootstrap_sample = InstanceList(bootstrap.getSample())
            experiment.getClassifier().train(trainSet=bootstrap_sample,
                                             parameters=experiment.getParameter())
            result.add(experiment.getClassifier().test(experiment.getDataSet().getInstanceList()))
        return result
