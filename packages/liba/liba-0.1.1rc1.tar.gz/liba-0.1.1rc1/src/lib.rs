/*!
An algorithm library based on C/C++ language

## Installation

Add this to your `Cargo.toml`:

```toml
[dependencies]
liba = "0.1"
```
*/

#![warn(missing_docs)]
#[allow(missing_docs)]
pub type Uint = libc::c_uint;
#[allow(missing_docs)]
pub type Real = f64;

pub mod mf;
pub mod pid;
pub use crate::pid::PID;
pub mod fpid;
pub use crate::fpid::FPID;
pub mod polytrack;
pub use crate::polytrack::PolyTrack3;
pub use crate::polytrack::PolyTrack5;
pub use crate::polytrack::PolyTrack7;

extern "C" {
    fn a_version() -> *const libc::c_char;
    fn a_version_major() -> Uint;
    fn a_version_minor() -> Uint;
    fn a_version_patch() -> Uint;
}

/**
algorithm library version

## Examples

```no_run
println!("version {}", liba::version());
```
*/
pub fn version() -> String {
    let c_str: &std::ffi::CStr = unsafe { std::ffi::CStr::from_ptr(a_version()) };
    let str_slice: &str = c_str.to_str().unwrap();
    let str_buf: String = str_slice.to_owned();
    str_buf
}

/**
algorithm library version major

## Examples

```no_run
println!("major {}", liba::version_major());
```
*/
pub fn version_major() -> u32 {
    unsafe { a_version_major() as u32 }
}

/**
algorithm library version minor

## Examples

```no_run
println!("minor {}", liba::version_minor());
```
*/
pub fn version_minor() -> u32 {
    unsafe { a_version_minor() as u32 }
}

/**
algorithm library version patch

## Examples

```no_run
println!("patch {}", liba::version_patch());
```
*/
pub fn version_patch() -> u32 {
    unsafe { a_version_patch() as u32 }
}

extern "C" {
    fn a_inv_sqrt(x: f32) -> f32;
}

/**
fast inverse square-root, $ \frac{1}{\sqrt{x}} $

## Examples

```no_run
println!("1/sqrt({})={}", 4, liba::inv_sqrt(4.0));
```
*/
pub fn inv_sqrt(x: f32) -> f32 {
    unsafe { a_inv_sqrt(x) }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn run_version() {
        println!("version {}", version());
        println!("major {}", version_major());
        println!("minor {}", version_minor());
        println!("patch {}", version_patch());
    }
}
