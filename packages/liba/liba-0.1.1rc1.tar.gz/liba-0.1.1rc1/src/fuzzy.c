/*!
 @file fuzzy.c
 @brief fuzzy operator
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#include "a/fuzzy.h"
#include <math.h>

a_real_t a_fuzzy_or(a_uint_t e, a_real_t l, a_real_t r)
{
    switch (e)
    {
    case A_FUZZY_ALGEBRA:
        return l + r - l * r;
    case A_FUZZY_BOUNDED:
        return A_REAL_F(fmin, 1, l + r);
    case A_FUZZY_DEFAULT:
    default:
        return A_REAL_F(fmax, l, r);
    }
}

a_real_t a_fuzzy_and(a_uint_t e, a_real_t l, a_real_t r)
{
    switch (e)
    {
    case A_FUZZY_ALGEBRA:
        return l * r;
    case A_FUZZY_BOUNDED:
        return A_REAL_F(fmax, 0, l + r - 1);
    case A_FUZZY_DEFAULT:
    default:
        return A_REAL_F(fmin, l, r);
    }
}

a_real_t a_fuzzy_equ(a_real_t gamma, a_real_t l, a_real_t r)
{
    return A_REAL_F(pow, l * r, 1 - gamma) *
           A_REAL_F(pow, 1 - (1 - l) * (1 - r), gamma);
}
