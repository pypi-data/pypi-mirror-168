/*!
 @file operator.h
 @brief algorithm library internal operators
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#ifndef __OPERATOR_H__
#define __OPERATOR_H__

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wc++-compat"
#endif /* diagnostic */

// clang-format off

#undef inc
#undef dec
#define inc ++ //!< increment
#define dec -- //!< decrement

#undef pos
#undef neg
#define pos + //!< positive
#define neg - //!< negative

#ifndef __cplusplus

#undef not
#undef compl
#define not   ! //!< logical NOT
#define compl ~ //!< bitwise NOT

#endif /* __cplusplus */

#undef mul
#undef div
#undef mod
#define mul * //!< multiplication
#define div / //!< division
#define mod % //!< remainder

#undef add
#undef sub
#define add + //!< addition
#define sub - //!< subtraction

#undef lshift
#undef rshift
#define lshift << //!< bitwise left shift
#define rshift >> //!< bitwise right shift

#undef eq
#undef ne
#undef lt
#undef gt
#undef le
#undef ge
#define eq == //!< equal
#define ne != //!< not equal
#define lt <  //!< less than
#define gt >  //!< greater than
#define le <= //!< less than or equal
#define ge >= //!< greater than or equal

#ifndef __cplusplus

#undef bitor
#undef bitxor
#undef bitand
#define bitand & //!< bitwise AND
#define bitxor ^ //!< bitwise XOR (exclusive or)
#define bitor  | //!< bitwise OR (inclusive or)

#undef or
#undef and
#define and && //!< logical AND
#define or  || //!< logical OR

#endif /* __cplusplus */

#undef add_eq
#undef sub_eq
#undef mul_eq
#undef div_eq
#undef mod_eq
#define add_eq += //!< in-place assignment by sum
#define sub_eq -= //!< in-place assignment by difference
#define mul_eq *= //!< in-place assignment by product
#define div_eq /= //!< in-place assignment by quotient
#define mod_eq %= //!< in-place assignment by remainder

#undef shl_eq
#undef shr_eq
#define shl_eq <<= //!< in-place assignment by bitwise left shift
#define shr_eq >>= //!< in-place assignment by bitwise right shift

#ifndef __cplusplus

#undef or_eq
#undef xor_eq
#undef and_eq
#define and_eq &= //!< in-place assignment by bitwise AND
#define xor_eq ^= //!< in-place assignment by bitwise XOR (exclusive or)
#define or_eq  |= //!< in-place assignment by bitwise OR (inclusive or)

#endif /* __cplusplus */

// clang-format on

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic pop
#endif /* diagnostic */

#endif /* __OPERATOR_H__ */
