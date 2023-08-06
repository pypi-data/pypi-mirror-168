/*!
 @file math.h
 @brief internal mathematical algorithm library
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#ifndef __MATH_H__
#define __MATH_H__

#include "a/math.h"

#undef M_E
#undef M_LOG2E
#undef M_LOG10E
#undef M_LN2
#undef M_LN10
#undef M_PI
#undef M_PI_2
#undef M_PI_4
#undef M_1_PI
#undef M_2_PI
#undef M_2_SQRTPI
#undef M_SQRT2
#undef M_SQRT1_2
#define M_E A_E
#define M_LOG2E A_LOG2E
#define M_LOG10E A_LOG10E
#define M_LN2 A_LN2
#define M_LN10 A_LN10
#define M_PI A_PI
#define M_PI_2 A_PI_2
#define M_PI_4 A_PI_4
#define M_1_PI A_1_PI
#define M_2_PI A_2_PI
#define M_2_SQRTPI A_2_SQRTPI
#define M_SQRT2 A_SQRT2
#define M_SQRT1_2 A_SQRT1_2

#undef DBL_C
#undef FLT_C
#undef LDBL_C
#define DBL_C(X) A_DBL_C(X)
#define FLT_C(X) A_FLT_C(X)
#define LDBL_C(X) A_LDBL_C(X)

#undef DBL_F
#undef FLT_F
#undef LDBL_F
#define DBL_F(F, ...) A_DBL_F(F, __VA_ARGS__)
#define FLT_F(F, ...) A_FLT_F(F, __VA_ARGS__)
#define LDBL_F(F, ...) A_LDBL_F(F, __VA_ARGS__)

#undef SQ
#undef ABS
#undef SGN
#define SQ(x) A_SQ(x)
#define ABS(x) A_ABS(x)
#define SGN(x) A_SGN(x)

#endif /* __MATH_H__ */
