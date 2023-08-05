from Math.Matrix cimport Matrix


cdef class Hmm(object):

    cdef Matrix transition_probabilities
    cdef dict state_indexes
    cdef list states
    cdef int state_count

    cpdef dict calculateEmissionProbabilities(self, object state, list observations, list emittedSymbols)
    cpdef double safeLog(self, double x)
