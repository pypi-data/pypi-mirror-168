/*!
 @file arr.c
 @brief basic array library
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#include "a/arr.h"
#include <assert.h>
#include <string.h>
#include <stdlib.h>

#undef a_arr_at
#undef a_arr_at_
#undef a_arr_ptr
#undef a_arr_end
#undef a_arr_top
#undef a_arr_top_
#undef a_arr_push
#undef a_arr_pull
#undef a_arr_search
#undef a_arr_insert
#undef a_arr_remove
#undef a_arr_push_fore
#undef a_arr_push_back
#undef a_arr_pull_fore
#undef a_arr_pull_back

A_ALWAYS a_vptr_t a_arr_inc_(a_arr_s *ctx)
{
    return (a_byte_t *)ctx->__ptr + ctx->__siz * ctx->__num++;
}

A_ALWAYS a_vptr_t a_arr_dec_(a_arr_s *ctx)
{
    return (a_byte_t *)ctx->__ptr + ctx->__siz * --ctx->__num;
}

A_STATIC a_void_t a_arr_drop_(a_arr_s *ctx, a_size_t bot, a_void_t (*dtor)(a_vptr_t))
{
    if (dtor)
    {
        while (ctx->__num > bot)
        {
            dtor(a_arr_dec_(ctx));
        }
    }
    ctx->__num = bot;
}

a_void_t a_arr_ctor(a_arr_s *ctx, a_vptr_t ptr, a_size_t siz, a_size_t num)
{
    A_ASSERT(ctx);
    ctx->__ptr = ptr;
    ctx->__siz = siz;
    ctx->__mem = num;
    ctx->__num = 0;
}

a_void_t a_arr_dtor(a_arr_s *ctx, a_void_t (*dtor)(a_vptr_t))
{
    A_ASSERT(ctx);
    if (ctx->__ptr)
    {
        a_arr_drop_(ctx, 0, dtor);
        ctx->__ptr = 0;
    }
    ctx->__mem = 0;
    ctx->__siz = 0;
}

a_arr_s *a_arr_move(a_arr_s *ctx, a_arr_s *obj)
{
    A_ASSERT(ctx);
    A_ASSERT(obj);
    memcpy(ctx, obj, sizeof(*obj));
    memset(obj, 0, sizeof(*obj));
    return ctx;
}

a_void_t a_arr_drop(a_arr_s *ctx, a_void_t (*dtor)(a_vptr_t))
{
    A_ASSERT(ctx);
    a_arr_drop_(ctx, 0, dtor);
}

a_void_t a_arr_swap(const a_arr_s *ctx, a_size_t lhs, a_size_t rhs)
{
    A_ASSERT(ctx);
    a_size_t num = ctx->__num - 1;
    lhs = lhs < ctx->__num ? lhs : num;
    rhs = rhs < ctx->__num ? rhs : num;
    if (lhs != rhs)
    {
        a_byte_t *ptr = (a_byte_t *)ctx->__ptr;
        a_vptr_t lobj = ptr + lhs * ctx->__siz;
        a_vptr_t robj = ptr + rhs * ctx->__siz;
        a_swap(ctx->__siz, lobj, robj);
    }
}

a_void_t a_arr_sort(const a_arr_s *ctx, a_int_t (*cmp)(a_cptr_t, a_cptr_t))
{
    A_ASSERT(ctx);
    qsort(ctx->__ptr, ctx->__num, ctx->__siz, cmp);
}

a_void_t a_arr_sort_fore(const a_arr_s *ctx, a_int_t (*cmp)(a_cptr_t, a_cptr_t))
{
    A_ASSERT(ctx);
    if (ctx->__num > 1)
    {
        a_byte_t *ptr = (a_byte_t *)ctx->__ptr;
        a_byte_t *end = (a_byte_t *)ctx->__ptr + ctx->__siz * ctx->__num - ctx->__siz;
        do
        {
            a_byte_t *cur = ptr + ctx->__siz;
            if (cmp(ptr, cur) > 0)
            {
                a_swap(ctx->__siz, cur, ptr);
            }
            else
            {
                break;
            }
            ptr = cur;
        } while (ptr != end);
    }
}

a_void_t a_arr_sort_back(const a_arr_s *ctx, a_int_t (*cmp)(a_cptr_t, a_cptr_t))
{
    A_ASSERT(ctx);
    if (ctx->__num > 1)
    {
        a_byte_t *ptr = (a_byte_t *)ctx->__ptr + ctx->__siz * ctx->__num - ctx->__siz;
        do
        {
            a_byte_t *cur = ptr - ctx->__siz;
            if (cmp(cur, ptr) > 0)
            {
                a_swap(ctx->__siz, cur, ptr);
            }
            else
            {
                break;
            }
            ptr = cur;
        } while (ptr != ctx->__ptr);
    }
}

a_vptr_t a_arr_search(const a_arr_s *ctx, a_cptr_t obj, a_int_t (*cmp)(a_cptr_t, a_cptr_t))
{
    A_ASSERT(ctx);
    return bsearch(obj, ctx->__ptr, ctx->__num, ctx->__siz, cmp);
}

a_vptr_t a_arr_insert(a_arr_s *ctx, a_size_t idx)
{
    A_ASSERT(ctx);
    if (a_likely(ctx->__num < ctx->__mem))
    {
        if (idx < ctx->__num)
        {
            a_byte_t *src = (a_byte_t *)ctx->__ptr + ctx->__siz * (idx + 0);
            a_byte_t *dst = (a_byte_t *)ctx->__ptr + ctx->__siz * (idx + 1);
            memmove(dst, src, (ctx->__num - idx) * ctx->__siz);
            ++ctx->__num;
            return src;
        }
        return a_arr_inc_(ctx);
    }
    return 0;
}

a_vptr_t a_arr_push_fore(a_arr_s *ctx) { return a_arr_insert(ctx, 0); }

a_vptr_t a_arr_push_back(a_arr_s *ctx)
{
    A_ASSERT(ctx);
    return a_likely(ctx->__num < ctx->__mem) ? a_arr_inc_(ctx) : 0;
}

a_vptr_t a_arr_remove(a_arr_s *ctx, a_size_t idx)
{
    A_ASSERT(ctx);
    if (ctx->__num && idx < ctx->__num - 1)
    {
        a_byte_t *end = (a_byte_t *)ctx->__ptr + ctx->__siz * ctx->__num;
        a_byte_t *dst = (a_byte_t *)ctx->__ptr + ctx->__siz * (idx + 0);
        a_byte_t *src = (a_byte_t *)ctx->__ptr + ctx->__siz * (idx + 1);
        for (; src != end; src += ctx->__siz, dst += ctx->__siz)
        {
            a_swap(ctx->__siz, dst, src);
        }
        --ctx->__num;
        return dst;
    }
    return a_likely(ctx->__num) ? a_arr_dec_(ctx) : 0;
}

a_vptr_t a_arr_pull_fore(a_arr_s *ctx) { return a_arr_remove(ctx, 0); }

a_vptr_t a_arr_pull_back(a_arr_s *ctx)
{
    A_ASSERT(ctx);
    return a_likely(ctx->__num) ? a_arr_dec_(ctx) : 0;
}
