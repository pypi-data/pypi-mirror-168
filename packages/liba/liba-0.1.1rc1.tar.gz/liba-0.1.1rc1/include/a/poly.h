/*!
 @file poly.h
 @brief polynomial
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#ifndef __A_POLY_H__
#define __A_POLY_H__

#include "a.h"

/*!
 @ingroup A
 @addtogroup A_POLY polynomial
 @{
*/

#if defined(__cplusplus)
extern "C" {
#endif /* __cplusplus */

/*!
 @brief convert between \f$ \sum_{i=0}^{n}a_{i}x^{i} \f$ and \f$ \sum_{i=0}^{n}a_{i}x^{n-i} \f$
*/
A_PUBLIC a_real_t *a_poly_inv(a_real_t *a, a_size_t n);

/*!
 @brief horner function for polynomial \f$ \sum_{i=0}^{n}a_{i}x^{i} \f$
 \f[
  \left\{\begin{array}{l}
  S_n = a_n\\
  S_i = xS_{i+1} + a_i,\quad(i=n-1,n-2,\cdots,1,0)\\
  P(x) = S_0
  \end{array}\right.
 \f]
*/
A_PUBLIC a_real_t a_poly_c(const a_real_t *a, a_size_t n, a_real_t x);

/*!
 @brief horner function for polynomial \f$ \sum_{i=0}^{n}a_{i}x^{n-i} \f$
 @f[
  \left\{\begin{array}{l}
  S_0 = a_0\\
  S_i = xS_{i-1} + a_i,\quad(i=1,2,\cdots,n-1,n)\\
  P(x) = S_n
  \end{array}\right.
 @f]
*/
A_PUBLIC a_real_t a_poly_r(const a_real_t *a, a_size_t n, a_real_t x);

#if defined(__cplusplus)
} /* extern "C" */
#endif /* __cplusplus */

/*! @} A_POLY */

#endif /* __A_POLY_H__ */
