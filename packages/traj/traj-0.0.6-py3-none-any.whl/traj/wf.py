"""Routines related to wavefunctions"""

import numpy as np
from numpy import asarray, pi, exp, square

def gaussian_1d(x,t,sigma):
    
    _x, _t = asarray(x), asarray(t)
    _sig = float(sigma)
    assert _sig > 0
    
    _a = 1. + 1.j / (2.*_sig**2) * _t
    _wf = (1./(2.*pi*_sig**2))**0.25 * 1./(_a)**0.5 \
        * exp(-_x**2 / ((4.*_sig**2) * _a))
    
    return _wf


def l2_norm(wf, dx):
    _wf = asarray(wf)
    assert (_wf.ndim == 1) and (_wf.size > 1)
    return dx * np.sum(square(np.abs(_wf)))


def l2_normalize(wf, dx):
    norm = l2_norm(wf, dx)
    wf_normalized = wf * (1./(norm**0.5))
    return wf_normalized

