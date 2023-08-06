/*!
 @file pid.c
 @brief proportional integral derivative controller
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#include "a/pid.h"

a_pid_s *a_pid_off(a_pid_s *ctx)
{
    ctx->mode = A_PID_OFF;
    return ctx;
}

a_pid_s *a_pid_inc(a_pid_s *ctx)
{
    ctx->mode = A_PID_INC;
    return ctx;
}

a_pid_s *a_pid_pos(a_pid_s *ctx, a_real_t max)
{
    ctx->summax = (max > 0) ? max : -max;
    if (ctx->outmax < ctx->summax)
    {
        ctx->summax = ctx->outmax;
    }
    ctx->mode = A_PID_POS;
    return ctx;
}

a_pid_s *a_pid_mode(a_pid_s *ctx, a_uint_t mode)
{
    ctx->mode = mode;
    return ctx;
}

a_pid_s *a_pid_time(a_pid_s *ctx, a_real_t ts)
{
    a_real_t t = ts / ctx->ts;
    ctx->ki *= t;
    ctx->kd /= t;
    ctx->ts = ts;
    return ctx;
}

a_pid_s *a_pid_kpid(a_pid_s *ctx, a_real_t kp, a_real_t ki, a_real_t kd)
{
    ctx->kp = kp;
    ctx->ki = ki * ctx->ts;
    ctx->kd = kd / ctx->ts;
    return ctx;
}

a_pid_s *a_pid_init(a_pid_s *ctx, a_real_t ts, a_real_t min, a_real_t max)
{
    ctx->mode = A_PID_OFF;
    ctx->outmin = min;
    ctx->outmax = max;
    ctx->summax = 0;
    ctx->ts = ts;
    ctx->kp = 0;
    ctx->ki = 0;
    ctx->kd = 0;
    ctx->out = 0;
    ctx->sum = 0;
    ctx->num = 0;
    ctx->ref = 0;
    ctx->ec = 0;
    ctx->e = 0;
    return ctx;
}

a_real_t a_pid_proc(a_pid_s *ctx, a_real_t set, a_real_t ref)
{
    a_real_t e = set - ref;
    return a_pid_proc_(ctx, set, ref, e, e - ctx->e);
}

a_pid_s *a_pid_done(a_pid_s *ctx)
{
    ctx->out = 0;
    ctx->sum = 0;
    ctx->ref = 0;
    ctx->ec = 0;
    ctx->e = 0;
    return ctx;
}

a_real_t a_pid_proc_(a_pid_s *ctx, a_real_t set, a_real_t ref, a_real_t e, a_real_t ec)
{
    /* calculation */
    switch (ctx->mode)
    {
    case A_PID_OFF:
    {
        ctx->out = ctx->sum = set;
    }
    break;
    case A_PID_POS:
    {
        a_real_t sum = ctx->ki * e;
        /* when the limit of integration is exceeded or */
        /* the direction of integration is the same, the integration stops. */
        if ((-ctx->summax < ctx->sum && ctx->sum < ctx->summax) || ctx->sum * sum < 0)
        {
            /* sum = K_i \sum^k_{i=0} e(i) */
            ctx->sum += sum;
        }
        /* avoid derivative kick, ref[k-1]-ref[k] */
        /* out = K_p e(k) + sum + K_d [ref(k-1)-ref(k)] */
        ctx->out = ctx->kp * e + ctx->sum + ctx->kd * (ctx->ref - ref);
    }
    break;
    case A_PID_INC:
    {
        /* K_p[e(k)-e(k-1)]+K_i e(k)+K_d[ec(k)-ec(k-1)] */
        ctx->sum += ctx->kp * ec + ctx->ki * e + ctx->kd * (ec - ctx->ec);
        ctx->out = ctx->sum;
    }
    break;
    default:
        break;
    }

    /* output limiter */
    if (ctx->out < ctx->outmin)
    {
        ctx->out = ctx->outmin;
    }
    else if (ctx->out > ctx->outmax)
    {
        ctx->out = ctx->outmax;
    }

    /* cache data */
    ctx->ref = ref;
    ctx->ec = ec;
    ctx->e = e;

    return ctx->out;
}
