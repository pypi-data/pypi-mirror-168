"""Routines for manipulating arrays"""

from operator import gt, lt
from numbers import Integral

from numba import njit
from numpy import asarray, empty, arange, cumsum, nonzero

@njit
def first_index(a, val):
    """
    Find the first index `j` such that `func(a[j], val)` 
    where `func` denotes a comparison operator
    
    # Arguments
    a : (N,) array-like
    val : float, value to compare with
    """
    _a = asarray(a)
    assert _a.ndim == 1
    _N = _a.size
    _func = gt
    for _j in range(_N):
        if _func(_a[_j],val): break
    if _j == _N-1: return None
    return _j


# from numbers import Integral

def linspace_int(j,k,N):
    _args = (j,k,N)
    for _arg in _args: assert isinstance(_arg, Integral)
    _j, _k, _N = _args
    assert _N > 0
    assert _j < _k
    _res = empty((_N,), dtype=int)
    _res[0] = _j
    if _N == 1: pass
    else:
        _n = arange(1,_N)
        _offset = _k - _j
        _interval_n = (_offset//(_N-1)) + (_n <= (_offset%(_N-1)))
        _delta_n = cumsum(_interval_n)
        _res[1:] = _j + _delta_n
    return _res




# from numpy import asarray, nonzero, empty

def above_thres_range_indices(a, th):
    """
    Return indices of intervals in which `a > th`
    
    For example, if the returned indices is [[3,5],[8,11]],
    ```
    np.all(a[3:5+1] > th) == True
    ```
    and
    ```
    np.all(a[8:11+1] > th) == True
    ```
    
    # Arguments
    a : (N,) array-like
    th : a real number
    
    # Returns
    indices : (M,2) array-like
        M is the number of intervals in which `a > th`
    """
    
    _a = asarray(a)
    assert _a.ndim == 1
    _th = asarray(th)
    assert _th.shape == ()
    
    _tf = _a > _th

    _A, _B = _tf[:-1], _tf[1:]

    _XOR_A_B = _A ^ _B
    _i_F_to_T_arr, = nonzero(_XOR_A_B & _B)
    _i_T_to_F_arr, = nonzero(_XOR_A_B & _A)
    
    # [NOTE1] an index j in `_i_F_to_T_arr` is the index of F in FT sequence, 
    # and we need T part so we add +1. also, if FT sequence exist, that means 
    # that index j is not the same as N-1 (the last index) 
    # since there is at least T as the next entry.
    
    _N_FT, _N_TF = _i_F_to_T_arr.size, _i_T_to_F_arr.size
    _N_FT_minus_N_TF = _N_FT - _N_TF

    _N_interval = _N_FT + _tf[0]
    _indices_pair_of_intervals = empty((_N_interval, 2), dtype=int)
    
    if _tf[0] == True:
        assert _N_FT_minus_N_TF in (0,-1)
        _indices_pair_of_intervals[0,0] = 0
        _indices_pair_of_intervals[1:,0] = _i_F_to_T_arr + 1 
        _indices_pair_of_intervals[:_N_TF,1] = _i_T_to_F_arr # See [NOTE1]
        if _N_FT_minus_N_TF == 0: _indices_pair_of_intervals[-1,1] = _tf.size-1
    else: 
        assert _N_FT_minus_N_TF in (1,0)
        _indices_pair_of_intervals[:,0] = _i_F_to_T_arr + 1
        _indices_pair_of_intervals[:_N_TF,1] = _i_T_to_F_arr # See [NOTE1]
        if _N_FT_minus_N_TF == 1: _indices_pair_of_intervals[-1,1] = _tf.size-1
            
    return _indices_pair_of_intervals



