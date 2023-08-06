/*!
 @file lib.c
 @brief algorithm library
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#include "a/a.h"

a_void_t a_swap(a_size_t siz, a_vptr_t lhs, a_vptr_t rhs)
{
    a_byte_t *l = (a_byte_t *)lhs;
    a_byte_t *r = (a_byte_t *)rhs;
    for (a_byte_t *d = r + siz; r != d; ++l, ++r)
    {
        *l ^= *r;
        *r ^= *l;
        *l ^= *r;
    }
}

a_void_t a_swap1(a_vptr_t lhs, a_vptr_t rhs)
{
    *(a_u8_t *)lhs = *(a_u8_t *)lhs ^ *(a_u8_t *)rhs;
    *(a_u8_t *)rhs = *(a_u8_t *)rhs ^ *(a_u8_t *)lhs;
    *(a_u8_t *)lhs = *(a_u8_t *)lhs ^ *(a_u8_t *)rhs;
}

a_void_t a_swap2(a_vptr_t lhs, a_vptr_t rhs)
{
    *(a_u16_t *)lhs = *(a_u16_t *)lhs ^ *(a_u16_t *)rhs;
    *(a_u16_t *)rhs = *(a_u16_t *)rhs ^ *(a_u16_t *)lhs;
    *(a_u16_t *)lhs = *(a_u16_t *)lhs ^ *(a_u16_t *)rhs;
}

a_void_t a_swap4(a_vptr_t lhs, a_vptr_t rhs)
{
    *(a_u32_t *)lhs = *(a_u32_t *)lhs ^ *(a_u32_t *)rhs;
    *(a_u32_t *)rhs = *(a_u32_t *)rhs ^ *(a_u32_t *)lhs;
    *(a_u32_t *)lhs = *(a_u32_t *)lhs ^ *(a_u32_t *)rhs;
}

a_void_t a_swap8(a_vptr_t lhs, a_vptr_t rhs)
{
    *(a_u64_t *)lhs = *(a_u64_t *)lhs ^ *(a_u64_t *)rhs;
    *(a_u64_t *)rhs = *(a_u64_t *)rhs ^ *(a_u64_t *)lhs;
    *(a_u64_t *)lhs = *(a_u64_t *)lhs ^ *(a_u64_t *)rhs;
}

a_void_t a_swapz(a_vptr_t lhs, a_vptr_t rhs)
{
    *(a_size_t *)lhs = *(a_size_t *)lhs ^ *(a_size_t *)rhs;
    *(a_size_t *)rhs = *(a_size_t *)rhs ^ *(a_size_t *)lhs;
    *(a_size_t *)lhs = *(a_size_t *)lhs ^ *(a_size_t *)rhs;
}

a_void_t a_swap16(a_vptr_t lhs, a_vptr_t rhs)
{
    typedef struct
    {
        a_u64_t m0;
        a_u64_t m1;
    } a_16_s;
    a_16_s buf = *(a_16_s *)lhs;
    *(a_16_s *)lhs = *(a_16_s *)rhs;
    *(a_16_s *)rhs = buf;
}
