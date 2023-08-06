/*!
 @file math.c
 @brief mathematical algorithm library
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#include "math.h"

a_f32_t a_inv_sqrt(a_f32_t x)
{
    union
    {
        a_f32_t x;
        a_u32_t u;
    } u[1] = {{x}};
    if (a_likely(x > 0))
    {
        a_f32_t xh = 0.5F * x;
        u->u = 0x5F3759DF - (u->u >> 1);
        u->x *= 1.5F - SQ(u->x) * xh;
        u->x *= 1.5F - SQ(u->x) * xh;
    }
    else if (x < 0)
    {
        u->u = 0xFFC00000;
    }
    else
    {
        u->u = 0x7F800000;
    }
    return u->x;
}
