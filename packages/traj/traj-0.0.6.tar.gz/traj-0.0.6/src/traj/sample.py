"""Routines for sampling from a given probability density function"""

import numpy as np
from numba import njit
from .array import linspace_int, above_thres_range_indices

@njit
def sample(N,pdf,dx,x0,p=None,shrink=True):
    
    _pdf = np.asarray(pdf)
    assert _pdf.ndim == 1 and _pdf.size > 1
    _N = int(N)
    assert _N == N
    _dx = float(dx)
    assert _dx == dx
    _x0 = x0
    assert shrink in (True,False)
    _shrink = shrink
    
    #### Evaluate the cumulative distribution function (CDF) 
    #### of the given (discritized) probability density function (PDF)
    _cdf = np.empty_like(_pdf, dtype=np.float64)
    _cdf[0] = 0.
    _cdf[1:] = (0.5*_dx)*(_pdf[1:]+_pdf[:-1])
    _cdf[:] = np.cumsum(_cdf)
    
    _epsil = 1e-15
    assert (1 - _epsil) < _cdf[-1] and _cdf[-1] < (1 + _epsil)
    
    _pj = np.empty((_N,), dtype=np.float64)
    _width = 1.5*_epsil if _shrink else 0.
    if p is None:
        _pj[:] = np.sort(np.random.rand(_N)) * (1-2*_width) + _width
    else:
        _p = np.asarray(p)
        assert _p.ndim == 1 and _p.size == _N
        assert not np.any(np.diff(_p) < 0)
        _pj[:] = _p * (1-2*_width) + _width
        
    _xj = np.empty((N,), dtype=np.float64)
    
    _j = 0
    _Nx = _pdf.size
    _fin = False
    for _i in range(1,_Nx):
        for __j in range(_j,_N):
            if _pj[__j] < _cdf[_i]:
                _xi = _x0 + _i*_dx
                _y, _x = (_pj[__j]-_cdf[_i-1]), (_cdf[_i]-_cdf[_i-1])
                _alp = np.tan(np.arctan2(_y,_x))
                _xj[__j] = (1-_alp)*(_xi-_dx) + _alp*_xi
                if _j == _N-1: _fin = True
            else: 
                _j = __j
                break
        if _fin: break
    
    return _xj




# import numpy as np
# from .array import linspace_int, above_thres_range_indices

def sample_uniformly_above_thres(a, th, N, each=False):
    
    assert int(N) == N
    _N = N
    
    _range_indices = above_thres_range_indices(a, th)
    _N_interval = _range_indices.shape[0]
    
    if _N_interval == 0: return np.array([])
    
    _N_indices_per_interval = _range_indices[:,1] + 1 - _range_indices[:,0]
    _N_indices_total = _N_indices_per_interval.sum()
    _N_sample_per_interval = np.empty((_N_interval,), dtype=int)
    _N_sample_per_interval[:] = np.round(
                _N * _N_indices_per_interval / _N_indices_total)
    _N_sample_per_interval[-1] = _N - np.sum(_N_sample_per_interval[:-1])
    if _N != np.sum(_N_sample_per_interval):
        print("_N_sample_per_interval = {}".format(_N_sample_per_interval))
        raise Exception(
                ("The sum of `_N_sample_per_interval={:d}`,"
                    " is different from given `_N={:d}`").format(
                        np.sum(_N_sample_per_interval), _N))
    
    _indices_sampled_per_interval_list = []
    for _j, (_isrt,_iend) in enumerate(_range_indices):
        _N_in_this_interval = _N_sample_per_interval[_j]
        if _N_in_this_interval == 0: continue 
        _indices_sampled_j = linspace_int(_isrt,_iend,_N_in_this_interval)
        _indices_sampled_per_interval_list.append(_indices_sampled_j)
    
    _indices_sampled = np.hstack(_indices_sampled_per_interval_list)
    
    _result = _indices_sampled_per_interval_list if each else _indices_sampled 
    return _result

