//! membership function

use crate::Real;

/// none
pub const NUL: Real = 0.0;
/// gaussian membership function
pub const GAUSS: Real = 1.0;
/// generalized bell-shaped membership function
pub const GBELL: Real = 2.0;
/// sigmoidal membership function
pub const SIG: Real = 3.0;
/// trapezoidal membership function
pub const TRAP: Real = 4.0;
/// triangular membership function
pub const TRI: Real = 5.0;
/// z-shaped membership function
pub const Z: Real = 6.0;

extern "C" {
    fn a_mf_gauss(x: Real, sigma: Real, c: Real) -> Real;
    fn a_mf_gbell(x: Real, a: Real, b: Real, c: Real) -> Real;
    fn a_mf_sig(x: Real, a: Real, c: Real) -> Real;
    fn a_mf_trap(x: Real, a: Real, b: Real, c: Real, d: Real) -> Real;
    fn a_mf_tri(x: Real, a: Real, b: Real, c: Real) -> Real;
    fn a_mf_z(x: Real, a: Real, b: Real) -> Real;
}

/// gaussian membership function
pub fn gauss(x: Real, sigma: Real, c: Real) -> Real {
    unsafe { a_mf_gauss(x, sigma, c) }
}

/// generalized bell-shaped membership function
pub fn gbell(x: Real, a: Real, b: Real, c: Real) -> Real {
    unsafe { a_mf_gbell(x, a, b, c) }
}

/// sigmoidal membership function
pub fn sig(x: Real, a: Real, c: Real) -> Real {
    unsafe { a_mf_sig(x, a, c) }
}

/// trapezoidal membership function
pub fn trap(x: Real, a: Real, b: Real, c: Real, d: Real) -> Real {
    unsafe { a_mf_trap(x, a, b, c, d) }
}

/// triangular membership function
pub fn tri(x: Real, a: Real, b: Real, c: Real) -> Real {
    unsafe { a_mf_tri(x, a, b, c) }
}

/// z-shaped membership function
pub fn z(x: Real, a: Real, b: Real) -> Real {
    unsafe { a_mf_z(x, a, b) }
}
