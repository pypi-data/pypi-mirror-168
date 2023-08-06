/*!
 @file mf.c
 @brief membership function
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#include "a/mf.h"
#include <math.h>

a_real_t a_mf_gauss(a_real_t x, a_real_t sigma, a_real_t c)
{
    return A_REAL_F(exp, A_REAL_F(pow, (x - c) / sigma, 2) / -2);
}

a_real_t a_mf_gbell(a_real_t x, a_real_t a, a_real_t b, a_real_t c)
{
    return 1 / (A_REAL_F(pow, A_REAL_F(fabs, (x - c) / a), 2 * b) + 1);
}

a_real_t a_mf_sig(a_real_t x, a_real_t a, a_real_t c)
{
    return 1 / (A_REAL_F(exp, (c - x) * a) + 1);
}

a_real_t a_mf_trap(a_real_t x, a_real_t a, a_real_t b, a_real_t c, a_real_t d)
{
    if (x < a)
    {
        x = 0;
    }
    else if (x < b)
    {
        x = (x - a) / (b - a);
    }
    else if (x < c)
    {
        x = 1;
    }
    else if (x < d)
    {
        x = (d - x) / (d - c);
    }
    else
    {
        x = 0;
    }
    return x;
}

a_real_t a_mf_tri(a_real_t x, a_real_t a, a_real_t b, a_real_t c)
{
    if (x < a)
    {
        x = 0;
    }
    else if (x < b)
    {
        x = (x - a) / (b - a);
    }
    else if (x < c)
    {
        x = (c - x) / (c - b);
    }
    else
    {
        x = 0;
    }
    return x;
}

a_real_t a_mf_z(a_real_t x, a_real_t a, a_real_t b)
{
    if (x < a)
    {
        x = 1;
    }
    else if (x < (a + b) / 2)
    {
        x = 1 - 2 * A_REAL_F(pow, (x - a) / (b - a), 2);
    }
    else if (x < b)
    {
        x = 2 * A_REAL_F(pow, (x - b) / (b - a), 2);
    }
    else
    {
        x = 0;
    }
    return x;
}

a_real_t a_mf(a_uint_t e, a_real_t x, a_real_t *a)
{
    switch (e)
    {
    case A_MF_GAUSS:
        return a_mf_gauss(x, a[0], a[1]);
    case A_MF_GBELL:
        return a_mf_gbell(x, a[0], a[1], a[2]);
    case A_MF_SIG:
        return a_mf_sig(x, a[0], a[1]);
    case A_MF_TRAP:
        return a_mf_trap(x, a[0], a[1], a[2], a[3]);
    case A_MF_TRI:
        return a_mf_tri(x, a[0], a[1], a[2]);
    case A_MF_Z:
        return a_mf_z(x, a[0], a[1]);
    case A_MF_NUL:
    default:
        return 0;
    }
}
