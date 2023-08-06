#define GSL_DISABLE_DEPRECATED 1
#define HAVE_DECL_ACOSH 1
#define HAVE_DECL_ASINH 1
#define HAVE_DECL_ATANH 1
#define HAVE_DECL_EXPM1 1
#define HAVE_DECL_FEENABLEEXCEPT 0
#define HAVE_DECL_FESETTRAPENABLE 0
#define HAVE_DECL_FINITE 1
#define HAVE_DECL_FREXP 1
#define HAVE_DECL_HYPOT 1
#define HAVE_DECL_ISFINITE 1
#define HAVE_DECL_ISINF 1
#define HAVE_DECL_ISNAN 1
#define HAVE_DECL_LDEXP 1
#define HAVE_DECL_LOG1P 1
#define HAVE_DLFCN_H 1
#define HAVE_EXIT_SUCCESS_AND_FAILURE 1
#define HAVE_EXTENDED_PRECISION_REGISTERS 1
#define HAVE_INTTYPES_H 1
#define HAVE_LIBM 1
#define HAVE_MEMCPY 1
#define HAVE_MEMMOVE 1
#define HAVE_MEMORY_H 1
#define HAVE_PRINTF_LONGDOUBLE 1
#define HAVE_STDINT_H 1
#define HAVE_STDLIB_H 1
#define HAVE_STRDUP 1
#define HAVE_STRINGS_H 1
#define HAVE_STRING_H 1
#define HAVE_STRTOL 1
#define HAVE_STRTOUL 1
#define HAVE_SYS_STAT_H 1
#define HAVE_SYS_TYPES_H 1
#define HAVE_UNISTD_H 1
#define HAVE_VPRINTF 1
#define LT_OBJDIR ".libs/"
#define PACKAGE "gsl"
#define PACKAGE_BUGREPORT ""
#define PACKAGE_NAME "gsl"
#define PACKAGE_STRING "gsl 1.11"
#define PACKAGE_TARNAME "gsl"
#define PACKAGE_VERSION "1.11"
#define RELEASED
#define STDC_HEADERS 1
#define VERSION "1.11"
#if !HAVE_EXIT_SUCCESS_AND_FAILURE
#define EXIT_SUCCESS 0
#define EXIT_FAILURE 1
#endif
#if HAVE_EXTENDED_PRECISION_REGISTERS
#define GSL_COERCE_DBL(x) (gsl_coerce_double(x))
#else
#define GSL_COERCE_DBL(x) (x)
#endif
#if !HAVE_DECL_HYPOT
#define hypot gsl_hypot
#endif
#if !HAVE_DECL_LOG1P
#define log1p gsl_log1p
#endif
#if !HAVE_DECL_EXPM1
#define expm1 gsl_expm1
#endif
#if !HAVE_DECL_ACOSH
#define acosh gsl_acosh
#endif
#if !HAVE_DECL_ASINH
#define asinh gsl_asinh
#endif
#if !HAVE_DECL_ATANH
#define atanh gsl_atanh
#endif
#if !HAVE_DECL_LDEXP
#define ldexp gsl_ldexp
#endif
#if !HAVE_DECL_FREXP
#define frexp gsl_frexp
#endif
#if !HAVE_DECL_ISINF
#define isinf gsl_isinf
#endif
#if !HAVE_DECL_ISFINITE
#define isfinite gsl_finite
#endif
#if !HAVE_DECL_FINITE
#define finite gsl_finite
#endif
#if !HAVE_DECL_ISNAN
#define isnan gsl_isnan
#endif
#ifdef __GNUC__
#define DISCARD_POINTER(p) do { ; } while(p ? 0 : 0);
#else
#define DISCARD_POINTER(p)
#endif
#if defined(GSL_RANGE_CHECK_OFF) || !defined(GSL_RANGE_CHECK)
#define GSL_RANGE_CHECK 0
#endif
#define RETURN_IF_NULL(x) if (!x) { return ; }
