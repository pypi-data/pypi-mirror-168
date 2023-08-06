from Classification.Classifier.Classifier cimport Classifier
from Classification.FeatureSelection.FeatureSubSet cimport FeatureSubSet
from Classification.Parameter.Parameter cimport Parameter
from Classification.DataSet.DataSet cimport DataSet


cdef class Experiment(object):

    cdef Classifier __classifier
    cdef Parameter __parameter
    cdef DataSet __dataSet

    cpdef Classifier getClassifier(self)
    cpdef Parameter getParameter(self)
    cpdef DataSet getDataSet(self)
    cpdef Experiment featureSelectedExperiment(self, FeatureSubSet featureSubSet)
