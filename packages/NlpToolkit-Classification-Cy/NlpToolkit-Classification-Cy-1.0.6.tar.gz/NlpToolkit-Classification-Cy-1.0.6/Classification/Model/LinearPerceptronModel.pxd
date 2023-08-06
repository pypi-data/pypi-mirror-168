from Math.Matrix cimport Matrix
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Model.NeuralNetworkModel cimport NeuralNetworkModel


cdef class LinearPerceptronModel(NeuralNetworkModel):

    cdef Matrix W

    cpdef initWithTrainSet(self, InstanceList trainSet)
    cpdef calculateOutput(self)
