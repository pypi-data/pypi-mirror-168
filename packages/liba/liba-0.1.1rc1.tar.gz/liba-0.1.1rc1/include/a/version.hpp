/*!
 @file version.hpp
 @brief algorithm library version
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#ifndef __A_VERSION_HPP__
#define __A_VERSION_HPP__

#include "a.hpp"

namespace a
{
/*!
 @ingroup AA
 @addtogroup AA_VERSION algorithm library version based on C++
 @{
*/

/*!
 @brief enumeration for algorithm library version
*/
enum
{
    VERSION_MAJOR = A_VERSION_MAJOR,
    VERSION_MINOR = A_VERSION_MINOR,
    VERSION_PATCH = A_VERSION_PATCH,
};

/*!
 @brief algorithm library version string
*/
A_PUBLIC cstr_t version(void);

/*!
 @brief algorithm library version major
*/
A_PUBLIC uint_t version_major(void);
/*!
 @brief algorithm library version minor
*/
A_PUBLIC uint_t version_minor(void);
/*!
 @brief algorithm library version patch
*/
A_PUBLIC uint_t version_patch(void);

/*! @} AA_VERSION */
} // namespace a

#endif /* __A_VERSION_HPP__ */
