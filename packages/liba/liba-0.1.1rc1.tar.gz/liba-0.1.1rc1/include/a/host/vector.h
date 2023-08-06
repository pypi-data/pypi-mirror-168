/*!
 @file vector.h
 @brief basic vector library
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#ifndef __A_HOST_VECTOR_H__
#define __A_HOST_VECTOR_H__

#include "../a.h"

#if __STDC_HOSTED__

#include <stdlib.h>

/*!
 @ingroup A
 @addtogroup A_VECTOR basic vector library
 @{
*/

/*!
 @brief instance structure for basic vector
*/
typedef struct a_vector_s
{
    a_void_t (*ctor)(a_vptr_t); /*!< element constructor */
    a_void_t (*dtor)(a_vptr_t); /*!< element destructor */
    a_vptr_t __head; /*!< head address */
    a_vptr_t __tail; /*!< tail address */
    a_vptr_t __last; /*!< last address */
    a_size_t __size; /*!< size element */
    a_size_t __num; /*!< count number */
    a_size_t __mem; /*!< count memory */
} a_vector_s;

/*!
 @brief access vector head pointer for a pointer to vector structure
 @param[in] ctx points to an instance of vector structure
*/
A_INLINE a_vptr_t a_vector_ptr(const a_vector_s *ctx) { return ctx->__head; }

/*!
 @brief access vector tail pointer for a pointer to vector structure
 @param[in] ctx points to an instance of vector structure
*/
A_INLINE a_vptr_t a_vector_end(const a_vector_s *ctx) { return ctx->__tail; }

/*!
 @brief access size of a element for a pointer to vector structure
 @param[in] ctx points to an instance of vector structure
*/
A_INLINE a_size_t a_vector_get(const a_vector_s *ctx) { return ctx->__size; }

/*!
 @brief access number of element for a pointer to vector structure
 @param[in] ctx points to an instance of vector structure
*/
A_INLINE a_size_t a_vector_num(const a_vector_s *ctx) { return ctx->__num; }

/*!
 @brief access capacity of element for a pointer to vector structure
 @param[in] ctx points to an instance of vector structure
*/
A_INLINE a_size_t a_vector_mem(const a_vector_s *ctx) { return ctx->__mem; }

/*!
 @brief access specified element for a pointer to vector structure
 @param[in] ctx points to an instance of vector structure
 @param[in] idx index of element less than capacity
 @note should check for out of bounds
 @return element pointer
*/
A_INLINE a_vptr_t a_vector_at_(const a_vector_s *ctx, a_size_t idx)
{
    return a_cast_s(a_byte_t *, ctx->__head) + ctx->__size * idx;
}

/*!
 @brief access specified element for a pointer to vector structure
 @param[in] ctx points to an instance of vector structure
 @param[in] idx index of element less than capacity
 @return element pointer
  @retval 0 out of bounds
*/
A_INLINE a_vptr_t a_vector_at(const a_vector_s *ctx, a_size_t idx)
{
    return a_likely(idx < ctx->__mem) ? a_vector_at_(ctx, idx) : A_NULL;
}

/*!
 @brief access top element for a pointer to vector structure
 @param[in] ctx points to an instance of vector structure
 @note should check if vector is empty
 @return element pointer
*/
A_INLINE a_vptr_t a_vector_top_(const a_vector_s *ctx)
{
    return a_cast_s(a_byte_t *, ctx->__tail) - ctx->__size;
}

/*!
 @brief access top element for a pointer to vector structure
 @param[in] ctx points to an instance of vector structure
 @return element pointer
  @retval 0 empty vector
*/
A_INLINE a_vptr_t a_vector_top(const a_vector_s *ctx)
{
    return a_likely(ctx->__num) ? a_vector_top_(ctx) : A_NULL;
}

#if defined(__cplusplus)
extern "C" {
#endif /* __cplusplus */

/*!
 @brief allocate a pointer to vector structure from memory
 @param[in] size the size of the element
 @param[in] ctor element constructor
 @param[in] dtor element destructor
*/
A_PUBLIC a_vector_s *a_vector_new(a_size_t size,
                                  a_void_t (*ctor)(a_vptr_t),
                                  a_void_t (*dtor)(a_vptr_t));

/*!
 @brief deallocate a pointer to vector structure
 @param[in] ctx points to an instance of vector structure
*/
A_PUBLIC a_void_t a_vector_die(a_vector_s *ctx);

/*!
 @brief constructor for vector structure
 @param[in] ctx points to an instance of vector structure
 @param[in] size the size of the element
 @param[in] ctor element constructor
 @param[in] dtor element destructor
*/
A_PUBLIC a_void_t a_vector_ctor(a_vector_s *ctx, a_size_t size,
                                a_void_t (*ctor)(a_vptr_t),
                                a_void_t (*dtor)(a_vptr_t));

/*!
 @brief destructor for vector structure
 @param[in] ctx points to an instance of vector structure
*/
A_PUBLIC a_void_t a_vector_dtor(a_vector_s *ctx);

/*!
 @brief initialize a pointer to vector structure by copying
 @param[in] ctx points to an instance of vector structure
 @param[in] obj input source pointing to an instance
 @param[in] dup a function that copies elements
  @arg 0 use function memcpy to copy elements
 @return the execution state of the function
  @retval 0 success
  @retval 1 failure
*/
A_PUBLIC a_int_t a_vector_copy(a_vector_s *ctx, const a_vector_s *obj, a_int_t (*dup)(a_vptr_t, a_cptr_t));

/*!
 @brief initialize a pointer to vector structure by moving
 @param[in] ctx points to an instance of vector structure
 @param[in] obj input source pointing to an instance
*/
A_PUBLIC a_vector_s *a_vector_move(a_vector_s *ctx, a_vector_s *obj);

/*!
 @brief modify size of a element for a pointer to vector structure
 @param[in] ctx points to an instance of vector structure
 @param[in] size the size of the new element
 @param[in] ctor current element constructor
 @param[in] dtor current element destructor
*/
A_PUBLIC a_void_t a_vector_set(a_vector_s *ctx, a_size_t size,
                               a_void_t (*ctor)(a_vptr_t),
                               a_void_t (*dtor)(a_vptr_t));

/*!
 @brief modify element number for a pointer to string structure
 @param[in] ctx points to an instance of string structure
 @param[in] num number of all elements in the vector
 @return the execution state of the function
  @retval 0 success
  @retval 1 failure
*/
A_PUBLIC a_int_t a_vector_make(a_vector_s *ctx, a_size_t num);

/*!
 @brief drop all the elements for a pointer to vector structure
 @param[in] ctx points to an instance of vector structure
*/
A_PUBLIC a_void_t a_vector_drop(a_vector_s *ctx);

/*!
 @brief swap elements lhs and rhs for a pointer to vector structure
 @param[in] ctx points to an instance of vector structure
 @param[in] lhs element index on the left
 @param[in] rhs element index on the right
*/
A_PUBLIC a_void_t a_vector_swap(const a_vector_s *ctx, a_size_t lhs, a_size_t rhs);

/*!
 @brief sort all elements for a pointer to vector structure
 @param[in] ctx points to an instance of vector structure
 @param[in] cmp a function that compares two elements
  @arg cmp(lhs,rhs)==0 *lhs is equivalent to *rhs
  @arg cmp(lhs,rhs)<0 *lhs goes before *rhs
  @arg cmp(lhs,rhs)>0 *lhs goes after *rhs
*/
A_PUBLIC a_void_t a_vector_sort(const a_vector_s *ctx, a_int_t (*cmp)(a_cptr_t, a_cptr_t));

/*!
 @brief insert sort foremost element for a pointer to vector structure
 @code{.c}
 T *obj = a_vector_push_fore(T, ctx);
 if (obj)
 {
     CTOR(obj);
     INIT(obj);
     a_vector_sort_fore(ctx, cmp);
 }
 @endcode
 @param[in] ctx points to an instance of vector structure
 @param[in] cmp a function that compares two elements
  @arg cmp(lhs,rhs)==0 *lhs is equivalent to *rhs
  @arg cmp(lhs,rhs)<0 *lhs goes before *rhs
  @arg cmp(lhs,rhs)>0 *lhs goes after *rhs
*/
A_PUBLIC a_void_t a_vector_sort_fore(const a_vector_s *ctx, a_int_t (*cmp)(a_cptr_t, a_cptr_t));

/*!
 @brief insert sort backmost element for a pointer to vector structure
 @code{.c}
 T *obj = a_vector_push_back(T, ctx);
 if (obj)
 {
     CTOR(obj);
     INIT(obj);
     a_vector_sort_back(ctx, cmp);
 }
 @endcode
 @param[in] ctx points to an instance of vector structure
 @param[in] cmp a function that compares two elements
  @arg cmp(lhs,rhs)==0 *lhs is equivalent to *rhs
  @arg cmp(lhs,rhs)<0 *lhs goes before *rhs
  @arg cmp(lhs,rhs)>0 *lhs goes after *rhs
*/
A_PUBLIC a_void_t a_vector_sort_back(const a_vector_s *ctx, a_int_t (*cmp)(a_cptr_t, a_cptr_t));

/*!
 @brief search the given element in this vector
 @param[in] ctx points to an instance of vector structure
 @param[in] obj object that serves as key for the search
 @param[in] cmp a function that compares two elements
  @arg cmp(lhs,rhs)==0 *lhs is equivalent to *rhs
  @arg cmp(lhs,rhs)<0 *lhs goes before *rhs
  @arg cmp(lhs,rhs)>0 *lhs goes after *rhs
 @return matching element pointer
  @retval 0 failure
*/
A_PUBLIC a_vptr_t a_vector_search(const a_vector_s *ctx, a_cptr_t obj, a_int_t (*cmp)(a_cptr_t, a_cptr_t));

/*!
 @brief insert an element into the vector
 @param[in] ctx points to an instance of vector structure
 @param[in] idx index of element in this vector
  @arg 0 @ref a_vector_push_fore
  @arg n @ref a_vector_push_back
 @return element pointer
  @retval 0 failure
*/
A_PUBLIC a_vptr_t a_vector_insert(a_vector_s *ctx, a_size_t idx);

/*!
 @brief remove an element from the vector
 @param[in] ctx points to an instance of vector structure
 @param[in] idx index of element in this vector
  @arg 0 @ref a_vector_pull_fore
  @arg n @ref a_vector_pull_back
 @return element pointer
  @retval 0 failure
*/
A_PUBLIC a_vptr_t a_vector_remove(a_vector_s *ctx, a_size_t idx);

/*!
 @brief push an element into the vector forward
 @param[in] ctx points to an instance of vector structure
 @return element pointer
  @retval 0 failure
*/
A_PUBLIC a_vptr_t a_vector_push_fore(a_vector_s *ctx);

/*!
 @brief push an element into the vector backward
 @param[in] ctx points to an instance of vector structure
 @return element pointer
  @retval 0 failure
*/
A_PUBLIC a_vptr_t a_vector_push_back(a_vector_s *ctx);

/*!
 @brief pull an element from the vector forward
 @param[in] ctx points to an instance of vector structure
 @return element pointer
  @retval 0 failure
*/
A_PUBLIC a_vptr_t a_vector_pull_fore(a_vector_s *ctx);

/*!
 @brief pull an element from the vector backward
 @param[in] ctx points to an instance of vector structure
 @return element pointer
  @retval 0 failure
*/
A_PUBLIC a_vptr_t a_vector_pull_back(a_vector_s *ctx);

#if defined(__cplusplus)
} /* extern "C" */
#endif /* __cplusplus */

/*!
 @brief push an element into the vector
 @param[in] ctx points to an instance of vector structure
 @return element pointer
  @retval 0 failure
*/
A_INLINE a_vptr_t a_vector_push(a_vector_s *ctx) { return a_vector_push_back(ctx); }

/*!
 @brief pull an element from the vector
 @param[in] ctx points to an instance of vector structure
 @return element pointer
  @retval 0 failure
*/
A_INLINE a_vptr_t a_vector_pull(a_vector_s *ctx) { return a_vector_pull_back(ctx); }

/*!
 @brief iterate over a vector
 @code{.c}
 a_vector_forenum(i, ctx)
 {
     T *it = (T *)a_vector_at(ctx, i);
     assert(a_vector_get(ctx) == sizeof(*it));
 }
 @endcode
 @param i index of elements in the vector
 @param ctx points to an instance of vector structure
*/
#define a_vector_forenum(i, ctx) a_forenum(a_size_t, i, (ctx)->__num)

/*!
 @brief iterate over a vector in reverse
 @code{.c}
 a_vector_forenum_reverse(i, ctx)
 {
     T *it = (T *)a_vector_at(ctx, i);
     assert(a_vector_get(ctx) == sizeof(*it));
 }
 @endcode
 @param i index of elements in the vector
 @param ctx points to an instance of vector structure
*/
#define a_vector_forenum_reverse(i, ctx) a_forenum_reverse(a_size_t, i, (ctx)->__num)

/*!
 @brief iterate over a vector
 @code{.c}
 a_vector_foreach(T, it, ctx)
 {
     assert(a_vector_get(ctx) == sizeof(*it));
 }
 @endcode
 @param T type of elements in the vector
 @param it the &a_vector_s to use as a loop counter
 @param ctx points to an instance of vector structure
*/
#define a_vector_foreach(T, it, ctx) a_iterate(T, it, (ctx)->__head, (ctx)->__tail)

/*!
 @brief iterate over a vector in reverse
 @code{.c}
 a_vector_foreach_reverse(T, it, ctx)
 {
     assert(a_vector_get(ctx) == sizeof(*it));
 }
 @endcode
 @param T type of elements in the vector
 @param it the &a_vector_s to use as a loop counter
 @param ctx points to an instance of vector structure
*/
#define a_vector_foreach_reverse(T, it, ctx) a_iterate_reverse(T, it, (ctx)->__head, (ctx)->__tail)

#if defined(__clang__)
#pragma GCC diagnostic ignored "-Wdisabled-macro-expansion"
#endif /* __clang__ */

#define a_vector_ptr(T, ctx) a_cast_s(T *, a_vector_ptr(ctx))
#define a_vector_end(T, ctx) a_cast_s(T *, a_vector_end(ctx))
#define a_vector_top(T, ctx) a_cast_s(T *, a_vector_top(ctx))
#define a_vector_top_(T, ctx) a_cast_s(T *, a_vector_top_(ctx))
#define a_vector_at(T, ctx, idx) a_cast_s(T *, a_vector_at(ctx, idx))
#define a_vector_at_(T, ctx, idx) a_cast_s(T *, a_vector_at_(ctx, idx))
#define a_vector_search(T, ctx, obj, cmp) a_cast_s(T *, a_vector_search(ctx, obj, cmp))
#define a_vector_insert(T, ctx, idx) a_cast_s(T *, a_vector_insert(ctx, idx))
#define a_vector_remove(T, ctx, idx) a_cast_s(T *, a_vector_remove(ctx, idx))
#define a_vector_push_fore(T, ctx) a_cast_s(T *, a_vector_push_fore(ctx))
#define a_vector_push_back(T, ctx) a_cast_s(T *, a_vector_push_back(ctx))
#define a_vector_pull_fore(T, ctx) a_cast_s(T *, a_vector_pull_fore(ctx))
#define a_vector_pull_back(T, ctx) a_cast_s(T *, a_vector_pull_back(ctx))
#define a_vector_push(T, ctx) a_cast_s(T *, a_vector_push(ctx))
#define a_vector_pull(T, ctx) a_cast_s(T *, a_vector_pull(ctx))

/*! @} A_VECTOR */

#endif /* __STDC_HOSTED__ */

#endif /* __A_HOST_VECTOR_H__ */
