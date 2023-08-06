/*!
 @file vec.c
 @brief basic vector library
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#if __STDC_HOSTED__

#include "a/host/vec.h"
#include <assert.h>
#include <string.h>

#undef a_vec_at
#undef a_vec_at_
#undef a_vec_ptr
#undef a_vec_end
#undef a_vec_top
#undef a_vec_end_
#undef a_vec_top_
#undef a_vec_push
#undef a_vec_pull
#undef a_vec_search
#undef a_vec_insert
#undef a_vec_remove
#undef a_vec_push_fore
#undef a_vec_push_back
#undef a_vec_pull_fore
#undef a_vec_pull_back

A_ALWAYS a_vptr_t a_vec_inc_(a_vec_s *ctx)
{
    return (a_byte_t *)ctx->__ptr + ctx->__siz * ctx->__num++;
}

A_ALWAYS a_vptr_t a_vec_dec_(a_vec_s *ctx)
{
    return (a_byte_t *)ctx->__ptr + ctx->__siz * --ctx->__num;
}

A_STATIC a_void_t a_vec_drop_(a_vec_s *ctx, a_size_t bot, a_void_t (*dtor)(a_vptr_t))
{
    if (dtor)
    {
        while (ctx->__num > bot)
        {
            dtor(a_vec_dec_(ctx));
        }
    }
    ctx->__num = bot;
}

A_STATIC a_int_t a_vec_alloc(a_vec_s *ctx, a_size_t num)
{
    if (ctx->__mem <= num)
    {
        a_size_t mem = ctx->__mem;
        do
        {
            mem += (mem >> 1) + 1;
        } while (mem < num);
        a_size_t siz = a_align(sizeof(a_vptr_t), ctx->__siz * mem);
        a_vptr_t ptr = realloc(ctx->__ptr, siz);
        if (a_unlikely(ptr == 0))
        {
            return A_FAILURE;
        }
        ctx->__mem = mem;
        ctx->__ptr = ptr;
    }
    return A_SUCCESS;
}

a_vec_s *a_vec_new(a_size_t size)
{
    a_vec_s *ctx = (a_vec_s *)malloc(sizeof(a_vec_s));
    if (ctx)
    {
        a_vec_ctor(ctx, size);
    }
    return ctx;
}

a_void_t a_vec_die(a_vec_s *ctx, a_void_t (*dtor)(a_vptr_t))
{
    if (ctx)
    {
        a_vec_dtor(ctx, dtor);
        free(ctx);
    }
}

a_void_t a_vec_ctor(a_vec_s *ctx, a_size_t size)
{
    A_ASSERT(ctx);
    ctx->__siz = size ? size : sizeof(a_cast_u);
    ctx->__mem = 0;
    ctx->__num = 0;
    ctx->__ptr = 0;
}

a_void_t a_vec_dtor(a_vec_s *ctx, a_void_t (*dtor)(a_vptr_t))
{
    A_ASSERT(ctx);
    if (ctx->__ptr)
    {
        a_vec_drop_(ctx, 0, dtor);
        free(ctx->__ptr);
        ctx->__ptr = 0;
    }
    ctx->__mem = 0;
    ctx->__siz = 0;
}

a_int_t a_vec_copy(a_vec_s *ctx, const a_vec_s *obj, a_int_t (*dup)(a_vptr_t, a_cptr_t))
{
    A_ASSERT(ctx);
    A_ASSERT(obj);
    ctx->__ptr = malloc(obj->__mem * obj->__siz);
    if (a_unlikely(ctx->__ptr == 0))
    {
        return A_FAILURE;
    }
    ctx->__siz = obj->__siz;
    ctx->__num = obj->__num;
    ctx->__mem = obj->__mem;
    a_size_t size = obj->__num * obj->__siz;
    if (dup)
    {
        a_byte_t *dst = (a_byte_t *)ctx->__ptr;
        a_byte_t *src = (a_byte_t *)obj->__ptr;
        for (a_byte_t *end = src + size; src != end;)
        {
            dup(dst, src);
            dst += ctx->__siz;
            src += ctx->__siz;
        }
    }
    else
    {
        memcpy(ctx->__ptr, obj->__ptr, size);
    }
    return A_SUCCESS;
}

a_vec_s *a_vec_move(a_vec_s *ctx, a_vec_s *obj)
{
    A_ASSERT(ctx);
    A_ASSERT(obj);
    memcpy(ctx, obj, sizeof(*obj));
    memset(obj, 0, sizeof(*obj));
    return ctx;
}

a_void_t a_vec_set(a_vec_s *ctx, a_size_t size, a_void_t (*dtor)(a_vptr_t))
{
    A_ASSERT(ctx);
    size = size ? size : sizeof(a_cast_u);
    a_vec_drop_(ctx, 0, dtor);
    ctx->__mem = ctx->__mem * ctx->__siz / size;
    ctx->__siz = size;
}

a_int_t a_vec_make(a_vec_s *ctx, a_size_t num, a_void_t (*dtor)(a_vptr_t))
{
    A_ASSERT(ctx);
    if (a_unlikely(a_vec_alloc(ctx, num)))
    {
        return A_FAILURE;
    }
    a_vec_drop_(ctx, num, dtor);
    return A_SUCCESS;
}

a_void_t a_vec_drop(a_vec_s *ctx, a_void_t (*dtor)(a_vptr_t))
{
    A_ASSERT(ctx);
    a_vec_drop_(ctx, 0, dtor);
}

a_void_t a_vec_swap(const a_vec_s *ctx, a_size_t lhs, a_size_t rhs)
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

a_void_t a_vec_sort(const a_vec_s *ctx, a_int_t (*cmp)(a_cptr_t, a_cptr_t))
{
    A_ASSERT(ctx);
    qsort(ctx->__ptr, ctx->__num, ctx->__siz, cmp);
}

a_void_t a_vec_sort_fore(const a_vec_s *ctx, a_int_t (*cmp)(a_cptr_t, a_cptr_t))
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

a_void_t a_vec_sort_back(const a_vec_s *ctx, a_int_t (*cmp)(a_cptr_t, a_cptr_t))
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

a_vptr_t a_vec_search(const a_vec_s *ctx, a_cptr_t obj, a_int_t (*cmp)(a_cptr_t, a_cptr_t))
{
    A_ASSERT(ctx);
    return bsearch(obj, ctx->__ptr, ctx->__num, ctx->__siz, cmp);
}

a_vptr_t a_vec_insert(a_vec_s *ctx, a_size_t idx)
{
    A_ASSERT(ctx);
    if (a_unlikely(a_vec_alloc(ctx, ctx->__num)))
    {
        return 0;
    }
    if (idx < ctx->__num)
    {
        a_byte_t *src = (a_byte_t *)ctx->__ptr + ctx->__siz * (idx + 0);
        a_byte_t *dst = (a_byte_t *)ctx->__ptr + ctx->__siz * (idx + 1);
        memmove(dst, src, (ctx->__num - idx) * ctx->__siz);
        ++ctx->__num;
        return src;
    }
    return a_vec_inc_(ctx);
}

a_vptr_t a_vec_push_fore(a_vec_s *ctx) { return a_vec_insert(ctx, 0); }

a_vptr_t a_vec_push_back(a_vec_s *ctx)
{
    A_ASSERT(ctx);
    if (a_unlikely(a_vec_alloc(ctx, ctx->__num)))
    {
        return 0;
    }
    return a_vec_inc_(ctx);
}

a_vptr_t a_vec_remove(a_vec_s *ctx, a_size_t idx)
{
    A_ASSERT(ctx);
    if (ctx->__num && idx < ctx->__num - 1)
    {
        if (a_unlikely(a_vec_alloc(ctx, ctx->__num)))
        {
            return 0;
        }
        a_byte_t *ptr = (a_byte_t *)ctx->__ptr + ctx->__siz * ctx->__num;
        a_byte_t *dst = (a_byte_t *)ctx->__ptr + ctx->__siz * (idx + 0);
        a_byte_t *src = (a_byte_t *)ctx->__ptr + ctx->__siz * (idx + 1);
        memcpy(ptr, dst, ctx->__siz);
        memmove(dst, src, (a_size_t)(ptr - src));
        --ctx->__num;
        return ptr;
    }
    return a_likely(ctx->__num) ? a_vec_dec_(ctx) : 0;
}

a_vptr_t a_vec_pull_fore(a_vec_s *ctx) { return a_vec_remove(ctx, 0); }

a_vptr_t a_vec_pull_back(a_vec_s *ctx)
{
    A_ASSERT(ctx);
    return a_likely(ctx->__num) ? a_vec_dec_(ctx) : 0;
}

#endif /* __STDC_HOSTED__ */
