"""Expressions for potentials"""

from numpy import asarray, empty_like, sin, pi, cos

def vecpot_cos_sq(t, A0, omega, nc, cep):
    _ampl = A0 # 0.5
    _ome = omega # pi / 10.
    _ncycle = nc # 3. # 1.
    _cep = cep # 0. # pi/2.
    
    _t = asarray(t)
    _A_t = empty_like(_t)
    _T = 2.*pi / _ome
    _duration = _ncycle*_T
    _t_env_max = 0.5 * _duration
    _t_field_mask = _t < _duration
    _t_during_field = _t[_t_field_mask]
    _envel = (sin(pi/(_ncycle*_T)*_t_during_field))**2
    _phase_t = _ome*(_t_during_field-_t_env_max) + _cep
    _A_t[_t_field_mask] = _ampl * _envel * cos(_phase_t)
    _A_t[~_t_field_mask] = 0.
    return _A_t

