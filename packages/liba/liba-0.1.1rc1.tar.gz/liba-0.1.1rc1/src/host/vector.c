/*!
 @file vector.c
 @brief basic vector library
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#if __STDC_HOSTED__

#include "a/host/vector.h"
#include <assert.h>
#include <string.h>

#undef a_vector_at
#undef a_vector_at_
#undef a_vector_ptr
#undef a_vector_end
#undef a_vector_top
#undef a_vector_top_
#undef a_vector_push
#undef a_vector_pull
#undef a_vector_search
#undef a_vector_insert
#undef a_vector_remove
#undef a_vector_push_fore
#undef a_vector_push_back
#undef a_vector_pull_fore
#undef a_vector_pull_back

A_ALWAYS a_vptr_t a_vector_inc_(a_vector_s *ctx)
{
    a_vptr_t last = ctx->__tail;
    ctx->__tail = (a_byte_t *)ctx->__tail + ctx->__size;
    return (void)(++ctx->__num), last;
}

A_ALWAYS a_vptr_t a_vector_dec_(a_vector_s *ctx)
{
    ctx->__tail = (a_byte_t *)ctx->__tail - ctx->__size;
    return (void)(--ctx->__num), ctx->__tail;
}

A_STATIC a_void_t a_vector_drop_(a_vector_s *ctx, a_size_t bot)
{
    if (ctx->dtor)
    {
        while (ctx->__num > bot)
        {
            ctx->dtor(a_vector_dec_(ctx));
        }
    }
    ctx->__tail = (a_byte_t *)(ctx->__head) + ctx->__size * bot;
    ctx->__num = bot;
}

A_STATIC a_int_t a_vector_alloc(a_vector_s *ctx, a_size_t num)
{
    if (ctx->__mem <= num)
    {
        a_size_t mem = ctx->__mem;
        do
        {
            mem += (mem >> 1) + 1;
        } while (mem < num);
        a_size_t mem_ = mem * ctx->__size;
        a_size_t num_ = ctx->__num * ctx->__size;
        a_size_t size = a_align(sizeof(a_vptr_t), mem_);
        a_vptr_t head = realloc(ctx->__head, size);
        if (a_unlikely(head == 0))
        {
            return A_FAILURE;
        }
        ctx->__mem = mem;
        ctx->__head = head;
        ctx->__tail = (a_byte_t *)head + num_;
        ctx->__last = (a_byte_t *)head + mem_;
    }
    return A_SUCCESS;
}

a_vector_s *a_vector_new(a_size_t size,
                         a_void_t (*ctor)(a_vptr_t),
                         a_void_t (*dtor)(a_vptr_t))
{
    a_vector_s *ctx = (a_vector_s *)malloc(sizeof(a_vector_s));
    if (ctx)
    {
        a_vector_ctor(ctx, size, ctor, dtor);
    }
    return ctx;
}

a_void_t a_vector_die(a_vector_s *ctx)
{
    if (ctx)
    {
        a_vector_dtor(ctx);
        free(ctx);
    }
}

a_void_t a_vector_ctor(a_vector_s *ctx, a_size_t size,
                       a_void_t (*ctor)(a_vptr_t),
                       a_void_t (*dtor)(a_vptr_t))
{
    A_ASSERT(ctx);
    ctx->__size = size ? size : sizeof(a_cast_u);
    ctx->ctor = ctor;
    ctx->dtor = dtor;
    ctx->__last = 0;
    ctx->__tail = 0;
    ctx->__head = 0;
    ctx->__num = 0;
    ctx->__mem = 0;
}

a_void_t a_vector_dtor(a_vector_s *ctx)
{
    A_ASSERT(ctx);
    if (ctx->__head)
    {
        a_vector_drop_(ctx, 0);
        free(ctx->__head);
        ctx->__head = 0;
    }
    ctx->__tail = 0;
    ctx->__last = 0;
    ctx->__size = 0;
    ctx->__mem = 0;
}

a_int_t a_vector_copy(a_vector_s *ctx, const a_vector_s *obj, a_int_t (*dup)(a_vptr_t, a_cptr_t))
{
    A_ASSERT(ctx);
    A_ASSERT(obj);
    a_size_t num_ = obj->__num * obj->__size;
    a_size_t mem_ = obj->__mem * obj->__size;
    ctx->__head = malloc(mem_);
    if (a_unlikely(ctx->__head == 0))
    {
        return A_FAILURE;
    }
    ctx->ctor = obj->ctor;
    ctx->dtor = obj->dtor;
    ctx->__num = obj->__num;
    ctx->__mem = obj->__mem;
    ctx->__size = obj->__size;
    ctx->__tail = (a_byte_t *)ctx->__head + num_;
    ctx->__last = (a_byte_t *)ctx->__head + mem_;
    if (dup)
    {
        a_byte_t *dst = (a_byte_t *)ctx->__head;
        a_byte_t *src = (a_byte_t *)obj->__head;
        while (src != obj->__tail)
        {
            dup(dst, src);
            dst += obj->__size;
            src += obj->__size;
        }
    }
    else
    {
        memcpy(ctx->__head, obj->__head, num_);
    }
    return A_SUCCESS;
}

a_vector_s *a_vector_move(a_vector_s *ctx, a_vector_s *obj)
{
    A_ASSERT(ctx);
    A_ASSERT(obj);
    memcpy(ctx, obj, sizeof(*obj));
    memset(obj, 0, sizeof(*obj));
    return ctx;
}

a_void_t a_vector_set(a_vector_s *ctx, a_size_t size,
                      a_void_t (*ctor)(a_vptr_t),
                      a_void_t (*dtor)(a_vptr_t))
{
    A_ASSERT(ctx);
    size = size ? size : sizeof(a_cast_u);
    a_vector_drop_(ctx, 0);
    ctx->__mem = ctx->__mem * ctx->__size / size;
    ctx->__size = size;
    ctx->ctor = ctor;
    ctx->dtor = dtor;
}

a_int_t a_vector_make(a_vector_s *ctx, a_size_t num)
{
    A_ASSERT(ctx);
    if (a_unlikely(a_vector_alloc(ctx, num)))
    {
        return A_FAILURE;
    }
    a_vector_drop_(ctx, num);
    return A_SUCCESS;
}

a_void_t a_vector_drop(a_vector_s *ctx)
{
    A_ASSERT(ctx);
    a_vector_drop_(ctx, 0);
}

a_void_t a_vector_swap(const a_vector_s *ctx, a_size_t lhs, a_size_t rhs)
{
    A_ASSERT(ctx);
    a_size_t num = ctx->__num - 1;
    lhs = lhs < ctx->__num ? lhs : num;
    rhs = rhs < ctx->__num ? rhs : num;
    if (lhs != rhs)
    {
        a_byte_t *ptr = (a_byte_t *)ctx->__head;
        a_vptr_t lobj = ptr + lhs * ctx->__size;
        a_vptr_t robj = ptr + rhs * ctx->__size;
        a_swap(ctx->__size, lobj, robj);
    }
}

a_void_t a_vector_sort(const a_vector_s *ctx, a_int_t (*cmp)(a_cptr_t, a_cptr_t))
{
    A_ASSERT(ctx);
    qsort(ctx->__head, ctx->__num, ctx->__size, cmp);
}

a_void_t a_vector_sort_fore(const a_vector_s *ctx, a_int_t (*cmp)(a_cptr_t, a_cptr_t))
{
    A_ASSERT(ctx);
    if (ctx->__num > 1)
    {
        a_byte_t *ptr = (a_byte_t *)ctx->__head;
        a_byte_t *end = (a_byte_t *)ctx->__tail - ctx->__size;
        do
        {
            a_byte_t *cur = ptr + ctx->__size;
            if (cmp(ptr, cur) > 0)
            {
                a_swap(ctx->__size, cur, ptr);
            }
            else
            {
                break;
            }
            ptr = cur;
        } while (ptr != end);
    }
}

a_void_t a_vector_sort_back(const a_vector_s *ctx, a_int_t (*cmp)(a_cptr_t, a_cptr_t))
{
    A_ASSERT(ctx);
    if (ctx->__num > 1)
    {
        a_byte_t *ptr = (a_byte_t *)ctx->__tail - ctx->__size;
        do
        {
            a_byte_t *cur = ptr - ctx->__size;
            if (cmp(cur, ptr) > 0)
            {
                a_swap(ctx->__size, cur, ptr);
            }
            else
            {
                break;
            }
            ptr = cur;
        } while (ptr != ctx->__head);
    }
}

a_vptr_t a_vector_search(const a_vector_s *ctx, a_cptr_t obj, a_int_t (*cmp)(a_cptr_t, a_cptr_t))
{
    A_ASSERT(ctx);
    return bsearch(obj, ctx->__head, ctx->__num, ctx->__size, cmp);
}

a_vptr_t a_vector_insert(a_vector_s *ctx, a_size_t idx)
{
    A_ASSERT(ctx);
    if (a_unlikely(a_vector_alloc(ctx, ctx->__num)))
    {
        return 0;
    }
    if (idx < ctx->__num)
    {
        a_byte_t *ptr = (a_byte_t *)ctx->__tail;
        a_byte_t *src = (a_byte_t *)ctx->__head + ctx->__size * (idx + 0);
        a_byte_t *dst = (a_byte_t *)ctx->__head + ctx->__size * (idx + 1);
        memmove(dst, src, (a_size_t)(ptr - src));
        a_vector_inc_(ctx);
        if (ctx->ctor)
        {
            ctx->ctor(src);
        }
        return src;
    }
    a_vptr_t obj = a_vector_inc_(ctx);
    if (ctx->ctor)
    {
        ctx->ctor(obj);
    }
    return obj;
}

a_vptr_t a_vector_push_fore(a_vector_s *ctx) { return a_vector_insert(ctx, 0); }

a_vptr_t a_vector_push_back(a_vector_s *ctx)
{
    A_ASSERT(ctx);
    if (a_unlikely(a_vector_alloc(ctx, ctx->__num)))
    {
        return 0;
    }
    a_vptr_t obj = a_vector_inc_(ctx);
    if (ctx->ctor)
    {
        ctx->ctor(obj);
    }
    return obj;
}

a_vptr_t a_vector_remove(a_vector_s *ctx, a_size_t idx)
{
    A_ASSERT(ctx);
    if (ctx->__num && idx < ctx->__num - 1)
    {
        if (a_unlikely(a_vector_alloc(ctx, ctx->__num)))
        {
            return 0;
        }
        a_byte_t *ptr = (a_byte_t *)ctx->__tail;
        a_byte_t *dst = (a_byte_t *)ctx->__head + ctx->__size * (idx + 0);
        a_byte_t *src = (a_byte_t *)ctx->__head + ctx->__size * (idx + 1);
        memcpy(ptr, dst, ctx->__size);
        memmove(dst, src, (a_size_t)(ptr - src));
        a_vector_dec_(ctx);
        return ptr;
    }
    return a_likely(ctx->__head != ctx->__tail) ? a_vector_dec_(ctx) : 0;
}

a_vptr_t a_vector_pull_fore(a_vector_s *ctx) { return a_vector_remove(ctx, 0); }

a_vptr_t a_vector_pull_back(a_vector_s *ctx)
{
    A_ASSERT(ctx);
    return a_likely(ctx->__head != ctx->__tail) ? a_vector_dec_(ctx) : 0;
}

#endif /* __STDC_HOSTED__ */
