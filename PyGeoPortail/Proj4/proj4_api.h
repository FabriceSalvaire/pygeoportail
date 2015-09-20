/***************************************************************************************************
 *
 * PROJ.4 API 480
 *
 **************************************************************************************************/

char * get_pj_release();
int get_errno();

/**************************************************************************************************/

typedef struct { double u, v; } projUV;
typedef void *projPJ;
typedef projUV projXY;
typedef projUV projLP;
typedef void *projCtx;

/**************************************************************************************************/

void pj_fwd_(projLP *in, projPJ proj, projXY *out);
void pj_inv_(projLP *in, projPJ proj, projXY *out);

// projXY pj_fwd(projLP, projPJ);
// projLP pj_inv(projXY, projPJ);

int pj_transform(projPJ src, projPJ dst,
		 long point_count, int point_offset,
		 double *x, double *y, double *z);
int pj_datum_transform(projPJ src, projPJ dst,
		       long point_count, int point_offset,
		       double *x, double *y, double *z);
int pj_geocentric_to_geodetic(double a, double es,
			      long point_count, int point_offset,
			      double *x, double *y, double *z);
int pj_geodetic_to_geocentric(double a, double es,
			      long point_count, int point_offset,
			      double *x, double *y, double *z);
int pj_compare_datums(projPJ srcdefn, projPJ dstdefn);
int pj_apply_gridshift(projCtx, const char *, int,
		       long point_count, int point_offset,
		       double *x, double *y, double *z);
void pj_deallocate_grids(void);
void pj_clear_initcache(void);
int pj_is_latlong(projPJ);
int pj_is_geocent(projPJ);
void pj_get_spheroid_defn(projPJ defn, double *major_axis, double *eccentricity_squared);
void pj_pr_list(projPJ);
void pj_free(projPJ);
void pj_set_finder(const char *(*)(const char *));
void pj_set_searchpath (int count, const char **path);
projPJ pj_init(int, char **);
projPJ pj_init_plus(const char *);
projPJ pj_init_ctx(projCtx, int, char **);
projPJ pj_init_plus_ctx(projCtx, const char *);
char *pj_get_def(projPJ, int);
projPJ pj_latlong_from_proj(projPJ);
void *pj_malloc(size_t);
void pj_dalloc(void *);
char *pj_strerrno(int);
int *pj_get_errno_ref(void);
const char *pj_get_release(void);
void pj_acquire_lock(void);
void pj_release_lock(void);
void pj_cleanup_lock(void);

projCtx pj_get_default_ctx(void);
projCtx pj_get_ctx(projPJ);
void pj_set_ctx(projPJ, projCtx);
projCtx pj_ctx_alloc(void);
void pj_ctx_free(projCtx);
int pj_ctx_get_errno(projCtx);
void pj_ctx_set_errno(projCtx, int);
void pj_ctx_set_debug(projCtx, int);
void pj_ctx_set_logger(projCtx, void (*)(void *, int, const char *));
void pj_ctx_set_app_data(projCtx, void *);
void *pj_ctx_get_app_data(projCtx);

void pj_log(projCtx ctx, int level, const char *fmt, ...);
void pj_stderr_logger(void *, int, const char *);

/***************************************************************************************************
 *
 * End
 *
 **************************************************************************************************/
