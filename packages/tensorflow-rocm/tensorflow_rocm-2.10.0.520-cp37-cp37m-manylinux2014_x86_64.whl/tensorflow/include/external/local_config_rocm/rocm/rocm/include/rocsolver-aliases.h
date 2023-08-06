/*
    Copyright (c) 2022 Advanced Micro Devices, Inc. All rights reserved.
*/

#ifndef ROCM_SYMLINK_ROCSOLVER_ALIASES_H
#define ROCM_SYMLINK_ROCSOLVER_ALIASES_H

#if defined(ROCM_NO_WRAPPER_HEADER_WARNING) || defined(ROCM_SYMLINK_GAVE_WARNING)
/* include file */
#include "rocsolver/rocsolver-aliases.h"
#else
/* give warning */
#if defined(_MSC_VER)
#pragma message(": warning:This file is deprecated. Use the header file from /opt/rocm-5.2.0/include/rocsolver/rocsolver-aliases.h by using #include <rocsolver/rocsolver-aliases.h>")
#elif defined(__GNUC__)
#pragma message(": warning : This file is deprecated. Use the header file from /opt/rocm-5.2.0/include/rocsolver/rocsolver-aliases.h by using #include <rocsolver/rocsolver-aliases.h>")
#endif
/* include file */
#define ROCM_SYMLINK_GAVE_WARNING
#include "rocsolver/rocsolver-aliases.h"
#undef ROCM_SYMLINK_GAVE_WARNING
#endif /* defined(ROCM_NO_WRAPPER_HEADER_WARNING) || defined(ROCM_SYMLINK_GAVE_WARNING) */

#endif /* ROCM_SYMLINK_ROCSOLVER_ALIASES_H */


