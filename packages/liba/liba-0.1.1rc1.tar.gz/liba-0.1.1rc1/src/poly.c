/*!
 @file poly.c
 @brief polynomial
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#include "a/poly.h"
#include <assert.h>

a_real_t *a_poly_inv(a_real_t *a, a_size_t n)
{
    A_ASSERT(!n || a);
    for (a_real_t *l = a, *r = a + n - 1, *m = a + (n >> 1); l < m; ++l, --r)
    {
        a_swap(sizeof(a_real_t), l, r);
    }
    return a;
}

a_real_t a_poly_c(const a_real_t *a, a_size_t n, a_real_t x)
{
    A_ASSERT(!n || a);
    a_real_t y = 0;
    for (const a_real_t *p = --a + n; p > a; --p)
    {
        y = y * x + *p;
    }
    return y;
}

a_real_t a_poly_r(const a_real_t *a, a_size_t n, a_real_t x)
{
    A_ASSERT(!n || a);
    a_real_t y = 0;
    for (const a_real_t *q = a + n; a < q; ++a)
    {
        y = y * x + *a;
    }
    return y;
}
