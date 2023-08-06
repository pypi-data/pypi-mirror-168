from Math.DiscreteDistribution cimport DiscreteDistribution
from Math.Vector cimport Vector
from Math.Matrix cimport Matrix


cdef class QdaModel(GaussianModel):

    def __init__(self,
                 priorDistribution: DiscreteDistribution,
                 W: dict,
                 w: dict,
                 w0: dict):
        """
        A constructor which sets the priorDistribution, w and w0 and dictionary of String Matrix according to given
        inputs.

        PARAMETERS
        ----------
        priorDistribution : DiscreteDistribution
            DiscreteDistribution input.
        W :
            Dict of String and Matrix.
        w : dict
            Dict of String and Vectors.
        w0 : dict
            Dict of String and float.
        """
        self.prior_distribution = priorDistribution
        self.__W = W
        self.w = w
        self.w0 = w0

    cpdef double calculateMetric(self,
                                 Instance instance,
                                 str Ci):
        """
        The calculateMetric method takes an Instance and a String as inputs. It multiplies Matrix Wi with Vector xi
        then calculates the dot product of it with xi. Then, again it finds the dot product of wi and xi and returns the
        summation with w0i.

        PARAMETERS
        ----------
        instance : Instance
            Instance input.
        Ci : str
            String input.

        RETURNS
        -------
        float
            The result of Wi.multiplyWithVectorFromLeft(xi).dotProduct(xi) + wi.dotProduct(xi) + w0i.
        """
        cdef Vector xi, wi
        cdef double w0i
        cdef Matrix Wi
        xi = instance.toVector()
        Wi = self.__W[Ci]
        wi = self.w[Ci]
        w0i = self.w0[Ci]
        return Wi.multiplyWithVectorFromLeft(xi).dotProduct(xi) + wi.dotProduct(xi) + w0i
