/*!
 @file version.h
 @brief algorithm library version
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#ifndef __A_VERSION_H__
#define __A_VERSION_H__

#include "a.h"

/*!
 @ingroup A
 @addtogroup A_VERSION algorithm library version based on C
 @{
*/

#if defined(__cplusplus)
extern "C" {
#endif /* __cplusplus */

/*!
 @brief algorithm library version string
*/
A_PUBLIC a_cstr_t a_version(void);

/*!
 @brief algorithm library version major
*/
A_PUBLIC a_uint_t a_version_major(void);
/*!
 @brief algorithm library version minor
*/
A_PUBLIC a_uint_t a_version_minor(void);
/*!
 @brief algorithm library version patch
*/
A_PUBLIC a_uint_t a_version_patch(void);

#if defined(__cplusplus)
} /* extern "C" */
#endif /* __cplusplus */

/*! @} A_VERSION */

#endif /* __A_VERSION_H__ */
