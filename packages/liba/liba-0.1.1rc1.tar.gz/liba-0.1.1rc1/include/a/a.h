/*!
 @file a.h
 @brief algorithm library
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#ifndef __A_A_H__
#define __A_A_H__

#include "a.config.h"

/* extern "C" */
#if !defined __cplusplus
#define A_EXTERN_C
#define A_EXTERN_C_ENTER
#define A_EXTERN_C_LEAVE
#else /* !__cplusplus */
#define A_EXTERN_C extern "C"
#define A_EXTERN_C_ENTER extern "C" {
#define A_EXTERN_C_LEAVE }
#endif /* __cplusplus */

/*! @cond */

#if defined(__MINGW32__)
#undef __USE_MINGW_ANSI_STDIO
#define __USE_MINGW_ANSI_STDIO 1
#endif /* __MINGW32__ */

#if !defined A_SIZEOF_P
#if defined(__SIZEOF_POINTER__)
#define A_SIZEOF_P __SIZEOF_POINTER__
#elif defined(_WIN64)
#define A_SIZEOF_P 8
#elif defined(_WIN32)
#define A_SIZEOF_P 4
#endif /* __SIZEOF_POINTER__ */
#endif /* A_SIZEOF_P */

#if !defined __has_attribute
#define __has_attribute(...) 0
#endif /* __has_attribute */
#if !defined __has_builtin
#define __has_builtin(...) 0
#endif /* __has_builtin */
#if !defined __has_feature
#define __has_feature(...) 0
#endif /* __has_feature */
#if !defined __has_include
#define __has_include(...) 0
#endif /* __has_include */
#if !defined __has_warning
#define __has_warning(...) 0
#endif /* __has_warning */

/* https://en.wikipedia.org/wiki/Microsoft_Visual_C++ */
#if defined(_MSC_VER)
#define a_prereq_msvc(maj, min) (_MSC_VER >= (maj * 100 + min * 10))
#else /* !_MSC_VER */
#define a_prereq_msvc(maj, min) 0
#endif /* _MSC_VER */

/* https://gcc.gnu.org/onlinedocs/gcc-4.9.4/cpp/Common-Predefined-Macros.html */
#if defined(__GNUC__) && defined(__GNUC_MINOR__)
#define a_prereq_gnuc(maj, min) ((__GNUC__ << 16) + __GNUC_MINOR__ >= ((maj) << 16) + (min))
#else /* !__GNUC__ */
#define a_prereq_gnuc(maj, min) 0
#endif /* __GNUC__ */

/* https://clang.llvm.org/docs/LanguageExtensions.html */
#if defined(__clang_major__) && defined(__clang_minor__)
#define a_prereq_clang(maj, min) ((__clang_major__ << 16) + __clang_minor__ >= ((maj) << 16) + (min))
#else /* !__clang__ */
#define a_prereq_clang(maj, min) 0
#endif /* __clang__ */

#if a_prereq_gnuc(2, 96) || __has_builtin(__builtin_expect)
#define a_unlikely(...) __builtin_expect(!!(__VA_ARGS__), 0)
#define a_likely(...) __builtin_expect(!!(__VA_ARGS__), 1)
#else /* !__GNUC__ */
#define a_unlikely(...) (__VA_ARGS__)
#define a_likely(...) (__VA_ARGS__)
#endif /* __GNUC__ */

#if defined(__GNUC__) || defined(__clang__)
#define A_ATTRIBUTE(...) __attribute__((__VA_ARGS__))
#else /* !__attribute__ */
#define A_ATTRIBUTE(...)
#endif /* __attribute__ */

#if defined(_WIN32) || defined(__CYGWIN__)
#define A_DECLSPEC(...) __declspec(__VA_ARGS__)
#else /* !__declspec */
#define A_DECLSPEC(...)
#endif /* __declspec */

/* attribute fallthrough */
#if a_prereq_gnuc(7, 1) || __has_attribute(fallthrough)
#define A_FALLTHROUGH __attribute__((fallthrough))
#else /* !fallthrough */
#define A_FALLTHROUGH ((void)(0))
#endif /* fallthrough */

/* attribute format */
#if a_prereq_gnuc(2, 4) || __has_attribute(format)
#define A_FORMAT(...) __attribute__((format(__VA_ARGS__)))
#else /* !format */
#define A_FORMAT(...)
#endif /* format */

/* attribute deprecated */
#if a_prereq_gnuc(3, 2) || __has_attribute(deprecated)
#define A_DEPRECATED(...) __attribute__((deprecated(__VA_ARGS__)))
#elif defined(_WIN32) || defined(__CYGWIN__)
#define A_DEPRECATED(...) __declspec(deprecated(__VA_ARGS__))
#else /* !deprecated */
#define A_DEPRECATED(...)
#endif /* deprecated */

/* attribute always inline */
#if a_prereq_gnuc(3, 2) || __has_attribute(always_inline)
#define A_ALWAYS static __inline __attribute__((always_inline))
#elif defined(_MSC_VER)
#define A_ALWAYS static __forceinline
#else /* !_MSC_VER */
#define A_ALWAYS static __inline
#endif /* _MSC_VER */
#define A_INLINE static __inline
#define A_STATIC static

/* attribute visibility */
#if defined(_WIN32) || defined(__CYGWIN__)
#define A_EXPORT __declspec(dllexport)
#define A_IMPORT __declspec(dllimport)
#define A_HIDDEN
#elif a_prereq_gnuc(4, 0) || __has_attribute(visibility)
#define A_EXPORT __attribute__((visibility("default")))
#define A_IMPORT __attribute__((visibility("default")))
#define A_HIDDEN __attribute__((visibility("hidden")))
#else /* !visibility */
#define A_EXPORT
#define A_IMPORT
#define A_HIDDEN
#endif /* visibility */
#if defined(A_EXPORTS)
#define A_PUBLIC A_EXPORT
#elif defined(A_SHARED)
#define A_PUBLIC A_IMPORT
#else /* !A_PUBLIC */
#define A_PUBLIC
#endif /* A_PUBLIC */

#if !defined NDEBUG && defined(__GNUC__)
#define A_ASSERT(E) assert(E)
#else /* !NDEBUG */
#define A_ASSERT(E) ((void)(0))
#endif /* NDEBUG */

/*! @endcond */

/*!
 @addtogroup A algorithm library based on C
 @{
*/

/* keywords */
#if defined(__cplusplus)
#define a_register
#else /* !__cplusplus */
#define a_register __register
#endif /* __cplusplus */
#define a_volatile __volatile
#define a_restrict __restrict

#if !defined __cplusplus
#define a_cast_c(T, ...) ((T)(__VA_ARGS__))
#define a_cast_s(T, ...) ((T)(__VA_ARGS__))
#define a_cast_d(T, ...) ((T)(__VA_ARGS__))
#define a_cast_r(T, ...) ((T)(__VA_ARGS__))
#else /* !__cplusplus */
#define a_cast_c(T, ...) const_cast<T>(__VA_ARGS__)
#define a_cast_s(T, ...) static_cast<T>(__VA_ARGS__)
#define a_cast_d(T, ...) dynamic_cast<T>(__VA_ARGS__)
#define a_cast_r(T, ...) reinterpret_cast<T>(__VA_ARGS__)
#endif /* __cplusplus */

#include <stddef.h>
#include <stdint.h>
#include <limits.h>

typedef char a_c_t;
#define A_C_MIN CHAR_MIN
#define A_C_MAX CHAR_MAX

typedef int a_bool_t;
#if !defined __cplusplus
#define A_FALSE 0
#define A_TRUE !A_FALSE
#else /* !__cplusplus */
#define A_TRUE true
#define A_FALSE false
#endif /* __cplusplus */

typedef void a_void_t;
#if !defined __cplusplus
#define A_NULL NULL
#else /* !__cplusplus */
#define A_NULL nullptr
#endif /* __cplusplus */
#define A_INIT 0

typedef size_t a_size_t;
#define A_SIZE_MAX SIZE_MAX

// clang-format off

typedef  int8_t a_i8_t;
typedef uint8_t a_u8_t;
#define A_I8_C(X)  INT8_C(X)
#define A_U8_C(X) UINT8_C(X)
#define A_I8_MIN   INT8_MIN
#define A_I8_MAX   INT8_MAX
#define A_U8_MAX  UINT8_MAX

typedef  int16_t a_i16_t;
typedef uint16_t a_u16_t;
#define A_I16_C(X)  INT16_C(X)
#define A_U16_C(X) UINT16_C(X)
#define A_I16_MIN   INT16_MIN
#define A_I16_MAX   INT16_MAX
#define A_U16_MAX  UINT16_MAX

typedef  int32_t a_i32_t;
typedef uint32_t a_u32_t;
#define A_I32_C(X)  INT32_C(X)
#define A_U32_C(X) UINT32_C(X)
#define A_I32_MIN   INT32_MIN
#define A_I32_MAX   INT32_MAX
#define A_U32_MAX  UINT32_MAX

typedef  int64_t a_i64_t;
typedef uint64_t a_u64_t;
#define A_I64_C(X)  INT64_C(X)
#define A_U64_C(X) UINT64_C(X)
#define A_I64_MIN   INT64_MIN
#define A_I64_MAX   INT64_MAX
#define A_U64_MAX  UINT64_MAX

typedef  intmax_t a_imax_t;
typedef uintmax_t a_umax_t;
#define A_IMAX_C(X)  INTMAX_C(X)
#define A_UMAX_C(X) UINTMAX_C(X)
#define A_IMAX_MIN   INTMAX_MIN
#define A_IMAX_MAX   INTMAX_MAX
#define A_UMAX_MAX  UINTMAX_MAX

typedef  intptr_t a_iptr_t;
typedef uintptr_t a_uptr_t;
#define A_IPTR_C(X)  INTPTR_C(X)
#define A_UPTR_C(X) UINTPTR_C(X)
#define A_IPTR_MIN   INTPTR_MIN
#define A_IPTR_PTR   INTPTR_PTR
#define A_UPTR_PTR  UINTPTR_PTR

typedef ptrdiff_t a_diff_t;
#define A_DIFF_MIN PTRDIFF_MIN
#define A_DIFF_MAX PTRDIFF_MAX

typedef   signed int a_i_t;
typedef unsigned int a_u_t;
#define A_I_MIN  INT_MIN
#define A_I_MAX  INT_MAX
#define A_U_MIN UINT_MAX

typedef   signed long a_il_t;
typedef unsigned long a_ul_t;
#define A_IL_MIN  LONG_MIN
#define A_IL_MAX  LONG_MAX
#define A_UL_MIN ULONG_MAX

typedef   signed short a_is_t;
typedef unsigned short a_us_t;
#define A_IS_MIN  SHRT_MIN
#define A_IS_MAX  SHRT_MAX
#define A_US_MIN USHRT_MAX

typedef   signed long long a_ill_t;
typedef unsigned long long a_ull_t;
#define A_ILL_MIN  LLONG_MIN
#define A_ILL_MAX  LLONG_MAX
#define A_ULL_MIN ULLONG_MAX

typedef          int  a_int_t;
typedef   signed int a_sint_t;
typedef unsigned int a_uint_t;

typedef unsigned char  a_byte_t;
typedef          char  a_char_t;
typedef   signed char a_schar_t;
typedef unsigned char a_uchar_t;

typedef       char * a_str_t;
typedef const char *a_cstr_t;
typedef       void *a_vptr_t;
typedef const void *a_cptr_t;

typedef       float a_f32_t;
typedef      double a_f64_t;
typedef long double a_f128_t;

// clang-format on

typedef union a_cast_u
{
    a_c_t c;
    a_i_t i;
    a_u_t u;
    a_is_t is;
    a_us_t us;
    a_il_t il;
    a_ul_t ul;
    a_ill_t ill;
    a_ull_t ull;
    a_f64_t f64;
    a_f32_t f32;
    a_i8_t i8;
    a_u8_t u8;
    a_i16_t i16;
    a_u16_t u16;
    a_i32_t i32;
    a_u32_t u32;
    a_i64_t i64;
    a_u64_t u64;
    a_diff_t diff;
    a_imax_t imax;
    a_umax_t umax;
    a_iptr_t iptr;
    a_uptr_t uptr;
    a_size_t size;
    a_cptr_t cptr;
    a_vptr_t vptr;
    a_cstr_t cstr;
    a_str_t str;
} a_cast_u;

/*!
 @addtogroup A_REAL real number
 @{
*/

#ifndef A_REAL_BITS
#define A_REAL_BITS 64
#endif // real bits
#if A_REAL_BITS == 32

/*! @brief real number stored using `float` */
typedef float a_real_t;

/*!
 @brief expands to a floating-point constant expression
 having the value specified by its argument and the type @ref a_real_t
*/
#define A_REAL_C(X) X##F
/*!
 @brief expands to a floating-point function expression
 having the value specified by its argument and the type @ref a_real_t
*/
#define A_REAL_F(F, ...) F##f(__VA_ARGS__)

/*! @brief Format constants for the fprintf family of functions */
#define A_REAL_PRI(_, ...) "%" _ __VA_ARGS__
/*! @brief Format constants for the fscanf family of functions */
#define A_REAL_SCN(_, ...) "%" _ __VA_ARGS__

#elif A_REAL_BITS == 64

/*! @brief real number stored using `double` */
typedef double a_real_t;

/*!
 @brief expands to a floating-point constant expression
 having the value specified by its argument and the type @ref a_real_t
*/
#define A_REAL_C(X) X
/*!
 @brief expands to a floating-point function expression
 having the value specified by its argument and the type @ref a_real_t
*/
#define A_REAL_F(F, ...) F(__VA_ARGS__)

/*! @brief Format constants for the fprintf family of functions */
#define A_REAL_PRI(_, ...) "%" _ __VA_ARGS__
/*! @brief Format constants for the fscanf family of functions */
#define A_REAL_SCN(_, ...) "%" _ "l" __VA_ARGS__

#elif A_REAL_BITS == 128

/*! @brief real number stored using `long double` */
typedef long double a_real_t;

/*!
 @brief expands to a floating-point constant expression
 having the value specified by its argument and the type @ref a_real_t
*/
#define A_REAL_C(X) X##L
/*!
 @brief expands to a floating-point function expression
 having the value specified by its argument and the type @ref a_real_t
*/
#define A_REAL_F(F, ...) F##l(__VA_ARGS__)

/*! @brief Format constants for the fprintf family of functions */
#define A_REAL_PRI(_, ...) "%" _ "L" __VA_ARGS__
/*! @brief Format constants for the fscanf family of functions */
#define A_REAL_SCN(_, ...) "%" _ "L" __VA_ARGS__

#endif /* A_REAL_BITS */

/*! @} A_REAL */

/*!
 @brief size of memory that alignment is specified by alignment
 @param base specifies the alignment that is a power of two
 @param size number of bytes to allocate
*/
#define a_align(base, size) ((a_cast_r(a_size_t, size) + (base)-1) & ~((base)-1))

/*!
 @brief size of an array
 @param a must be an array variable
*/
#define a_arrayof(a) (sizeof(a) / sizeof(*a))

/*!
 @brief offset of a structure member
 @param type structure type
 @param member member variable
*/
#if defined(offsetof)
#define a_offsetof(type, member) offsetof(type, member)
#else /* !offsetof */
#define a_offsetof(type, member) a_cast_r(a_size_t, &a_cast_r(type *, 0)->member)
#endif /* offsetof */

/*!
 @brief container of a structure member
 @param ptr pointer to a member variable
 @param type structure type
 @param member member variable
*/
#define a_container_of(ptr, type, member) a_cast_r(type *, a_cast_r(a_size_t, ptr) - a_offsetof(type, member))

/*!
 @brief iterate from 0 to n and not include n
 @param I index type of the iteration
 @param i index variable of the iteration
 @param n final value of the iteration
*/
#define a_forenum(I, i, n) for (I i = 0; i < (n); ++i)

/*!
 @brief iterate from n to 0 and not include n
 @param I index type of the iteration
 @param i index variable of the iteration
 @param n final value of the iteration
*/
#define a_forenum_reverse(I, i, n) for (I i = (n); i-- > 0;)

/*!
 @brief iterate over an array
 @param T the element type in this array
 @param it pointer to the current element
 @param ptr starting address of this array
 @param num number of elements in this array
*/
#define a_foreach(T, it, ptr, num)                      \
    for (T *it = a_cast_s(T *, ptr),                    \
           *it##_ = a_likely(it) ? it + (num) : A_NULL; \
         it < it##_; ++it)

/*!
 @brief iterate over an array in reverse
 @param T the element type in this array
 @param it pointer to the current element
 @param ptr starting address of this array
 @param num number of elements in this array
*/
#define a_foreach_reverse(T, it, ptr, num)                           \
    for (T *it##_ = a_likely(ptr) ? a_cast_s(T *, ptr) - 1 : A_NULL, \
           *it = a_likely(ptr) ? it##_ + (num) : A_NULL;             \
         it > it##_; --it)

/*!
 @brief iterate over an array
 @param T the element type in this array
 @param it pointer to the current element
 @param ptr starting address of this array
 @param end the end address of this array
*/
#define a_iterate(T, it, ptr, end) \
    for (T *it = a_cast_s(T *, ptr), *it##_ = a_cast_s(T *, end); it < it##_; ++it)

/*!
 @brief iterate over an array in reverse
 @param T the element type in this array
 @param it pointer to the current element
 @param ptr starting address of this array
 @param end the end address of this array
*/
#define a_iterate_reverse(T, it, ptr, end)                           \
    for (T *it##_ = a_likely(ptr) ? a_cast_s(T *, ptr) - 1 : A_NULL, \
           *it = a_likely(end) ? a_cast_s(T *, end) - 1 : A_NULL;    \
         it > it##_; --it)

/*!
 @brief enumeration for return values
*/
enum
{
    A_SUCCESS, //!< return success
    A_FAILURE, //!< return failure
    A_INVALID, //!< return invalid
};

#if defined(__cplusplus)
extern "C" {
#endif /* __cplusplus */

/*!
 @brief swap two different memory blocks of the same size
 @param[in] siz the size of memory block being swapped
 @param[in,out] lhs points to memory block on the left
 @param[in,out] rhs points to memory block on the right
*/
A_PUBLIC a_void_t a_swap(a_size_t siz, a_vptr_t lhs, a_vptr_t rhs);
A_PUBLIC a_void_t a_swap1(a_vptr_t lhs, a_vptr_t rhs);
A_PUBLIC a_void_t a_swap2(a_vptr_t lhs, a_vptr_t rhs);
A_PUBLIC a_void_t a_swap4(a_vptr_t lhs, a_vptr_t rhs);
A_PUBLIC a_void_t a_swap8(a_vptr_t lhs, a_vptr_t rhs);
A_PUBLIC a_void_t a_swapz(a_vptr_t lhs, a_vptr_t rhs);
A_PUBLIC a_void_t a_swap16(a_vptr_t lhs, a_vptr_t rhs);

#if defined(__cplusplus)
} /* extern "C" */
#endif /* __cplusplus */

/*! @} A */

#endif /* __A_A_H__ */
