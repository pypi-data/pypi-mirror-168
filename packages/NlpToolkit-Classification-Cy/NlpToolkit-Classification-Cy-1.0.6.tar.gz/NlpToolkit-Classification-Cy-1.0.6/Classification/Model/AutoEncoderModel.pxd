from Math.Matrix cimport Matrix
from Math.Vector cimport Vector
from Classification.Instance.Instance cimport Instance
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Model.NeuralNetworkModel cimport NeuralNetworkModel
from Classification.Performance.Performance cimport Performance


cdef class AutoEncoderModel(NeuralNetworkModel):

    cdef Matrix __V
    cdef Matrix __W

    cpdef __allocateWeights(self, int H, int seed)
    cpdef Performance testAutoEncoder(self, InstanceList data)
    cpdef Vector __predictInput(self, Instance instance)
    cpdef calculateOutput(self)
