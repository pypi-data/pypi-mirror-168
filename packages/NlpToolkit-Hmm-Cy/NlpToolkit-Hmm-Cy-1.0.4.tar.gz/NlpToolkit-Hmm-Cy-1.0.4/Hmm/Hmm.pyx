from DataStructure.CounterHashMap cimport CounterHashMap
from Hmm.HmmState cimport HmmState
import math


cdef class Hmm(object):

    def calculatePi(self, observations: list):
        pass

    def calculateTransitionProbabilities(self, observations: list):
        pass

    def viterbi(self, s: list) -> list:
        pass

    def __init__(self,
                 states: set,
                 observations: list,
                 emittedSymbols: list):
        """
        A constructor of Hmm class which takes a Set of states, an array of observations (which also
        consists of an array of states) and an array of instances (which also consists of an array of emitted symbols).
        The constructor initializes the state array with the set of states and uses observations and emitted symbols
        to calculate the emission probabilities for those states.

        PARAMETERS
        ----------
        states : set
            A Set of states, consisting of all possible states for this problem.
        observations : list
            An array of instances, where each instance consists of an array of states.
        emittedSymbols : list
            An array of instances, where each instance consists of an array of symbols.
        """
        cdef int i
        cdef dict emission_probabilities
        i = 0
        self.state_count = len(states)
        self.states = []
        self.state_indexes = {}
        for state in states:
            self.state_indexes[state] = i
            i = i + 1
        self.calculatePi(observations)
        for state in states:
            emission_probabilities = self.calculateEmissionProbabilities(state, observations, emittedSymbols)
            self.states.append(HmmState(state, emission_probabilities))
        self.calculateTransitionProbabilities(observations)

    cpdef dict calculateEmissionProbabilities(self, object state, list observations, list emittedSymbols):
        """
        calculateEmissionProbabilities calculates the emission probabilities for a specific state. The method takes the
        state, an array of observations (which also consists of an array of states) and an array of instances (which also
        consists of an array of emitted symbols).

        PARAMETERS
        ----------
        states : set
            A Set of states, consisting of all possible states for this problem.
        observations : list
            An array of instances, where each instance consists of an array of states.
        emittedSymbols : list
            An array of instances, where each instance consists of an array of symbols.

        RETURNS
        -------
        dict
            A HashMap. Emission probabilities for a single state. Contains a probability for each symbol emitted.
        """
        cdef CounterHashMap counts
        cdef dict emission_probabilities
        cdef int i, j
        counts = CounterHashMap()
        emission_probabilities = {}
        for i in range(len(observations)):
            for j in range(len(observations[i])):
                current_state = observations[i][j]
                current_symbol = emittedSymbols[i][j]
                if current_state == state:
                    counts.put(current_symbol)
        total = counts.sumOfCounts()
        for symbol in counts:
            emission_probabilities[symbol] = counts[symbol] / total
        return emission_probabilities

    cpdef double safeLog(self, double x):
        """
        safeLog calculates the logarithm of a number. If the number is less than 0, the logarithm is not defined, therefore
        the function returns -Infinity.

        PARAMETERS
        ----------
        x : float
            Input number

        RETURNS
        -------
        float
            The logarithm of x. If x < 0 return -infinity.
        """
        if x <= 0:
            return -1000
        else:
            return math.log(x)

    def __repr__(self):
        return f"{self.transition_probabilities} {self.states}"
