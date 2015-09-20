/***************************************************************************************************
 *
 * PROJ.4 Helper
 *
 **************************************************************************************************/

#include <proj_api.h>

static char * get_pj_release() {
return pj_release;
}

static int get_errno() {
return pj_errno;
}

static void pj_fwd_(projLP *in, projPJ proj, projXY *out) {
  *out = pj_fwd(*in, proj);
}

static void pj_inv_(projLP *in, projPJ proj, projXY *out) {
  *out = pj_inv(*in, proj);
}

/***************************************************************************************************
 *
 * End
 *
 **************************************************************************************************/
