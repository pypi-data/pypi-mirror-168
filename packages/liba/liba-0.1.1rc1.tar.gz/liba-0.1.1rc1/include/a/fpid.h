/*!
 @file fpid.h
 @brief fuzzy proportional integral derivative controller
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#ifndef __A_FPID_H__
#define __A_FPID_H__

#include "pid.h"
#include "mf.h"

/*!
 @ingroup A
 @addtogroup A_FPID fuzzy proportional integral derivative controller
 @{
*/

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wpadded"
#endif /* diagnostic */
#if defined(_MSC_VER)
#pragma warning(push)
#pragma warning(disable : 4820)
#endif /* _MSC_VER */

/*!
 @brief instance structure for fuzzy PID controller
*/
typedef struct a_fpid_s
{
    a_pid_s pid[1]; //!< instance structure for PID controller

    const a_real_t *mkp; //!< points to Kp's rule base table, the rule base must be square
    const a_real_t *mki; //!< points to Ki's rule base table, the rule base must be square
    const a_real_t *mkd; //!< points to Kd's rule base table, the rule base must be square
    const a_real_t *mma; //!< points to membership function argument table, an array terminated by @ref A_MF_NUL

    a_uint_t *idx; //!< the memory cache for membership index
    /*!< the length must be greater than or equal to twice the maximum number triggered by the rule */
    a_real_t *mms; //!< the memory cache for membership
    /*!< the length must be greater than or equal to twice the maximum number triggered by the rule */
    a_real_t *mat; //!< the memory cache for matrix of the membership outer product of e and ec

    a_real_t sigma; //!< the coefficient of the input, ((num-1)>>1<<1)/(Imax-Imin)
    a_real_t alpha; //!< the coefficient of the output, (Omax-Omin)/((num-1)>>1<<1)

    a_real_t kp; //!< base proportional constant
    a_real_t ki; //!< base integral constant
    a_real_t kd; //!< base derivative constant

    a_real_t (*op)(a_real_t, a_real_t); //!< fuzzy relational operator
} a_fpid_s;

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic pop
#endif /* diagnostic */
#if defined(_MSC_VER)
#pragma warning(pop)
#endif /* _MSC_VER */

#if defined(__cplusplus)
extern "C" {
#endif /* __cplusplus */

/*!
 @brief turn off fuzzy PID controller
 @param[in,out] ctx points to an instance of fuzzy PID controller
*/
A_PUBLIC a_fpid_s *a_fpid_off(a_fpid_s *ctx);

/*!
 @brief incremental fuzzy PID controller
 @param[in,out] ctx points to an instance of fuzzy PID controller
*/
A_PUBLIC a_fpid_s *a_fpid_inc(a_fpid_s *ctx);

/*!
 @brief positional fuzzy PID controller
 @param[in,out] ctx points to an instance of fuzzy PID controller
 @param[in] max maximum intergral output
*/
A_PUBLIC a_fpid_s *a_fpid_pos(a_fpid_s *ctx, a_real_t max);

/*!
 @brief set mode for fuzzy PID controller directly
 @param[in,out] ctx points to an instance of fuzzy PID controller
 @param[in] mode Mode for fuzzy PID controller
  @arg @ref A_PID_OFF turn off fuzzy PID controller
  @arg @ref A_PID_POS positional fuzzy PID controller
  @arg @ref A_PID_INC incremental fuzzy PID controller
*/
A_PUBLIC a_fpid_s *a_fpid_mode(a_fpid_s *ctx, a_uint_t mode);

/*!
 @brief set sampling period for fuzzy PID controller
 @param[in,out] ctx points to an instance of fuzzy PID controller
 @param[in] ts sampling time unit(s)
*/
A_PUBLIC a_fpid_s *a_fpid_time(a_fpid_s *ctx, a_real_t ts);

/*!
 @brief set input extreme value for fuzzy PID controller
 @param[in,out] ctx points to an instance of fuzzy PID controller
 @param[in] min mininum input
 @param[in] max maxinum input
*/
A_PUBLIC a_fpid_s *a_fpid_ilim(a_fpid_s *ctx, a_real_t min, a_real_t max);

/*!
 @brief set output extreme value for fuzzy PID controller
 @param[in,out] ctx points to an instance of fuzzy PID controller
 @param[in] min mininum output
 @param[in] max maxinum output
*/
A_PUBLIC a_fpid_s *a_fpid_olim(a_fpid_s *ctx, a_real_t min, a_real_t max);

A_PUBLIC a_size_t A_FPID_BUF1(a_uint_t max);
/*!
 @brief set one cache buffer for fuzzy PID controller
 @param[in,out] ctx points to an instance of fuzzy PID controller
 @param[in] ptr points to a buffer at least A_FPID_BUF1(max)
 @param[in] max the maximum number triggered by the rule
*/
A_PUBLIC a_fpid_s *a_fpid_buf1(a_fpid_s *ctx, a_vptr_t ptr, a_size_t max);
#define A_FPID_BUF1(N) (sizeof(a_uint_t) * 2 * (N) + sizeof(a_real_t) * (N) * ((N) + 2))

/*!
 @brief set proportional integral derivative constant for fuzzy PID controller
 @param[in,out] ctx points to an instance of fuzzy PID controller
 @param[in] kp proportional constant
 @param[in] ki integral constant
 @param[in] kd derivative constant
*/
A_PUBLIC a_fpid_s *a_fpid_kpid(a_fpid_s *ctx, a_real_t kp, a_real_t ki, a_real_t kd);

/*!
 @brief set buffer for fuzzy PID controller
 @param[in,out] ctx points to an instance of fuzzy PID controller
 @param[in] idx the memory cache for membership index
  the length must be greater than or equal to twice the maximum number triggered by the rule
 @param[in] mms the memory cache for membership
  the length must be greater than or equal to twice the maximum number triggered by the rule
 @param[in] mat the memory cache for matrix of the membership outer product of e and ec
*/
A_PUBLIC a_fpid_s *a_fpid_buff(a_fpid_s *ctx, a_uint_t *idx, a_real_t *mms, a_real_t *mat);
#define A_FPID_MAT1(N) (sizeof(a_real_t) * (N) * (N))
#define A_FPID_MMS1(N) (sizeof(a_real_t) * 2 * (N))
#define A_FPID_IDX1(N) (sizeof(a_uint_t) * 2 * (N))
#define A_FPID_MAT(N) ((N) * (N))
#define A_FPID_MMS(N) (2 * (N))
#define A_FPID_IDX(N) (2 * (N))

/*!
 @brief set rule base for fuzzy PID controller
 @param[in,out] ctx points to an instance of fuzzy PID controller
 @param[in] num number of columns in the rule base
 @param[in] mma points to membership function parameter table, an array terminated by @ref A_MF_NUL
 @param[in] mkp points to Kp's rule base table, the rule base must be square
 @param[in] mki points to Ki's rule base table, the rule base must be square
 @param[in] mkd points to Kd's rule base table, the rule base must be square
*/
A_PUBLIC a_fpid_s *a_fpid_base(a_fpid_s *ctx, a_uint_t num, const a_real_t *mma, const a_real_t *mkp, const a_real_t *mki, const a_real_t *mkd);

/*!
 @brief initialize function for fuzzy PID controller, default setting is off
 @param[in,out] ctx points to an instance of fuzzy PID controller
 @param[in] ts sampling time unit(s)
 @param[in] num number of columns in the rule base
 @param[in] mma points to membership function parameter table, an array terminated by @ref A_MF_NUL
 @param[in] mkp points to Kp's rule base table, the rule base must be square
 @param[in] mki points to Ki's rule base table, the rule base must be square
 @param[in] mkd points to Kd's rule base table, the rule base must be square
 @param[in] imin mininum input
 @param[in] imax maxinum input
 @param[in] omin mininum output
 @param[in] omax maxinum output
*/
A_PUBLIC a_fpid_s *a_fpid_init(a_fpid_s *ctx, a_real_t ts, a_uint_t num, const a_real_t *mma,
                               const a_real_t *mkp, const a_real_t *mki, const a_real_t *mkd,
                               a_real_t imin, a_real_t imax, a_real_t omin, a_real_t omax);

A_HIDDEN a_real_t a_fpid_proc_(a_fpid_s *ctx, a_real_t set, a_real_t ref, a_real_t e, a_real_t ec);

/*!
 @brief process function for fuzzy PID controller
 @param[in,out] ctx points to an instance of fuzzy PID controller
 @param[in] set setpoint
 @param[in] ref feedback
 @return output
  @retval set when fuzzy PID controller is off
*/
A_PUBLIC a_real_t a_fpid_proc(a_fpid_s *ctx, a_real_t set, a_real_t ref);

/*!
 @brief terminate function for fuzzy PID controller
 @param[in,out] ctx points to an instance of fuzzy PID controller
*/
A_PUBLIC a_fpid_s *a_fpid_done(a_fpid_s *ctx);

#if defined(__cplusplus)
} /* extern "C" */
#endif /* __cplusplus */

/*! @} A_FPID */

#endif /* __A_FPID_H__ */
