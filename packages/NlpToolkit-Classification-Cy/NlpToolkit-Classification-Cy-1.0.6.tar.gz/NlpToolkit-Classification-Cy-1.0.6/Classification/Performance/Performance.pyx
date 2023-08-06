cdef class Performance(object):

    def __init__(self, errorRate: float):
        """
        Constructor that sets the error rate.

        PARAMETERS
        ----------
        errorRate : float
            Double input.
        """
        self.error_rate = errorRate

    cpdef double getErrorRate(self):
        """
        Accessor for the error rate.

        RETURNS
        -------
        float
            Double errorRate.
        """
        return self.error_rate
