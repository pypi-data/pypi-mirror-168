"""Root-finding routines"""

from numba import njit

import numpy as np

@njit
def secant(f, x0, x1, args=(), Nmax=100, atol=1e-8, rtol=1e-5):

    def _f(_x): return f(_x, *args)

    _x0, _x1 = x0, x1
    _f0, _f1 = _f(_x0), _f(_x1)
    _f1_minus_f0 = _f1 - _f0
    if np.abs(_f1_minus_f0) < 1e-10: raise Exception("f0 and f1 too close")
    if np.abs(_f0) < atol + rtol * np.abs(_f1_minus_f0):
        return _x0, True
    
    for i in range(Nmax):
        _x2 = _x1 - _f1 * (_x1-_x0) / (_f1-_f0)
        _f2 = _f(_x2)
        if np.abs(_f2) < atol + rtol * np.abs(_f2 - _f1): 
            return _x2, True
        _x0, _f0 = _x1, _f1
        _x1, _f1 = _x2, _f2

    return None, False        
