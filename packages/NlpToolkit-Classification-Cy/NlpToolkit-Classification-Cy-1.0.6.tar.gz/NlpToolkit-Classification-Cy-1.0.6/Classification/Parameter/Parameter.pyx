cdef class Parameter(object):

    def __init__(self, seed: int):
        """
        Constructor of Parameter class which assigns given seed value to seed.

        PARAMETERS
        ----------
        seed : int
            Seed is used for random number generation.
        """
        self.seed = seed

    cpdef int getSeed(self):
        """
        Accessor for the seed.

        RETURNS
        -------
        int
            The seed.
        """
        return self.seed
