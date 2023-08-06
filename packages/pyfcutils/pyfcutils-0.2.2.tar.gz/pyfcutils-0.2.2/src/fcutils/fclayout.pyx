cimport cython
cimport fclayout
from libc.stdlib cimport free, malloc


cdef class FCLAYOUT:
    cdef fclayout.FCLayout* s

    def __cinit__(self, pdp_addrs, missing_pixels):
        print("FCLayoutCreate()")
        p_addr = <int *>malloc(len(pdp_addrs)*cython.sizeof(int))
        m_p = <int *>malloc(len(missing_pixels)*cython.sizeof(int))

        for i in xrange(len(pdp_addrs)):
            p_addr[i] = pdp_addrs[i]
        for i in xrange(len(missing_pixels)):
            m_p[i] = missing_pixels[i]
        n_pdps = len(pdp_addrs)
        n_missing = len(missing_pixels)
        self.s = fclayout.FCLayoutCreate(p_addr, n_pdps, m_p, n_missing, CTA_MST_FLASHCAM_PROTOTYPE_LAYOUT)

        free(p_addr)
        free(m_p)

    def __dealloc__(self):
        print("FCLayoutDestroy()")
        fclayout.FCLayoutDestroy(self.s)

    @property
    def npixels(self):
       return self.s.npixels

    @property
    def npatches(self):
       return self.s.npatches

    @property
    def ncables(self):
       return self.s.ncables

    @property
    def npdps(self):
       return self.s.npdps

    @property
    def pixel(self):
       return self.s.pixel

    @property
    def patch(self):
        return self.s.patch

    @property
    def cable(self):
       return self.s.cable
