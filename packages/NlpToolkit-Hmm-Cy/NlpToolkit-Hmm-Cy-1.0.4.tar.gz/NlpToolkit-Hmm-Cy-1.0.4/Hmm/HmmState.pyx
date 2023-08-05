cdef class HmmState(object):

    def __init__(self,
                 state: object,
                 emissionProbabilities: dict):
        """
        A constructor of HmmState class which takes a State and emission probabilities as inputs and
        initializes corresponding class variable with these inputs.

        PARAMETERS
        ----------
        state : object
            Data for this state.
        emissionProbabilities : dict
            Emission probabilities for this state
        """
        self.state = state
        self.emission_probabilities = emissionProbabilities

    cpdef object getState(self):
        """
        Accessor method for the state variable.

        RETURNS
        -------
        object
            state variable.
        """
        return self.state

    cpdef double getEmitProb(self, object symbol):
        """
        getEmitProb method returns the emission probability for a specific symbol.

        PARAMETERS
        ----------
        symbol : object
            Symbol for which the emission probability will be get.

        RETURNS
        -------
        float
            Emission probability for a specific symbol.
        """
        if symbol in self.emission_probabilities:
            return self.emission_probabilities[symbol]
        else:
            return 0.0

    def __repr__(self):
        return f"{self.state} {self.emission_probabilities}"
