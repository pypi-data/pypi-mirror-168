/*
    Copyright (c) 2022 Advanced Micro Devices, Inc. All rights reserved.
*/

#ifndef ROCM_SYMLINK_INTERNAL_ROCBLAS_VERSION_H
#define ROCM_SYMLINK_INTERNAL_ROCBLAS_VERSION_H

#if defined(ROCM_NO_WRAPPER_HEADER_WARNING) || defined(ROCM_SYMLINK_GAVE_WARNING)
/* include file */
#include "../rocblas/internal/rocblas-version.h"
#else
/* give warning */
#if defined(_MSC_VER)
#pragma message(": warning:This file is deprecated. Use the header file from /opt/rocm-5.2.0/include/rocblas/internal/rocblas-version.h by using #include <rocblas/internal/rocblas-version.h>")
#elif defined(__GNUC__)
#pragma message(": warning : This file is deprecated. Use the header file from /opt/rocm-5.2.0/include/rocblas/internal/rocblas-version.h by using #include <rocblas/internal/rocblas-version.h>")
#endif
/* include file */
#define ROCM_SYMLINK_GAVE_WARNING
#include "../rocblas/internal/rocblas-version.h"
#undef ROCM_SYMLINK_GAVE_WARNING
#endif /* defined(ROCM_NO_WRAPPER_HEADER_WARNING) || defined(ROCM_SYMLINK_GAVE_WARNING) */

#endif /* ROCM_SYMLINK_INTERNAL_ROCBLAS_VERSION_H */

#if 0

/* The following is a copy of the original file for the benefit of build systems which grep for values
 * in this file rather than preprocess it. This is just for backward compatibility */

/* ************************************************************************
 * Copyright 2016-2022 Advanced Micro Devices, Inc.
 * ************************************************************************ */

/* the configured version and settings
 */
#ifndef ROCBLAS_VERSION_H_
#define ROCBLAS_VERSION_H_

// clang-format off
#define ROCBLAS_VERSION_MAJOR       2
#define ROCBLAS_VERSION_MINOR       44
#define ROCBLAS_VERSION_PATCH       0
#define ROCBLAS_VERSION_TWEAK       4a92c6f1-dirty
#define ROCBLAS_VERSION_COMMIT_ID   
// clang-format on

#endif

#endif
