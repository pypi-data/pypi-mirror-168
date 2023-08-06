/*
    Copyright (c) 2022 Advanced Micro Devices, Inc. All rights reserved.
*/

#ifndef ROCM_SYMLINK_ROCSPARSE_VERSION_H
#define ROCM_SYMLINK_ROCSPARSE_VERSION_H

#if defined(ROCM_NO_WRAPPER_HEADER_WARNING) || defined(ROCM_SYMLINK_GAVE_WARNING)
/* include file */
#include "rocsparse/rocsparse-version.h"
#else
/* give warning */
#if defined(_MSC_VER)
#pragma message(": warning:This file is deprecated. Use the header file from /opt/rocm-5.2.0/include/rocsparse/rocsparse-version.h by using #include <rocsparse/rocsparse-version.h>")
#elif defined(__GNUC__)
#pragma message(": warning : This file is deprecated. Use the header file from /opt/rocm-5.2.0/include/rocsparse/rocsparse-version.h by using #include <rocsparse/rocsparse-version.h>")
#endif
/* include file */
#define ROCM_SYMLINK_GAVE_WARNING
#include "rocsparse/rocsparse-version.h"
#undef ROCM_SYMLINK_GAVE_WARNING
#endif /* defined(ROCM_NO_WRAPPER_HEADER_WARNING) || defined(ROCM_SYMLINK_GAVE_WARNING) */

#endif /* ROCM_SYMLINK_ROCSPARSE_VERSION_H */


