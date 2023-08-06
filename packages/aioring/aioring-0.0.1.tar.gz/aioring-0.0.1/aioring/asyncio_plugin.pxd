from aioring.ring cimport IoRing


cdef class IoRingAsyncioPlugin:
    cdef public IoRing ring
    cdef public object loop 
    cdef bint close_ring_on_exit
    cdef bint closed

    cdef _hook_close(self)
    cpdef void on_ring_events(self) except *
    cpdef int close(self) except -1
    cpdef object create_future(self)

