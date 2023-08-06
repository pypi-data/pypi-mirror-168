/*
    Copyright (c) 2022 Advanced Micro Devices, Inc. All rights reserved.
*/

#ifndef ROCM_SYMLINK_ROCRAND_SOBOL64_H
#define ROCM_SYMLINK_ROCRAND_SOBOL64_H

#if defined(ROCM_NO_WRAPPER_HEADER_WARNING) || defined(ROCM_SYMLINK_GAVE_WARNING)
/* include file */
#include "rocrand/rocrand_sobol64.h"
#else
/* give warning */
#if defined(_MSC_VER)
#pragma message(": warning:This file is deprecated. Use the header file from /opt/rocm-5.2.0/include/rocrand/rocrand_sobol64.h by using #include <rocrand/rocrand_sobol64.h>")
#elif defined(__GNUC__)
#pragma message(": warning : This file is deprecated. Use the header file from /opt/rocm-5.2.0/include/rocrand/rocrand_sobol64.h by using #include <rocrand/rocrand_sobol64.h>")
#endif
/* include file */
#define ROCM_SYMLINK_GAVE_WARNING
#include "rocrand/rocrand_sobol64.h"
#undef ROCM_SYMLINK_GAVE_WARNING
#endif /* defined(ROCM_NO_WRAPPER_HEADER_WARNING) || defined(ROCM_SYMLINK_GAVE_WARNING) */

#endif /* ROCM_SYMLINK_ROCRAND_SOBOL64_H */


