cdef extern from "fclayout.h":
  cdef int FCLAYOUT_MAX_PIXELS
  cdef int FCLAYOUT_MAX_PDPS
  cdef int FCLAYOUT_PATCH_SIZE
  cdef int FCLAYOUT_CABLE_SIZE
  cdef int FCLAYOUT_MAX_PATCHES
  cdef int FCLAYOUT_MAX_CABLES
  cdef int QRAXISSIZE
  cdef int QROFFSET

  ctypedef enum FCLayoutType:
    UNKNOWN_CAMERA_LAYOUT = 0,
    CTA_MST_FLASHCAM_PROTOTYPE_LAYOUT = 1

  ctypedef struct FCPixel:
    int pixel_no
    int sector_no
    int crate_no
    int pdp_addr
    int pdp_chan
    int pdp_gchan
    int fadc_addr
    int fadc_chan
    int trigger_addr
    int three_pixel_patch
    int four_pixel_patch
    int trace_idx
    int has_pixel
    int ring
    double pixel_x
    double pixel_y
    double pixel_w
    double pixel_q
    double pixel_r
    int pdp_board_rev
    int pixel_dynodes
    double pixel_hv_offset
    double pixel_hv_setpoint
    double pixel_gain_exponent
    int pixel_preamp_gain

  ctypedef struct FCPatch:
    int patch_no
    int npixels
    int trigger_trace_idx
    int fadc_addr
    int trigger_addr
    int pdp_addr
    int sector_no
    double patch_x
    double patch_y
    double patch_q
    double patch_r
    # FCPixel* pixel[3]
    # FCPatch* neighbours[6]

  ctypedef struct FCCable:
    int cable_no
    int npixels
    int fadc_addr
    int trigger_addr
    int pdp_addr
    int sector_no
    # FCPixel* pixel[4]

  ctypedef struct FCLayout:
    FCLayoutType type
    int npixels
    int npatches
    int ncables
    int npdps
    FCPixel pixel[2304]
    FCPatch patch[768]
    FCCable cable[576]

  cdef FCLayout *FCLayoutCreate(int *pdp_addrs, int n_pdps, int *missing_pixels,
                                int n_missing, FCLayoutType type)
  cdef void FCLayoutDestroy(FCLayout *layout)
