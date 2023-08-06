//! fuzzy proportional integral derivative controller

use crate::pid::PID;
use crate::Real;
use crate::Uint;

/// fuzzy proportional integral derivative controller
#[repr(C)]
pub struct FPID {
    /// proportional integral derivative controller
    pub pid: PID,
    mkp: *const Real,
    mki: *const Real,
    mkd: *const Real,
    mma: *const Real,
    sigma: Real,
    alpha: Real,
    idx: *mut Uint,
    mms: *mut Real,
    mat: *mut Real,
    /// base proportional constant
    pub kp: Real,
    /// base integral constant
    pub ki: Real,
    /// base derivative constant
    pub kd: Real,
    /// fuzzy relational operator
    pub op: Option<extern "C" fn(Real, Real) -> Real>,
}

extern "C" {
    fn a_fpid_off(ctx: *mut FPID) -> *mut FPID;
    fn a_fpid_inc(ctx: *mut FPID) -> *mut FPID;
    fn a_fpid_pos(ctx: *mut FPID, max: Real) -> *mut FPID;
    fn a_fpid_mode(ctx: *mut FPID, mode: Uint) -> *mut FPID;
    fn a_fpid_time(ctx: *mut FPID, ts: Real) -> *mut FPID;
    fn a_fpid_ilim(ctx: *mut FPID, min: Real, max: Real) -> *mut FPID;
    fn a_fpid_olim(ctx: *mut FPID, min: Real, max: Real) -> *mut FPID;
    fn a_fpid_kpid(ctx: *mut FPID, kp: Real, ki: Real, kd: Real) -> *mut FPID;
    fn a_fpid_buff(ctx: *mut FPID, idx: *mut Uint, mms: *mut Real, mat: *mut Real) -> *mut FPID;
    fn a_fpid_base(
        ctx: *mut FPID,
        num: Uint,
        mma: *const Real,
        mkp: *const Real,
        mki: *const Real,
        mkd: *const Real,
    ) -> *mut FPID;
    fn a_fpid_init(
        ctx: *mut FPID,
        ts: Real,
        num: Uint,
        mma: *const Real,
        mkp: *const Real,
        mki: *const Real,
        mkd: *const Real,
        imin: Real,
        imax: Real,
        omin: Real,
        omax: Real,
    ) -> *mut FPID;
    fn a_fpid_proc(ctx: *mut FPID, set: Real, r#ref: Real) -> Real;
    fn a_fpid_done(ctx: *mut FPID) -> *mut FPID;
}

/**
## Examples

```no_run
use liba::Real;
const NB: Real = -3.0;
const NM: Real = -2.0;
const NS: Real = -1.0;
const ZO: Real = 0.0;
const PS: Real = 1.0;
const PM: Real = 2.0;
const PB: Real = 3.0;
let mkp = [
    [NB, NB, NM, NM, NS, ZO, ZO],
    [NB, NB, NM, NS, NS, ZO, PS],
    [NM, NM, NM, NS, ZO, PS, PS],
    [NM, NM, NS, ZO, PS, PM, PM],
    [NS, NS, ZO, PS, PS, PM, PM],
    [NS, ZO, PS, PM, PM, PM, PB],
    [ZO, ZO, PM, PM, PM, PB, PB],
];
let mki = [
    [PB, PB, PM, PM, PS, ZO, ZO],
    [PB, PB, PM, PS, PS, ZO, ZO],
    [PB, PM, PS, PS, ZO, NS, NS],
    [PM, PM, PS, ZO, NS, NM, NM],
    [PM, PS, ZO, NS, NS, NM, NB],
    [ZO, ZO, NS, NS, NM, NB, NB],
    [ZO, ZO, NS, NM, NM, NB, NB],
];
let mkd = [
    [NS, PS, PB, PB, PB, PM, NS],
    [NS, PS, PB, PM, PM, PS, ZO],
    [ZO, PS, PM, PM, PS, PS, ZO],
    [ZO, PS, PS, PS, PS, PS, ZO],
    [ZO, ZO, ZO, ZO, ZO, ZO, ZO],
    [NB, NS, NS, NS, NS, NS, NB],
    [NB, NM, NM, NM, NS, NS, NB],
];
let mma = [
    liba::mf::TRI,
    NB,
    NB,
    NM,
    liba::mf::TRI,
    NB,
    NM,
    NS,
    liba::mf::TRI,
    NM,
    NS,
    ZO,
    liba::mf::TRI,
    NS,
    ZO,
    PS,
    liba::mf::TRI,
    ZO,
    PS,
    PM,
    liba::mf::TRI,
    PS,
    PM,
    PB,
    liba::mf::TRI,
    PM,
    PB,
    PB,
    liba::mf::NUL,
];
let mut fpid = liba::FPID::new(
    1.0,
    mkp.len(),
    &mma,
    &mkp.concat(),
    &mki.concat(),
    &mkd.concat(),
    -10.0,
    10.0,
    -10.0,
    10.0,
);
fpid.base(mkp.len(), &mma, &mkp.concat(), &mki.concat(), &mkd.concat());
fpid.kpid(10.0, 0.1, 1.0);
let mut idx = [0u32; 4];
let mut mms = [0.0; 4];
let mut mat = [0.0; 4];
fpid.buff(&mut idx, &mut mms, &mut mat);
fpid.time(0.1).pos(10.0);
fpid.off().inc();
fpid.proc(1.0, 0.0);
fpid.done();
```
*/
impl FPID {
    /// initialize function for fuzzy PID controller, default is turn off
    pub fn new(
        ts: Real,
        num: usize,
        mma: &[Real],
        mkp: &[Real],
        mki: &[Real],
        mkd: &[Real],
        imin: Real,
        imax: Real,
        omin: Real,
        omax: Real,
    ) -> Self {
        let mut ctx: Self = Self {
            pid: PID::new(ts, omin, omax),
            mkp: std::ptr::null(),
            mki: std::ptr::null(),
            mkd: std::ptr::null(),
            mma: std::ptr::null(),
            sigma: 0.0,
            alpha: 0.0,
            idx: std::ptr::null_mut(),
            mms: std::ptr::null_mut(),
            mat: std::ptr::null_mut(),
            kp: 0.0,
            ki: 0.0,
            kd: 0.0,
            op: None,
        };
        unsafe {
            a_fpid_init(
                &mut ctx,
                ts,
                num as Uint,
                mma.as_ptr(),
                mkp.as_ptr(),
                mki.as_ptr(),
                mkd.as_ptr(),
                imin,
                imax,
                omin,
                omax,
            );
        };
        ctx
    }

    /// set turn off mode
    pub fn off(&mut self) -> &mut Self {
        unsafe { a_fpid_off(self).as_mut().unwrap_unchecked() }
    }

    /// set incremental mode
    pub fn inc(&mut self) -> &mut Self {
        unsafe { a_fpid_inc(self).as_mut().unwrap_unchecked() }
    }

    /// set positional mode
    pub fn pos(&mut self, max: Real) -> &mut Self {
        unsafe { a_fpid_pos(self, max).as_mut().unwrap_unchecked() }
    }

    /// set mode for fuzzy PID controller directly
    pub fn mode(&mut self, mode: u32) -> &mut Self {
        unsafe { a_fpid_mode(self, mode as Uint).as_mut().unwrap_unchecked() }
    }

    /// set sampling period for fuzzy PID controller
    pub fn time(&mut self, ts: Real) -> &mut Self {
        unsafe { a_fpid_time(self, ts).as_mut().unwrap_unchecked() }
    }

    /// set input extreme value for fuzzy PID controller
    pub fn ilim(&mut self, min: Real, max: Real) -> &mut Self {
        unsafe { a_fpid_ilim(self, min, max).as_mut().unwrap_unchecked() }
    }

    /// set output extreme value for fuzzy PID controller
    pub fn olim(&mut self, min: Real, max: Real) -> &mut Self {
        unsafe { a_fpid_olim(self, min, max).as_mut().unwrap_unchecked() }
    }

    /// set proportional integral derivative constant for fuzzy PID controller
    pub fn kpid(&mut self, kp: Real, ki: Real, kd: Real) -> &mut Self {
        unsafe { a_fpid_kpid(self, kp, ki, kd).as_mut().unwrap_unchecked() }
    }

    /// set buffer for fuzzy PID controller
    pub fn buff(&mut self, idx: &mut [u32], mms: &mut [Real], mat: &mut [Real]) -> &mut Self {
        unsafe {
            a_fpid_buff(self, idx.as_mut_ptr(), mms.as_mut_ptr(), mat.as_mut_ptr())
                .as_mut()
                .unwrap_unchecked()
        }
    }

    /// set rule base for fuzzy PID controller
    pub fn base(
        &mut self,
        num: usize,
        mma: &[Real],
        mkp: &[Real],
        mki: &[Real],
        mkd: &[Real],
    ) -> &mut Self {
        unsafe {
            a_fpid_base(
                self,
                num as Uint,
                mma.as_ptr(),
                mkp.as_ptr(),
                mki.as_ptr(),
                mkd.as_ptr(),
            )
            .as_mut()
            .unwrap_unchecked()
        }
    }

    /// process function for fuzzy PID controller
    pub fn proc(&mut self, set: Real, r#ref: Real) -> Real {
        unsafe { a_fpid_proc(self, set, r#ref) }
    }

    /// terminate function for fuzzy PID controller
    pub fn done(&mut self) -> &mut Self {
        unsafe { a_fpid_done(self).as_mut().unwrap_unchecked() }
    }
}
