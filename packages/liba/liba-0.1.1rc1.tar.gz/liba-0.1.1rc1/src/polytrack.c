/*!
 @file polytrack.c
 @brief polynomial trajectory
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#include "a/polytrack.h"
#include "a/poly.h"
#include <assert.h>

/* function for cubic polynomial trajectory */

a_void_t a_polytrack3_init(a_polytrack3_s *ctx, const a_real_t source[3], const a_real_t target[3])
{
    A_ASSERT(ctx);
    A_ASSERT(source);
    A_ASSERT(target);

    ctx->t[0] = source[0];
    ctx->q[0] = source[1];
    ctx->v[0] = source[2];
    ctx->t[1] = target[0];
    ctx->q[1] = target[1];
    ctx->v[1] = target[2];

    a_real_t q = ctx->q[1] - ctx->q[0];
    a_real_t t = ctx->t[1] - ctx->t[0];
    a_real_t inv_t1 = 1 / t;
    a_real_t inv_t2 = inv_t1 * inv_t1;
    a_real_t inv_t3 = inv_t1 * inv_t2;

    ctx->k[0] = ctx->q[0];
    ctx->k[1] = ctx->v[0];
    ctx->k[2] = inv_t1 * (-2 * ctx->v[0] - ctx->v[1]) +
                inv_t2 * q * 3;
    ctx->k[3] = inv_t2 * (ctx->v[0] + ctx->v[1]) -
                inv_t3 * q * 2;
}

a_real_t a_polytrack3_pos(const a_polytrack3_s *ctx, a_real_t ts)
{
    A_ASSERT(ctx);
    a_real_t a[4] = {
        ctx->k[3],
        ctx->k[2],
        ctx->k[1],
        ctx->k[0],
    };
    return a_poly_r(a, 4, ts - ctx->t[0]);
}

a_real_t a_polytrack3_vec(const a_polytrack3_s *ctx, a_real_t ts)
{
    A_ASSERT(ctx);
    a_real_t a[3] = {
        ctx->k[3] * 3,
        ctx->k[2] * 2,
        ctx->k[1],
    };
    return a_poly_r(a, 3, ts - ctx->t[0]);
}

a_real_t a_polytrack3_acc(const a_polytrack3_s *ctx, a_real_t ts)
{
    A_ASSERT(ctx);
    a_real_t a[2] = {
        ctx->k[3] * 3 * 2,
        ctx->k[2] * 2,
    };
    return a_poly_r(a, 2, ts - ctx->t[0]);
}

a_void_t a_polytrack3_all(const a_polytrack3_s *ctx, a_real_t ts, a_real_t out[3])
{
    A_ASSERT(out);
    A_ASSERT(ctx);
    a_real_t a[4] = {
        ctx->k[3],
        ctx->k[2],
        ctx->k[1],
        ctx->k[0],
    };
    ts -= ctx->t[0];
    out[0] = a_poly_r(a, 4, ts);
    a[0] *= 3;
    a[1] *= 2;
    out[1] = a_poly_r(a, 3, ts);
    a[0] *= 2;
    out[2] = a_poly_r(a, 2, ts);
}

/* function for quintic polynomial trajectory */

a_void_t a_polytrack5_init(a_polytrack5_s *ctx, const a_real_t source[4], const a_real_t target[4])
{
    A_ASSERT(ctx);
    A_ASSERT(source);
    A_ASSERT(target);

    ctx->t[0] = source[0];
    ctx->q[0] = source[1];
    ctx->v[0] = source[2];
    ctx->a[0] = source[3];
    ctx->t[1] = target[0];
    ctx->q[1] = target[1];
    ctx->v[1] = target[2];
    ctx->a[1] = target[3];

    a_real_t q = ctx->q[1] - ctx->q[0];
    a_real_t t = ctx->t[1] - ctx->t[0];
    a_real_t inv_t1 = 1 / t;
    a_real_t inv_t2 = inv_t1 * inv_t1;
    a_real_t inv_t3 = inv_t1 * inv_t2;
    a_real_t inv_t4 = inv_t2 * inv_t2;
    a_real_t inv_t5 = inv_t2 * inv_t3;

    ctx->k[0] = ctx->q[0];
    ctx->k[1] = ctx->v[0];
    ctx->k[2] = ctx->a[0] * (a_real_t)(1 / 2.0);
    ctx->k[3] = (a_real_t)(1 / 2.0) *
                (inv_t1 * (ctx->a[1] - 3 * ctx->a[0]) -
                 inv_t2 * (12 * ctx->v[0] + 8 * ctx->v[1]) +
                 inv_t3 * q * 20);
    ctx->k[4] = (a_real_t)(1 / 2.0) *
                (inv_t2 * (3 * ctx->a[0] - 2 * ctx->a[1]) +
                 inv_t3 * (16 * ctx->v[0] + 14 * ctx->v[1]) -
                 inv_t4 * q * 30);
    ctx->k[5] = (a_real_t)(1 / 2.0) *
                (inv_t3 * (ctx->a[1] - ctx->a[0]) -
                 inv_t4 * (ctx->v[0] + ctx->v[1]) * 6 +
                 inv_t5 * q * 12);
}

a_real_t a_polytrack5_pos(const a_polytrack5_s *ctx, a_real_t ts)
{
    A_ASSERT(ctx);
    a_real_t a[6] = {
        ctx->k[5],
        ctx->k[4],
        ctx->k[3],
        ctx->k[2],
        ctx->k[1],
        ctx->k[0],
    };
    return a_poly_r(a, 6, ts - ctx->t[0]);
}

a_real_t a_polytrack5_vec(const a_polytrack5_s *ctx, a_real_t ts)
{
    A_ASSERT(ctx);
    a_real_t a[5] = {
        ctx->k[5] * 5,
        ctx->k[4] * 4,
        ctx->k[3] * 3,
        ctx->k[2] * 2,
        ctx->k[1],
    };
    return a_poly_r(a, 5, ts - ctx->t[0]);
}

a_real_t a_polytrack5_acc(const a_polytrack5_s *ctx, a_real_t ts)
{
    A_ASSERT(ctx);
    a_real_t a[4] = {
        ctx->k[5] * 5 * 4,
        ctx->k[4] * 4 * 3,
        ctx->k[3] * 3 * 2,
        ctx->k[2] * 2,
    };
    return a_poly_r(a, 4, ts - ctx->t[0]);
}

a_void_t a_polytrack5_all(const a_polytrack5_s *ctx, a_real_t ts, a_real_t out[3])
{
    A_ASSERT(out);
    A_ASSERT(ctx);
    a_real_t a[6] = {
        ctx->k[5],
        ctx->k[4],
        ctx->k[3],
        ctx->k[2],
        ctx->k[1],
        ctx->k[0],
    };
    ts -= ctx->t[0];
    out[0] = a_poly_r(a, 6, ts);
    a[0] *= 5;
    a[1] *= 4;
    a[2] *= 3;
    a[3] *= 2;
    out[1] = a_poly_r(a, 5, ts);
    a[0] *= 4;
    a[1] *= 3;
    a[2] *= 2;
    out[2] = a_poly_r(a, 4, ts);
}

/* function for hepta polynomial trajectory */

a_void_t a_polytrack7_init(a_polytrack7_s *ctx, const a_real_t source[5], const a_real_t target[5])
{
    A_ASSERT(ctx);
    A_ASSERT(source);
    A_ASSERT(target);

    ctx->t[0] = source[0];
    ctx->q[0] = source[1];
    ctx->v[0] = source[2];
    ctx->a[0] = source[3];
    ctx->j[0] = source[4];
    ctx->t[1] = target[0];
    ctx->q[1] = target[1];
    ctx->v[1] = target[2];
    ctx->a[1] = target[3];
    ctx->j[1] = target[4];

    a_real_t q = ctx->q[1] - ctx->q[0];
    a_real_t t = ctx->t[1] - ctx->t[0];
    a_real_t inv_t1 = 1 / t;
    a_real_t inv_t2 = inv_t1 * inv_t1;
    a_real_t inv_t3 = inv_t1 * inv_t2;
    a_real_t inv_t4 = inv_t2 * inv_t2;
    a_real_t inv_t5 = inv_t2 * inv_t3;
    a_real_t inv_t6 = inv_t3 * inv_t3;
    a_real_t inv_t7 = inv_t3 * inv_t4;

    ctx->k[0] = ctx->q[0];
    ctx->k[1] = ctx->v[0];
    ctx->k[2] = ctx->a[0] * (a_real_t)(1 / 2.0);
    ctx->k[3] = ctx->j[0] * (a_real_t)(1 / 6.0);
    ctx->k[4] = (a_real_t)(1 / 6.0) *
                (inv_t1 * (-4 * ctx->j[0] - ctx->j[1]) +
                 inv_t2 * (15 * ctx->a[1] - 30 * ctx->a[0]) -
                 inv_t3 * (120 * ctx->v[0] + 90 * ctx->v[1]) +
                 inv_t4 * q * 210);
    ctx->k[5] = (a_real_t)(1 / 2.0) *
                (inv_t2 * (2 * ctx->j[0] + ctx->j[1]) +
                 inv_t3 * (20 * ctx->a[0] - 14 * ctx->a[1]) +
                 inv_t4 * (90 * ctx->v[0] + 78 * ctx->v[1]) -
                 inv_t5 * q * 168);
    ctx->k[6] = (a_real_t)(1 / 6.0) *
                (inv_t3 * (-4 * ctx->j[0] - 3 * ctx->j[1]) +
                 inv_t4 * (39 * ctx->a[1] - 45 * ctx->a[0]) -
                 inv_t5 * (216 * ctx->v[0] + 204 * ctx->v[1]) +
                 inv_t6 * q * 420);
    ctx->k[7] = (a_real_t)(1 / 6.0) *
                (inv_t4 * (ctx->j[0] + ctx->j[1]) +
                 inv_t5 * (ctx->a[0] - ctx->a[1]) * 12 +
                 inv_t6 * (ctx->v[0] + ctx->v[1]) * 60 -
                 inv_t7 * q * 120);
}

a_real_t a_polytrack7_pos(const a_polytrack7_s *ctx, a_real_t ts)
{
    A_ASSERT(ctx);
    a_real_t a[8] = {
        ctx->k[7],
        ctx->k[6],
        ctx->k[5],
        ctx->k[4],
        ctx->k[3],
        ctx->k[2],
        ctx->k[1],
        ctx->k[0],
    };
    return a_poly_r(a, 8, ts - ctx->t[0]);
}

a_real_t a_polytrack7_vec(const a_polytrack7_s *ctx, a_real_t ts)
{
    A_ASSERT(ctx);
    a_real_t a[7] = {
        ctx->k[7] * 7,
        ctx->k[6] * 6,
        ctx->k[5] * 5,
        ctx->k[4] * 4,
        ctx->k[3] * 3,
        ctx->k[2] * 2,
        ctx->k[1],
    };
    return a_poly_r(a, 7, ts - ctx->t[0]);
}

a_real_t a_polytrack7_acc(const a_polytrack7_s *ctx, a_real_t ts)
{
    A_ASSERT(ctx);
    a_real_t a[6] = {
        ctx->k[7] * 7 * 6,
        ctx->k[6] * 6 * 5,
        ctx->k[5] * 5 * 4,
        ctx->k[4] * 4 * 3,
        ctx->k[3] * 3 * 2,
        ctx->k[2] * 2,
    };
    return a_poly_r(a, 6, ts - ctx->t[0]);
}

a_real_t a_polytrack7_jer(const a_polytrack7_s *ctx, a_real_t ts)
{
    A_ASSERT(ctx);
    a_real_t a[5] = {
        ctx->k[7] * 7 * 6 * 5,
        ctx->k[6] * 6 * 5 * 4,
        ctx->k[5] * 5 * 4 * 3,
        ctx->k[4] * 4 * 3 * 2,
        ctx->k[3] * 3 * 2,
    };
    return a_poly_r(a, 5, ts - ctx->t[0]);
}

a_void_t a_polytrack7_all(const a_polytrack7_s *ctx, a_real_t ts, a_real_t out[4])
{
    A_ASSERT(out);
    A_ASSERT(ctx);
    a_real_t a[8] = {
        ctx->k[7],
        ctx->k[6],
        ctx->k[5],
        ctx->k[4],
        ctx->k[3],
        ctx->k[2],
        ctx->k[1],
        ctx->k[0],
    };
    ts -= ctx->t[0];
    out[0] = a_poly_r(a, 8, ts);
    a[0] *= 7;
    a[1] *= 6;
    a[2] *= 5;
    a[3] *= 4;
    a[4] *= 3;
    a[5] *= 2;
    out[1] = a_poly_r(a, 7, ts);
    a[0] *= 6;
    a[1] *= 5;
    a[2] *= 4;
    a[3] *= 3;
    a[4] *= 2;
    out[2] = a_poly_r(a, 6, ts);
    a[0] *= 5;
    a[1] *= 4;
    a[2] *= 3;
    a[3] *= 2;
    out[3] = a_poly_r(a, 5, ts);
}
