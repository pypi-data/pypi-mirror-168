"""routines for tridiagonal matrices"""

from numba import njit
import numpy as np
from numpy import asarray, conj


@njit
def tridiag_mul(tri,x):
    _tri, _x = asarray(tri), asarray(x)
    _b = np.empty_like(_x)
    assert _b.size == _tri.shape[1]
    _b[0] = _tri[1,0] * _x[0] + _tri[0,1] * _x[1]
    for _i in range(1,_x.shape[0]-1):
        _b[_i] = _tri[2,_i-1] * _x[_i-1] \
                + _tri[1,_i] * _x[_i] \
                + _tri[0,_i+1] * _x[_i+1]
    _b[-1] = _tri[2,-2] * _x[-2] + _tri[1,-1] * _x[-1]
    return _b



@njit
def tridiagh_mul(de,x):
    """
    Multiply the Hermitian tridiagonal with given vector `x`.
    The `de` is the diagonal and the off-diagonal of the Hermitian tridiagonal matrix.

    # Arguments
    de : array-like, (2,N)
        `de[1,:]` is the diagonal of the Hermitian trdiagonal matrix.
        `de[0,1:]` is the off-diagonal of the Hermitian trdiagonal matrix.
    x : array-like, (N,)
        The vector to be multiplied by the Hermitian trdiagonal matrix

    # Returns
    b : numpy.ndarray, (N,)
        The product of the Hermitian trdiagonal matrix and the given vector `x`
    """
    _x = asarray(x)
    _de = asarray(de)

    N = _de.shape[1]
    assert (_x.shape[-1] == N) and (_x.ndim >= 1)

    # [NOTE] _b also gets the dtype of `x`
    # -> but it may need revision to deal with a case
    # where _d or _e are complex but _x is real
    _b = np.empty_like(_x)

    _b[...,0] = _de[1,0] * _x[...,0] + _de[0,1] * _x[...,1]
    for _i in range(1,N-1):
        _b[...,_i] = np.conjugate(_de[0,_i]) * _x[...,_i-1] \
                + _de[1,_i] * _x[...,_i] \
                + _de[0,_i+1] * _x[...,_i+1]
    _b[...,-1] = np.conjugate(_de[0,-1]) * _x[...,-2] + _de[1,-1] * _x[...,-1]

    return _b






def oper_expect_1(op_de, state, thres=1e-15):
    """
    Evaluate expectation value of given operator.
    
    # Arguments
    op_de : array-like (2,N)
        The diagonal and the off-diagonal elements 
        of the operator in number-state basis.
        The state in the basis with maximal number is `N-1`.
    state : array-like (...,N)
        The state vector in number-state basis of length `N`.
    thres : float, positive
        The upper bound of imaginary part 
        of the calculated expectation values.
    """
    _state = asarray(state)
    _op_de = asarray(op_de)
    N = _state.shape[-1]
    assert _op_de.shape == (2,N)
    
    op_expect_complex = np.sum((conj(_state) * tridiagh_mul(_op_de, _state)), axis=-1)
    
    # Check whether the calculated expectation value is real-valued
    op_expect = None
    if np.any(np.imag(op_expect_complex) > 1e-15):
        raise ValueError("The expectation value may not be real-valued.")
    else: op_expect = np.real(op_expect_complex)
    assert op_expect is not None
    
    return op_expect






def d2trid(N,h):
    _tr = np.empty((3,N))
    _tr[0,1:] = 1
    _tr[1,:] = -2
    _tr[2,:-1] = 1
    _tr *= 1./h**2
    # For preventing overflow
    _tr[0,0] = 0.
    _tr[2,-1] = 0.
    return _tr

def eye_trid(N):
    _tr = np.empty((3,N))
    _tr[0,1:] = 0.
    _tr[1,:] = 1.
    _tr[2,:-1] = 0.
    # For preventing overflow
    _tr[0,0] = 0.
    _tr[2,-1] = 0.
    return _tr

def d1trid(N,h):
    d1tr = np.empty((3,N), dtype=np.float64)
    d1tr[0,1:] = 1./(2*h)
    d1tr[1,:] = 0.
    d1tr[2,:-1] = -1./(2*h)
    d1tr[0,1] = 0.
    return d1tr

