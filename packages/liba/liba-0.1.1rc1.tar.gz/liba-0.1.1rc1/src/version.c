/*!
 @file version.c
 @brief algorithm library version
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#include "a/version.h"

a_cstr_t a_version(void)
{
    return A_VERSION;
}

a_uint_t a_version_major(void)
{
    return A_VERSION_MAJOR;
}

a_uint_t a_version_minor(void)
{
    return A_VERSION_MINOR;
}

a_uint_t a_version_patch(void)
{
    return A_VERSION_PATCH;
}
