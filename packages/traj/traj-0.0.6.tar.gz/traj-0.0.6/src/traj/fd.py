"""Routines for a set of finite difference schemes"""

import numpy as np

from numba import stencil, njit


@stencil
def d2_kernel(y,h):
    return (1./h**2) * (y[1] - 2*y[0] + y[-1])


@njit(parallel=True)
def d2_parallel(f,h):
    _d2_f = d2_kernel(f,h)
    _d2_f[0] = (1*f[0]-2*f[1]+1*f[2])/(1*1.0*h**2)
    _d2_f[-1] = (1*f[-3]-2*f[-2]+1*f[-1])/(1*1.0*h**2)
    return _d2_f


@njit(parallel=False)
def d2(f,h):
    _f = np.asarray(f)
    assert _f.ndim == 1 and _f.size > 3
    _d2_f = d2_kernel(f,h)
    _d2_f[0] = (2*f[0]-5*f[1]+4*f[2]-f[3])/(1.0*h**2)
    _d2_f[-1] = (-f[-4]+4*f[-3]-5*f[-2]+2*f[-1])/(1.0*h**2)
    return _d2_f



@njit
def m_Ns4(x,x0,dx,Nx):
    _ml = int((x-x0) / dx)
    _less = 1 - _ml
    _more = (Nx - 3) - _ml
    _m = (_ml-1) + (_less>0)*_less + (_more<0)*_more
    return _m



@njit
def diff_wf_fd(wf,x,x0,dx,m=None):
    
    _wf = np.asarray(wf)
    assert _wf.ndim == 1
    _Nx = _wf.size
    _Ns = 4
    assert _Nx >= _Ns
    _x, _x0, _dx = float(x), float(x0), float(dx)
   
    _m = int(m) if m is not None else None
    if m is not None: assert _m == m

    if _m is None: _m = m_Ns4(_x,_x0,_dx,_Nx)
    
    _a = np.empty((_Ns,_Ns), dtype=_wf.dtype)
    _x_seg = _x0 + np.arange(_m,_m+_Ns) * _dx - _x
    _a[:,0] = 1.
    _a[:,1] = _x_seg # = _x_seg / 1!
    _a[:,2] = _a[:,1] * _x_seg / 2.
    _a[:,3] = _a[:,2] * _x_seg / 3.
    _diff_wf = np.linalg.solve(_a,_wf[_m:_m+_Ns])
    
    return _diff_wf

