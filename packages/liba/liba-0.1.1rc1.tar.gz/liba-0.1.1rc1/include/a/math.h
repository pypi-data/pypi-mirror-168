/*!
 @file math.h
 @brief mathematical algorithm library
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#ifndef __A_MATH_H__
#define __A_MATH_H__

#include "a.h"

/*!
 @ingroup A
 @addtogroup A_MATH mathematical algorithm library
 @{
*/

/*! @brief \f$ e \f$ */
#define A_E 2.71828182845904523536
/*! @brief \f$ \log_{2}{e}=\frac{1}{\ln{2}} \f$ */
#define A_LOG2E 1.44269504088896340736
/*! @brief \f$ \lg{e}=\frac{1}{\ln{2}+\ln{5}} \f$ */
#define A_LOG10E 0.434294481903251827651
/*! @brief \f$ \ln{2} \f$ */
#define A_LN2 0.693147180559945309417
/*! @brief \f$ \ln{10} \f$ */
#define A_LN10 2.30258509299404568402
/*! @brief \f$ \pi \f$ */
#define A_PI 3.14159265358979323846
/*! @brief \f$ \frac{\pi}{2} \f$ */
#define A_PI_2 1.57079632679489661923
/*! @brief \f$ \frac{\pi}{4} \f$ */
#define A_PI_4 0.785398163397448309616
/*! @brief \f$ \frac{1}{\pi} \f$ */
#define A_1_PI 0.318309886183790671538
/*! @brief \f$ \frac{2}{\pi} \f$ */
#define A_2_PI 0.636619772367581343076
/*! @brief \f$ \frac{2}{\sqrt{\pi}} \f$ */
#define A_2_SQRTPI 1.12837916709551257390
/*! @brief \f$ \sqrt{2} \f$ */
#define A_SQRT2 1.41421356237309504880
/*! @brief \f$ \frac{1}{\sqrt{2}}=\frac{\sqrt{2}}{2} \f$ */
#define A_SQRT1_2 0.707106781186547524401

/*!
 @brief expands to a floating-point constant expression
 having the value specified by its argument and the type double
*/
#define A_DBL_C(X) (X)
/*!
 @brief expands to a floating-point constant expression
 having the value specified by its argument and the type float
*/
#define A_FLT_C(X) (X##F)
/*!
 @brief expands to a floating-point constant expression
 having the value specified by its argument and the type long double
*/
#define A_LDBL_C(X) (X##L)

/*!
 @brief expands to a floating-point function expression
 having the value specified by its argument and the type double
*/
#define A_DBL_F(F, ...) F(__VA_ARGS__)
/*!
 @brief expands to a floating-point function expression
 having the value specified by its argument and the type float
*/
#define A_FLT_F(F, ...) F##f(__VA_ARGS__)
/*!
 @brief expands to a floating-point function expression
 having the value specified by its argument and the type long double
*/
#define A_LDBL_F(F, ...) F##l(__VA_ARGS__)

/*!
 @brief square of x, \f$ x^2 \f$
*/
#define A_SQ(x) ((x) * (x))

/*!
 @brief absolute value of x, \f$ |x| \f$
*/
#define A_ABS(x) ((x) < 0 ? -(x) : (x))

/*!
 @brief signum function, \f$ \texttt{sgn}{x}=\begin{cases}+1&x>0\\0&0\\-1&x<0\end{cases} \f$
*/
#define A_SGN(x) ((0 < (x)) - ((x) < 0))

#if defined(__cplusplus)
extern "C" {
#endif /* __cplusplus */

/*!
 @brief fast inverse square-root, \f$ \frac{1}{\sqrt{x}} \f$
 @details http://en.wikipedia.org/wiki/Fast_inverse_square_root
 @param[in] x independent variable
*/
A_PUBLIC a_f32_t a_inv_sqrt(a_f32_t x);

#if defined(__cplusplus)
} /* extern "C" */
#endif /* __cplusplus */

/*! @} A_MATH */

#endif /* __A_MATH_H__ */
