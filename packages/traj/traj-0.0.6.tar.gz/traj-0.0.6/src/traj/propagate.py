"""Routines for propagation"""

import numpy as np
from scipy.linalg import solve_banded

from .tri import d2trid, eye_trid, tridiag_mul
from .wf import l2_norm


# [TODO] Develop normalize routine

def propagate_imaginary(wf, Vx, dx, dt, Nt_max, thres=1e-13, v=False):

    # Process arguments
    _wf = np.asarray(wf)
    _Vx = np.asarray(Vx)
    for _arr in (_wf, _Vx):
        assert (_arr.ndim == 1) and (_arr.size > 1)
    assert _wf.size == _Vx.size
    Nx = _wf.size
    assert (int(Nt_max) == Nt_max) and (Nt_max > 0)
    assert thres > 0
   
    # Construct Crank-Nicolson propagator
    Htr = np.empty((3,Nx), dtype=np.complex128)
    Htr[:] = (-0.5) * d2trid(Nx,dx)
    Htr[1,:] += Vx
    Itr = eye_trid(Nx)
    Uf = Itr + (-0.5j * (-1.j*dt)) * Htr
    Ub = Itr + (0.5j * (-1.j*dt)) * Htr
    
    # Propagate wavefunction with imaginary time
    out_prev = np.empty((Nx,), dtype=np.complex128)
    out_prev[:] = _wf
    out_prev *= 1./np.sqrt(l2_norm(out_prev, dx)) 
    out = np.empty((Nx,), dtype=np.complex128)

    for it in range(Nt_max-1):

        out[:] = solve_banded((1,1), Ub, tridiag_mul(Uf, out_prev))

        out *= 1./np.sqrt(l2_norm(out, dx))
#        print(l2_norm(out, dx), l2_norm(out_prev, dx))

        norm_of_diff = l2_norm(out - out_prev, dx)
        if v and ((it+1)%100==0): print("[{:04d}] norm_of_diff={:.3e}".format(it+1, norm_of_diff))
        if norm_of_diff < thres:
            if v: print("The norm_of_diff='{:.3e}' reached the threshold='{:.3e}'".format(norm_of_diff, thres))
            break
        out_prev[:] = out
        
    # Check the convergence of the wavefunction
    if it == ((Nt_max-1)-1):
        raise Exception("Convergence might not have been reached.")
        
    return out



