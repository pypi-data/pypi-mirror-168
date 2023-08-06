/*!
 @file pid.h
 @brief proportional integral derivative controller
 @details
 A proportional integral derivative controller (PID controller or three-term controller) is
 a control loop mechanism employing feedback that is widely used in industrial control systems
 and a variety of other applications requiring continuously modulated control.
 \f[
  u(t) = K_p\left[e(t)+\frac{1}{T_i}\int{e(t)}\text{dt}+T_d\frac{\text{d}e(t)}{\text{d}t}\right]
 \f]
 \f[
  u(t) = K_p\left[e(t)+\frac{T}{T_i}\sum^k_{i=0}e(i)+\frac{T_d}{T}[e(k)-e(k-1)]\right]
 \f]
 - positional PID controller
 \f{aligned}{
  u(k) &= K_p e(k) + q\sum^k_{i=0} K_i e(i) + K_d [e(k)-e(k-1)] \\
       &= (K_p+K_d) e(k) + q\sum^k_{i=0}K_i e(i) + (-K_d) e(k-1) \\
       &\begin{cases}q=0&|\sum\limits^{k-1}_{i=0}K_ie(i)|>E \bigvee
       [\sum\limits^{k-1}_{i=0}K_ie(i)]K_ke(k)>0 \\ q=1\end{cases}
 \f}
 - incremental PID controller
 \f{aligned}{
  \Delta u(k) &= K_p [e(k)-e(k-1)] + K_i e(k) + K_d [e(k)+e(k-2)-2e(k-1)] \\
              &= (K_p+K_i+K_d) e(k) + (-K_p-2K_i) e(k-1) + K_d e(k-2)
 \f}
 https://en.wikipedia.org/wiki/PID_controller
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#ifndef __A_PID_H__
#define __A_PID_H__

#include "a.h"

/*!
 @ingroup A
 @addtogroup A_PID proportional integral derivative controller
 @{
*/

/*!
 @brief instance enumeration for PID controller mode
*/
typedef enum a_pid_e
{
    A_PID_OFF, //!< turn off PID controller
    A_PID_POS, //!< positional PID controller
    A_PID_INC, //!< incremental PID controller
} a_pid_e;

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wpadded"
#endif /* diagnostic */
#if defined(_MSC_VER)
#pragma warning(push)
#pragma warning(disable : 4820)
#endif /* _MSC_VER */

/*!
 @brief instance structure for PID controller
*/
typedef struct a_pid_s
{
    a_real_t ts; //!< sampling time unit(s)
    a_real_t kp; //!< proportional constant
    a_real_t ki; //!< integral constant
    a_real_t kd; //!< derivative constant
    a_real_t out; //!< controller output
    a_real_t outmin; //!< minimum output
    a_real_t outmax; //!< maximum output
    a_real_t summax; //!< maximum integral output
    a_real_t sum; //!< (integral) output item sum
    a_real_t ref; //!< cache feedback
    a_real_t ec; //!< error change
    a_real_t e; //!< error input
    a_uint_t mode; //!< mode for PID controller
    a_uint_t num; //!< number of columns
} a_pid_s;

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
 @brief turn off PID controller
 @param[in,out] ctx points to an instance of PID controller
*/
A_PUBLIC a_pid_s *a_pid_off(a_pid_s *ctx);

/*!
 @brief incremental PID controller
 @param[in,out] ctx points to an instance of PID controller
*/
A_PUBLIC a_pid_s *a_pid_inc(a_pid_s *ctx);

/*!
 @brief positional PID controller
 @param[in,out] ctx points to an instance of PID controller
 @param[in] max maximum intergral output
*/
A_PUBLIC a_pid_s *a_pid_pos(a_pid_s *ctx, a_real_t max);

/*!
 @brief set mode for PID controller directly
 @param[in,out] ctx points to an instance of PID controller
 @param[in] mode Mode for PID controller
  @arg @ref A_PID_OFF turn off PID controller
  @arg @ref A_PID_POS positional PID controller
  @arg @ref A_PID_INC incremental PID controller
*/
A_PUBLIC a_pid_s *a_pid_mode(a_pid_s *ctx, a_uint_t mode);

/*!
 @brief set sampling period for PID controller
 @param[in,out] ctx points to an instance of PID controller
 @param[in] ts sampling time unit(s)
*/
A_PUBLIC a_pid_s *a_pid_time(a_pid_s *ctx, a_real_t ts);

/*!
 @brief set proportional integral derivative constant for PID controller
 @param[in,out] ctx points to an instance of PID controller
 @param[in] kp proportional constant
 @param[in] ki integral constant
 @param[in] kd derivative constant
*/
A_PUBLIC a_pid_s *a_pid_kpid(a_pid_s *ctx, a_real_t kp, a_real_t ki, a_real_t kd);

/*!
 @brief initialize function for PID controller, default is turn off
 @param[in,out] ctx points to an instance of PID controller
 @param[in] ts sampling time unit(s)
 @param[in] min minimum output
 @param[in] max maximum output
*/
A_PUBLIC a_pid_s *a_pid_init(a_pid_s *ctx, a_real_t ts, a_real_t min, a_real_t max);

A_HIDDEN a_real_t a_pid_proc_(a_pid_s *ctx, a_real_t set, a_real_t ref, a_real_t e, a_real_t ec);

/*!
 @brief process function for PID controller
 @param[in,out] ctx points to an instance of PID controller
 @param[in] set setpoint
 @param[in] ref feedback
 @return output
  @retval set when PID controller is off
*/
A_PUBLIC a_real_t a_pid_proc(a_pid_s *ctx, a_real_t set, a_real_t ref);

/*!
 @brief terminate function for PID controller
 @param[in,out] ctx points to an instance of PID controller
*/
A_PUBLIC a_pid_s *a_pid_done(a_pid_s *ctx);

#if defined(__cplusplus)
} /* extern "C" */
#endif /* __cplusplus */

/*! @} A_PID */

#endif /* __A_PID_H__ */
