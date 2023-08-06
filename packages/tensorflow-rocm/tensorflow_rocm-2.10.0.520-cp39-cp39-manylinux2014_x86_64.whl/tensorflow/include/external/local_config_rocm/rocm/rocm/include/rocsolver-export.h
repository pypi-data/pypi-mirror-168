/*
    Copyright (c) 2022 Advanced Micro Devices, Inc. All rights reserved.
*/

#ifndef ROCM_SYMLINK_ROCSOLVER_EXPORT_H
#define ROCM_SYMLINK_ROCSOLVER_EXPORT_H

#if defined(ROCM_NO_WRAPPER_HEADER_WARNING) || defined(ROCM_SYMLINK_GAVE_WARNING)
/* include file */
#include "rocsolver/rocsolver-export.h"
#else
/* give warning */
#if defined(_MSC_VER)
#pragma message(": warning:This file is deprecated. Use the header file from /opt/rocm-5.2.0/include/rocsolver/rocsolver-export.h by using #include <rocsolver/rocsolver-export.h>")
#elif defined(__GNUC__)
#pragma message(": warning : This file is deprecated. Use the header file from /opt/rocm-5.2.0/include/rocsolver/rocsolver-export.h by using #include <rocsolver/rocsolver-export.h>")
#endif
/* include file */
#define ROCM_SYMLINK_GAVE_WARNING
#include "rocsolver/rocsolver-export.h"
#undef ROCM_SYMLINK_GAVE_WARNING
#endif /* defined(ROCM_NO_WRAPPER_HEADER_WARNING) || defined(ROCM_SYMLINK_GAVE_WARNING) */

#endif /* ROCM_SYMLINK_ROCSOLVER_EXPORT_H */

#if 0

/* The following is a copy of the original file for the benefit of build systems which grep for values
 * in this file rather than preprocess it. This is just for backward compatibility */

/* ************************************************************************
 * Copyright (c) 2019-2020 Advanced Micro Devices, Inc.
 * ************************************************************************ */

/* the configured version and settings
 */
#ifndef ROCSOLVER_VERSION_H_
#define ROCSOLVER_VERSION_H_

// clang-format off
#define ROCSOLVER_VERSION_MAJOR 3
#define ROCSOLVER_VERSION_MINOR 18
#define ROCSOLVER_VERSION_PATCH 0
#define ROCSOLVER_VERSION_TWEAK d883d5f
// clang-format on

#endif

#endif
