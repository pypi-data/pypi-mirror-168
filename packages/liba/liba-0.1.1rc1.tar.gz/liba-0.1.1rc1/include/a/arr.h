/*!
 @file arr.h
 @brief basic array library
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#ifndef __A_ARR_H__
#define __A_ARR_H__

#include "a.h"

/*!
 @ingroup A
 @addtogroup A_ARR basic array library
 @{
*/

/*!
 @brief instance structure for basic array
*/
typedef struct a_arr_s
{
    a_vptr_t __ptr; /*!< address of memory */
    a_size_t __num; /*!< number of element */
    a_size_t __mem; /*!< memory of element */
    a_size_t __siz; /*!< size of a element */
} a_arr_s;

/*!
 @brief access address of array for a pointer to array structure
 @param[in] ctx points to an instance of array structure
*/
A_INLINE a_vptr_t a_arr_ptr(const a_arr_s *ctx) { return ctx->__ptr; }

/*!
 @brief access number of element for a pointer to array structure
 @param[in] ctx points to an instance of array structure
*/
A_INLINE a_size_t a_arr_num(const a_arr_s *ctx) { return ctx->__num; }

/*!
 @brief access memory of element for a pointer to array structure
 @param[in] ctx points to an instance of array structure
*/
A_INLINE a_size_t a_arr_mem(const a_arr_s *ctx) { return ctx->__mem; }

/*!
 @brief access size of a element for a pointer to array structure
 @param[in] ctx points to an instance of array structure
*/
A_INLINE a_size_t a_arr_get(const a_arr_s *ctx) { return ctx->__siz; }

/*!
 @brief access specified element for a pointer to array structure
 @param[in] ctx points to an instance of array structure
 @param[in] idx index of element less than memory
 @note should check for out of bounds
 @return element pointer
*/
A_INLINE a_vptr_t a_arr_at_(const a_arr_s *ctx, a_size_t idx)
{
    return a_cast_s(a_byte_t *, ctx->__ptr) + ctx->__siz * idx;
}

/*!
 @brief access specified element for a pointer to array structure
 @param[in] ctx points to an instance of array structure
 @param[in] idx index of element less than memory
 @return element pointer
  @retval 0 out of bounds
*/
A_INLINE a_vptr_t a_arr_at(const a_arr_s *ctx, a_size_t idx)
{
    return a_likely(idx < ctx->__mem) ? a_arr_at_(ctx, idx) : A_NULL;
}

/*!
 @brief access top element for a pointer to array structure
 @param[in] ctx points to an instance of array structure
 @note should check if array is empty
 @return element pointer
*/
A_INLINE a_vptr_t a_arr_top_(const a_arr_s *ctx)
{
    return a_cast_s(a_byte_t *, ctx->__ptr) + ctx->__siz * (ctx->__num - 1);
}

/*!
 @brief access top element for a pointer to array structure
 @param[in] ctx points to an instance of array structure
 @return element pointer
  @retval 0 empty array
*/
A_INLINE a_vptr_t a_arr_top(const a_arr_s *ctx)
{
    return a_likely(ctx->__num) ? a_arr_top_(ctx) : A_NULL;
}

/*!
 @brief access end pointer for a pointer to array structure
 @param[in] ctx points to an instance of array structure
*/
A_INLINE a_vptr_t a_arr_end(const a_arr_s *ctx)
{
    return a_cast_s(a_byte_t *, ctx->__ptr) + ctx->__siz * ctx->__num;
}

#if defined(__cplusplus)
extern "C" {
#endif /* __cplusplus */

/*!
 @brief constructor for array structure
 @param[in] ctx points to an instance of array structure
 @param[in] ptr address of memory
 @param[in] siz size of a element
 @param[in] num number of element
*/
A_PUBLIC a_void_t a_arr_ctor(a_arr_s *ctx, a_vptr_t ptr, a_size_t siz, a_size_t num);

/*!
 @brief destructor for array structure
 @param[in] ctx points to an instance of array structure
 @param[in] dtor element destructor
*/
A_PUBLIC a_void_t a_arr_dtor(a_arr_s *ctx, a_void_t (*dtor)(a_vptr_t));

/*!
 @brief initialize a pointer to array structure by moving
 @param[in] ctx points to an instance of array structure
 @param[in] obj input source pointing to an instance
*/
A_PUBLIC a_arr_s *a_arr_move(a_arr_s *ctx, a_arr_s *obj);

/*!
 @brief drop all the elements for a pointer to array structure
 @param[in] ctx points to an instance of array structure
 @param[in] dtor current element destructor
*/
A_PUBLIC a_void_t a_arr_drop(a_arr_s *ctx, a_void_t (*dtor)(a_vptr_t));

/*!
 @brief swap elements lhs and rhs for a pointer to array structure
 @param[in] ctx points to an instance of array structure
 @param[in] lhs element index on the left
 @param[in] rhs element index on the right
*/
A_PUBLIC a_void_t a_arr_swap(const a_arr_s *ctx, a_size_t lhs, a_size_t rhs);

/*!
 @brief sort all elements for a pointer to array structure
 @param[in] ctx points to an instance of array structure
 @param[in] cmp a function that compares two elements
  @arg cmp(lhs,rhs)==0 *lhs is equivalent to *rhs
  @arg cmp(lhs,rhs)<0 *lhs goes before *rhs
  @arg cmp(lhs,rhs)>0 *lhs goes after *rhs
*/
A_PUBLIC a_void_t a_arr_sort(const a_arr_s *ctx, a_int_t (*cmp)(a_cptr_t, a_cptr_t));

/*!
 @brief insert sort foremost element for a pointer to array structure
 @code{.c}
 T *obj = a_arr_push_fore(T, ctx);
 if (obj)
 {
     CTOR(obj);
     INIT(obj);
     a_arr_sort_fore(ctx, cmp);
 }
 @endcode
 @param[in] ctx points to an instance of array structure
 @param[in] cmp a function that compares two elements
  @arg cmp(lhs,rhs)==0 *lhs is equivalent to *rhs
  @arg cmp(lhs,rhs)<0 *lhs goes before *rhs
  @arg cmp(lhs,rhs)>0 *lhs goes after *rhs
*/
A_PUBLIC a_void_t a_arr_sort_fore(const a_arr_s *ctx, a_int_t (*cmp)(a_cptr_t, a_cptr_t));

/*!
 @brief insert sort backmost element for a pointer to array structure
 @code{.c}
 T *obj = a_arr_push_back(T, ctx);
 if (obj)
 {
     CTOR(obj);
     INIT(obj);
     a_arr_sort_back(ctx, cmp);
 }
 @endcode
 @param[in] ctx points to an instance of array structure
 @param[in] cmp a function that compares two elements
  @arg cmp(lhs,rhs)==0 *lhs is equivalent to *rhs
  @arg cmp(lhs,rhs)<0 *lhs goes before *rhs
  @arg cmp(lhs,rhs)>0 *lhs goes after *rhs
*/
A_PUBLIC a_void_t a_arr_sort_back(const a_arr_s *ctx, a_int_t (*cmp)(a_cptr_t, a_cptr_t));

/*!
 @brief search the given element in this array
 @param[in] ctx points to an instance of array structure
 @param[in] obj object that serves as key for the search
 @param[in] cmp a function that compares two elements
  @arg cmp(lhs,rhs)==0 *lhs is equivalent to *rhs
  @arg cmp(lhs,rhs)<0 *lhs goes before *rhs
  @arg cmp(lhs,rhs)>0 *lhs goes after *rhs
 @return matching element pointer
  @retval 0 failure
*/
A_PUBLIC a_vptr_t a_arr_search(const a_arr_s *ctx, a_cptr_t obj, a_int_t (*cmp)(a_cptr_t, a_cptr_t));

/*!
 @brief insert an element into the array
 @param[in] ctx points to an instance of array structure
 @param[in] idx index of element in this array
  @arg 0 @ref a_arr_push_fore
  @arg n @ref a_arr_push_back
 @return element pointer
  @retval 0 failure
*/
A_PUBLIC a_vptr_t a_arr_insert(a_arr_s *ctx, a_size_t idx);

/*!
 @brief remove an element from the array
 @param[in] ctx points to an instance of array structure
 @param[in] idx index of element in this array
  @arg 0 @ref a_arr_pull_fore
  @arg n @ref a_arr_pull_back
 @return element pointer
  @retval 0 failure
*/
A_PUBLIC a_vptr_t a_arr_remove(a_arr_s *ctx, a_size_t idx);

/*!
 @brief push an element into the array forward
 @param[in] ctx points to an instance of array structure
 @return element pointer
  @retval 0 failure
*/
A_PUBLIC a_vptr_t a_arr_push_fore(a_arr_s *ctx);

/*!
 @brief push an element into the array backward
 @param[in] ctx points to an instance of array structure
 @return element pointer
  @retval 0 failure
*/
A_PUBLIC a_vptr_t a_arr_push_back(a_arr_s *ctx);

/*!
 @brief pull an element from the array forward
 @param[in] ctx points to an instance of array structure
 @return element pointer
  @retval 0 failure
*/
A_PUBLIC a_vptr_t a_arr_pull_fore(a_arr_s *ctx);

/*!
 @brief pull an element from the array backward
 @param[in] ctx points to an instance of array structure
 @return element pointer
  @retval 0 failure
*/
A_PUBLIC a_vptr_t a_arr_pull_back(a_arr_s *ctx);

#if defined(__cplusplus)
} /* extern "C" */
#endif /* __cplusplus */

/*!
 @brief push an element into the array
 @param[in] ctx points to an instance of array structure
 @return element pointer
  @retval 0 failure
*/
A_INLINE a_vptr_t a_arr_push(a_arr_s *ctx) { return a_arr_push_back(ctx); }

/*!
 @brief pull an element from the array
 @param[in] ctx points to an instance of array structure
 @return element pointer
  @retval 0 failure
*/
A_INLINE a_vptr_t a_arr_pull(a_arr_s *ctx) { return a_arr_pull_back(ctx); }

/*!
 @brief iterate over a array
 @code{.c}
 a_arr_forenum(i, ctx)
 {
     T *it = (T *)a_arr_at(ctx, i);
     assert(a_arr_get(ctx) == sizeof(*it));
 }
 @endcode
 @param i index of elements in the array
 @param ctx points to an instance of array structure
*/
#define a_arr_forenum(i, ctx) a_forenum(a_size_t, i, (ctx)->__num)

/*!
 @brief iterate over a array in reverse
 @code{.c}
 a_arr_forenum_reverse(i, ctx)
 {
     T *it = (T *)a_arr_at(ctx, i);
     assert(a_arr_get(ctx) == sizeof(*it));
 }
 @endcode
 @param i index of elements in the array
 @param ctx points to an instance of array structure
*/
#define a_arr_forenum_reverse(i, ctx) a_forenum_reverse(a_size_t, i, (ctx)->__num)

/*!
 @brief iterate over a array
 @code{.c}
 a_arr_foreach(T, it, ctx)
 {
     assert(a_arr_get(ctx) == sizeof(*it));
 }
 @endcode
 @param T type of elements in the array
 @param it the &a_arr_s to use as a loop counter
 @param ctx points to an instance of array structure
*/
#define a_arr_foreach(T, it, ctx) a_foreach(T, it, (ctx)->__ptr, (ctx)->__num)

/*!
 @brief iterate over a array in reverse
 @code{.c}
 a_arr_foreach_reverse(T, it, ctx)
 {
     assert(a_arr_get(ctx) == sizeof(*it));
 }
 @endcode
 @param T type of elements in the array
 @param it the &a_arr_s to use as a loop counter
 @param ctx points to an instance of array structure
*/
#define a_arr_foreach_reverse(T, it, ctx) a_foreach_reverse(T, it, (ctx)->__ptr, (ctx)->__num)

#if defined(__clang__)
#pragma GCC diagnostic ignored "-Wdisabled-macro-expansion"
#endif /* __clang__ */

#define a_arr_ptr(T, ctx) a_cast_s(T *, a_arr_ptr(ctx))
#define a_arr_end(T, ctx) a_cast_s(T *, a_arr_end(ctx))
#define a_arr_top(T, ctx) a_cast_s(T *, a_arr_top(ctx))
#define a_arr_top_(T, ctx) a_cast_s(T *, a_arr_top_(ctx))
#define a_arr_at(T, ctx, idx) a_cast_s(T *, a_arr_at(ctx, idx))
#define a_arr_at_(T, ctx, idx) a_cast_s(T *, a_arr_at_(ctx, idx))
#define a_arr_search(T, ctx, obj, cmp) a_cast_s(T *, a_arr_search(ctx, obj, cmp))
#define a_arr_insert(T, ctx, idx) a_cast_s(T *, a_arr_insert(ctx, idx))
#define a_arr_remove(T, ctx, idx) a_cast_s(T *, a_arr_remove(ctx, idx))
#define a_arr_push_fore(T, ctx) a_cast_s(T *, a_arr_push_fore(ctx))
#define a_arr_push_back(T, ctx) a_cast_s(T *, a_arr_push_back(ctx))
#define a_arr_pull_fore(T, ctx) a_cast_s(T *, a_arr_pull_fore(ctx))
#define a_arr_pull_back(T, ctx) a_cast_s(T *, a_arr_pull_back(ctx))
#define a_arr_push(T, ctx) a_cast_s(T *, a_arr_push(ctx))
#define a_arr_pull(T, ctx) a_cast_s(T *, a_arr_pull(ctx))

/*! @} A_ARR */

#endif /* __A_ARR_H__ */
