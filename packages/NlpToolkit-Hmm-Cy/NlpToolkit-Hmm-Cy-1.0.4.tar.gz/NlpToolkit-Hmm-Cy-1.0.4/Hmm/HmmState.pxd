cdef class HmmState(object):

    cdef dict emission_probabilities
    cdef object state

    cpdef object getState(self)
    cpdef double getEmitProb(self, object symbol)