/*!
 @file fpid.c
 @brief fuzzy proportional integral derivative controller
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#include "a/fpid.h"
#include <math.h>

#undef A_FPID_BUF1
a_size_t A_FPID_BUF1(a_uint_t max)
{
    return sizeof(a_uint_t) * (max << 1) + sizeof(a_real_t) * (max + 2) * max;
}

a_fpid_s *a_fpid_off(a_fpid_s *ctx)
{
    a_pid_off(ctx->pid);
    return ctx;
}

a_fpid_s *a_fpid_inc(a_fpid_s *ctx)
{
    a_pid_inc(ctx->pid);
    return ctx;
}

a_fpid_s *a_fpid_pos(a_fpid_s *ctx, a_real_t max)
{
    a_pid_pos(ctx->pid, max);
    return ctx;
}

a_fpid_s *a_fpid_mode(a_fpid_s *ctx, a_uint_t mode)
{
    a_pid_mode(ctx->pid, mode);
    return ctx;
}

a_fpid_s *a_fpid_time(a_fpid_s *ctx, a_real_t ts)
{
    a_pid_time(ctx->pid, ts);
    return ctx;
}

a_fpid_s *a_fpid_ilim(a_fpid_s *ctx, a_real_t min, a_real_t max)
{
    a_real_t x = (a_real_t)((ctx->pid->num - 1) >> 1 << 1);
    ctx->sigma = x / (max - min);
    return ctx;
}

a_fpid_s *a_fpid_olim(a_fpid_s *ctx, a_real_t min, a_real_t max)
{
    a_real_t x = (a_real_t)((ctx->pid->num - 1) >> 1 << 1);
    ctx->alpha = (max - min) / x;
    return ctx;
}

a_fpid_s *a_fpid_buf1(a_fpid_s *ctx, a_vptr_t ptr, a_size_t max)
{
    max <<= 1;
    ctx->idx = (a_uint_t *)ptr;
    ptr = (a_byte_t *)ptr + sizeof(a_uint_t) * max;
    ctx->mms = (a_real_t *)ptr;
    ptr = (a_byte_t *)ptr + sizeof(a_real_t) * max;
    ctx->mat = (a_real_t *)ptr;
    return ctx;
}

a_fpid_s *a_fpid_kpid(a_fpid_s *ctx, a_real_t kp, a_real_t ki, a_real_t kd)
{
    a_pid_kpid(ctx->pid, kp, ki, kd);
    ctx->kp = kp;
    ctx->ki = ki;
    ctx->kd = kd;
    return ctx;
}

a_fpid_s *a_fpid_buff(a_fpid_s *ctx, a_uint_t *idx, a_real_t *mms, a_real_t *mat)
{
    ctx->idx = idx;
    ctx->mms = mms;
    ctx->mat = mat;
    return ctx;
}

a_fpid_s *a_fpid_base(a_fpid_s *ctx, a_uint_t num, const a_real_t *mma, const a_real_t *mkp, const a_real_t *mki, const a_real_t *mkd)
{
    ctx->pid->num = num;
    ctx->mma = mma;
    ctx->mkp = mkp;
    ctx->mki = mki;
    ctx->mkd = mkd;
    return ctx;
}

A_INLINE a_real_t op(a_real_t a, a_real_t b)
{
    return A_REAL_F(sqrt, a * b) * A_REAL_F(sqrt, 1 - (1 - a) * (1 - b));
}

a_fpid_s *a_fpid_init(a_fpid_s *ctx, a_real_t ts, a_uint_t num, const a_real_t *mma,
                      const a_real_t *mkp, const a_real_t *mki, const a_real_t *mkd,
                      a_real_t imin, a_real_t imax, a_real_t omin, a_real_t omax)
{
    a_real_t x = (a_real_t)((num - 1) >> 1 << 1);
    a_pid_init(ctx->pid, ts, omin, omax);
    a_fpid_base(ctx, num, mma, mkp, mki, mkd);
    ctx->sigma = x / (imax - imin);
    ctx->alpha = (omax - omin) / x;
    ctx->idx = 0;
    ctx->mms = 0;
    ctx->mat = 0;
    ctx->op = op;
    ctx->kp = 0;
    ctx->ki = 0;
    ctx->kd = 0;
    return ctx;
}

a_real_t a_fpid_proc(a_fpid_s *ctx, a_real_t set, a_real_t ref)
{
    a_real_t e = set - ref;
    return a_fpid_proc_(ctx, set, ref, e, e - ctx->pid->e);
}

a_fpid_s *a_fpid_done(a_fpid_s *ctx)
{
    a_pid_done(ctx->pid);
    return ctx;
}

A_STATIC a_uint_t mf(a_fpid_s *ctx, a_real_t x, a_uint_t *idx, a_real_t *mms)
{
    a_uint_t num = 0;
    a_int_t e = A_MF_NUL;
    const a_real_t *a = ctx->mma;
    for (a_uint_t i = 0; (void)(e = (a_int_t)*a++), e != A_MF_NUL; ++i)
    {
        a_real_t y = 0;
        switch (e)
        {
        case A_MF_GAUSS:
        {
            y = a_mf_gauss(x, a[0], a[1]);
            a += 2;
        }
        break;
        case A_MF_GBELL:
        {
            y = a_mf_gbell(x, a[0], a[1], a[2]);
            a += 3;
        }
        break;
        case A_MF_SIG:
        {
            y = a_mf_sig(x, a[0], a[1]);
            a += 2;
        }
        break;
        case A_MF_TRAP:
        {
            y = a_mf_trap(x, a[0], a[1], a[2], a[3]);
            a += 4;
        }
        break;
        case A_MF_TRI:
        {
            y = a_mf_tri(x, a[0], a[1], a[2]);
            a += 3;
        }
        break;
        case A_MF_Z:
        {
            y = a_mf_z(x, a[0], a[1]);
            a += 2;
        }
        break;
        case A_MF_NUL:
        default:
            goto done;
        }
        if (y > 0)
        {
            ++num;
            *idx++ = i;
            *mms++ = y;
        }
    }
done:
    return num;
}

a_real_t a_fpid_proc_(a_fpid_s *ctx, a_real_t set, a_real_t ref, a_real_t e, a_real_t ec)
{
    a_real_t ev[2] = {e, ec};
    /* quantize input */
    ev[0] = ctx->sigma * ev[0] / (1 << 0);
    ev[1] = ctx->sigma * ev[1] / (1 << 1);
    /* calculate membership */
    a_uint_t ne = mf(ctx, ev[0], ctx->idx + 00, ctx->mms + 00);
    a_uint_t nc = mf(ctx, ev[1], ctx->idx + ne, ctx->mms + ne);
    if (!ne || !nc)
    {
        goto done;
    }
    /* joint membership */
    a_real_t inv = 0;
    for (a_uint_t i = 0; i != ne; ++i)
    {
        a_uint_t col = i * nc;
        for (a_uint_t j = 0; j != nc; ++j)
        {
            a_uint_t idx = col + j; /* mat(i,j)=f(e[i],ec[j]) */
            ctx->mat[idx] = ctx->op(ctx->mms[i], ctx->mms[ne + j]);
            inv += ctx->mat[idx];
        }
    }
    inv = ctx->alpha / inv;
    /* mean of centers defuzzifier */
    a_real_t qv[3] = {0, 0, 0};
    if (ctx->mkp == 0)
    {
        goto skip_kp;
    }
    for (a_uint_t i = 0; i != ne; ++i)
    {
        a_uint_t col = i * nc;
        a_uint_t num = ctx->idx[i] * ctx->pid->num;
        for (a_uint_t j = 0; j != nc; ++j)
        {
            qv[0] += ctx->mat[col + j] * ctx->mkp[ctx->idx[ne + j] + num]; /* mat(i,j)*kp(e[i],ec[j]) */
        }
    }
    qv[0] *= inv;
skip_kp:
    if (ctx->mki == 0)
    {
        goto skip_ki;
    }
    for (a_uint_t i = 0; i != ne; ++i)
    {
        a_uint_t col = i * nc;
        a_uint_t num = ctx->idx[i] * ctx->pid->num;
        for (a_uint_t j = 0; j != nc; ++j)
        {
            qv[1] += ctx->mat[col + j] * ctx->mki[ctx->idx[ne + j] + num]; /* mat(i,j)*ki(e[i],ec[j]) */
        }
    }
    qv[1] *= inv;
skip_ki:
    if (ctx->mkd == 0)
    {
        goto skip_kd;
    }
    for (a_uint_t i = 0; i != ne; ++i)
    {
        a_uint_t col = i * nc;
        a_uint_t num = ctx->idx[i] * ctx->pid->num;
        for (a_uint_t j = 0; j != nc; ++j)
        {
            qv[2] += ctx->mat[col + j] * ctx->mkd[ctx->idx[ne + j] + num]; /* mat(i,j)*kd(e[i],ec[j]) */
        }
    }
    qv[2] *= inv;
skip_kd:
    qv[0] += ctx->kp;
    qv[1] += ctx->ki;
    qv[2] += ctx->kd;
    a_pid_kpid(ctx->pid, qv[0], qv[1], qv[2]);
done:
    return a_pid_proc_(ctx->pid, set, ref, e, ec);
}
