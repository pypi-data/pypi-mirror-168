/*
    Copyright (c) 2022 Advanced Micro Devices, Inc. All rights reserved.
*/

#ifndef ROCM_SYMLINK_INTERNAL_HIPSOLVER_VERSION_H
#define ROCM_SYMLINK_INTERNAL_HIPSOLVER_VERSION_H

#if defined(ROCM_NO_WRAPPER_HEADER_WARNING) || defined(ROCM_SYMLINK_GAVE_WARNING)
/* include file */
#include "../hipsolver/internal/hipsolver-version.h"
#else
/* give warning */
#if defined(_MSC_VER)
#pragma message(": warning:This file is deprecated. Use the header file from /opt/rocm-5.2.0/include/hipsolver/internal/hipsolver-version.h by using #include <hipsolver/internal/hipsolver-version.h>")
#elif defined(__GNUC__)
#pragma message(": warning : This file is deprecated. Use the header file from /opt/rocm-5.2.0/include/hipsolver/internal/hipsolver-version.h by using #include <hipsolver/internal/hipsolver-version.h>")
#endif
/* include file */
#define ROCM_SYMLINK_GAVE_WARNING
#include "../hipsolver/internal/hipsolver-version.h"
#undef ROCM_SYMLINK_GAVE_WARNING
#endif /* defined(ROCM_NO_WRAPPER_HEADER_WARNING) || defined(ROCM_SYMLINK_GAVE_WARNING) */

#endif /* ROCM_SYMLINK_INTERNAL_HIPSOLVER_VERSION_H */

#if 0

/* The following is a copy of the original file for the benefit of build systems which grep for values
 * in this file rather than preprocess it. This is just for backward compatibility */

/* ************************************************************************
 * Copyright 2020-2021 Advanced Micro Devices, Inc.
 * ************************************************************************ */

#ifndef HIPSOLVER_VERSION_H_
#define HIPSOLVER_VERSION_H_

/* the configured version and settings
 */
// clang-format off
#define hipsolverVersionMajor 1
#define hipsolverVersionMinor 4
#define hipsolverVersionPatch 0
#define hipsolverVersionTweak 74dafd0
// clang-format on

#endif

#endif
