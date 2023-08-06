from Classification.Model.NeuralNetworkModel cimport NeuralNetworkModel
from Classification.Parameter.DeepNetworkParameter cimport DeepNetworkParameter


cdef class DeepNetworkModel(NeuralNetworkModel):

    cdef list __weights
    cdef int __hidden_layer_size
    cdef object __activation_function

    cpdef __allocateWeights(self, DeepNetworkParameter parameters)
    cpdef list __setBestWeights(self)
    cpdef calculateOutput(self)
