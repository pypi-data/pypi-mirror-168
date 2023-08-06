
/*========================================================//
date:    Mi 6. Jun 16:29:03 CEST 2018
sources: Libs-fc/fclayout/fclayout.c
//========================================================*/
#ifndef INCLUDED_fclayout_h
#define INCLUDED_fclayout_h

#ifdef __cplusplus
extern "C" {
#endif  // __cplusplus
#if !defined(MAX)
#define MAX(a, b) (((a) > (b)) ? (a) : (b))
#endif

#define FCLAYOUT_MAX_PIXELS 2304
#define FCLAYOUT_MAX_PDPS 192
#define FCLAYOUT_PATCH_SIZE 3
#define FCLAYOUT_CABLE_SIZE 4
#define FCLAYOUT_MAX_PATCHES 2304 / FCLAYOUT_PATCH_SIZE
#define FCLAYOUT_MAX_CABLES 2304 / FCLAYOUT_CABLE_SIZE
#define QRAXISSIZE 65
#define QROFFSET 32
#if FCLAYOUT_PATCH_SIZE != 3
  #error FCLAYOUT_PATCH_SIZE has to be 3.
#endif
#if FCLAYOUT_CABLE_SIZE != 4
  #error FCLAYOUT_CABLE_SIZE has to be 4.
#endif
typedef enum {
  UNKNOWN_CAMERA_LAYOUT = 0,
  CTA_MST_FLASHCAM_PROTOTYPE_LAYOUT = 1
} FCLayoutType;

typedef struct FCqrmap {
  int offset;
  int pixel_idx[QRAXISSIZE][QRAXISSIZE];
} FCqrmap;
typedef struct FCPixel {
  int pixel_no;  // (pdp_addr << 4) + (fadc_chan % 12)
  int sector_no;  // 0...2
  int crate_no;  // 0...5
  int pdp_addr;  // address of PDP board (0x10...0xcf)
  int pdp_chan;  // channel on PDP board (0...11)
  int pdp_gchan;  // global PDP channel (for use with pdpctl)
  int fadc_addr;  // address of connected FADC board (0x11, 0x12, ...)
  int fadc_chan;  // channel on FADC board (0...23)
  int trigger_addr;  // address of responsible trigger board (0x10, 0x20, ...)
  int three_pixel_patch;  // local three pixel patch (0...7) (numbered per fadc)
  int four_pixel_patch;  // local four pixel patch (0...2) (numbered per pdp)
  int trace_idx;  // index of corresponding trace in trace array (0...2303)
  int has_pixel;  // pixel is present (0: unconnected FADC)
  int ring;  // distance from centre of PDP
  double pixel_x;  // x coordinate in mm
  double pixel_y;  // y coordinate in mm
  double pixel_w;  // flat-to-flat width in mm
  double pixel_q;
  double pixel_r;
  int pdp_board_rev;
  int pixel_dynodes;
  double pixel_hv_offset;
  double pixel_hv_setpoint;
  double pixel_gain_exponent;
  int pixel_preamp_gain;
} FCPixel;
typedef struct FCPatch {
  int patch_no;
  int npixels;
  int trigger_trace_idx;
  int fadc_addr;
  int trigger_addr;
  int pdp_addr;
  int sector_no;
  double patch_x;
  double patch_y;
  double patch_q;
  double patch_r;
  FCPixel* pixel[FCLAYOUT_PATCH_SIZE];
  struct FCPatch* neighbours[6];
} FCPatch;
typedef struct FCCable {
  int cable_no;
  int npixels;
  int fadc_addr;
  int trigger_addr;
  int pdp_addr;
  int sector_no;
  FCPixel* pixel[FCLAYOUT_CABLE_SIZE];
} FCCable;
typedef struct FCLayout {
  FCLayoutType type;
  int npixels;
  int npatches;
  int ncables;
  int npdps;
  FCPixel pixel[FCLAYOUT_MAX_PIXELS];
  FCPatch patch[FCLAYOUT_MAX_PATCHES];
  FCCable cable[FCLAYOUT_MAX_CABLES];
  FCqrmap map;
} FCLayout;

void FCNeighbourPatches(FCqrmap* map, FCPatch* patch, int optflag, int (*result)[FCLAYOUT_PATCH_SIZE])
;
int FCNeighbourPixels(FCLayout* layout, FCPixel* pixel, FCPixel *neighbours[6])
;
FCLayout *FCLayoutCreate(int *pdp_addrs, int n_pdps, int *missing_pixels,
                         int n_missing, FCLayoutType type)
;
void FCLayoutDestroy(FCLayout *layout)
;
int FCLayoutGetPDPAddresses(FCLayout *layout, int **pdp_addrs)
;
#ifdef __cplusplus
}
#endif  // __cplusplus

#endif
