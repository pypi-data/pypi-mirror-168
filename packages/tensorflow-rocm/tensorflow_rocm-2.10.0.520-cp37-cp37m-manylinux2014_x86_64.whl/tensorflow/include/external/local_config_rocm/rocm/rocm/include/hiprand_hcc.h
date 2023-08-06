/*
    Copyright (c) 2022 Advanced Micro Devices, Inc. All rights reserved.
*/

#ifndef ROCM_SYMLINK_HIPRAND_HCC_H
#define ROCM_SYMLINK_HIPRAND_HCC_H

#if defined(ROCM_NO_WRAPPER_HEADER_WARNING) || defined(ROCM_SYMLINK_GAVE_WARNING)
/* include file */
#include "hiprand/hiprand_hcc.h"
#else
/* give warning */
#if defined(_MSC_VER)
#pragma message(": warning:This file is deprecated. Use the header file from /opt/rocm-5.2.0/include/hiprand/hiprand_hcc.h by using #include <hiprand/hiprand_hcc.h>")
#elif defined(__GNUC__)
#pragma message(": warning : This file is deprecated. Use the header file from /opt/rocm-5.2.0/include/hiprand/hiprand_hcc.h by using #include <hiprand/hiprand_hcc.h>")
#endif
/* include file */
#define ROCM_SYMLINK_GAVE_WARNING
#include "hiprand/hiprand_hcc.h"
#undef ROCM_SYMLINK_GAVE_WARNING
#endif /* defined(ROCM_NO_WRAPPER_HEADER_WARNING) || defined(ROCM_SYMLINK_GAVE_WARNING) */

#endif /* ROCM_SYMLINK_HIPRAND_HCC_H */


