"""Routines for evaluating time-of-flight of Bohmian particles"""


from numpy import exp, pi, asarray, sqrt


def prob_tof_single_gaussian_zero_central_momentum(t,sig,R):
    _t = asarray(t)
    tp = _t / (2.*sig**2)
    sigp = sig * sqrt(1+tp**2)
    rho_tof = R/(2.*sqrt(2.*pi)) * tp / sigp**3 * exp(-R*R / (2.*sigp**2))
    return rho_tof


def peak_of_prob_tof_single_gaussian_zero_central_momentum(sig,R):
    gamma = (R/sig)**2 - 1
    tof_peak = sig**2 * sqrt(gamma + sqrt(gamma**2 + 8))
    return tof_peak

