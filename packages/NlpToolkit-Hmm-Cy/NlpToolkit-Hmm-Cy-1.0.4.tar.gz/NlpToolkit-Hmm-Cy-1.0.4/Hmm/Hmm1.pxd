from Hmm.Hmm cimport Hmm
from Math.Vector cimport Vector


cdef class Hmm1(Hmm):

    cdef Vector __pi

    cpdef calculatePi(self, list observations)
    cpdef calculateTransitionProbabilities(self, list observations)
    cpdef Vector __logOfColumn(self, int column)
    cpdef list viterbi(self, list s)
