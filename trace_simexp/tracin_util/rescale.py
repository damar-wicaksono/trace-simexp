# -*- coding: utf-8 -*-
"""Module with functions to scale a univariate [0, 1] samples to a specified
distribution
"""

__author__ = "Damar Wicaksono"


def uniform(quantile, min_val, max_val):
    """Rescale uniform random number into a uniform distribution

    Rescale the uniformly sampled value [0,1] into a value taken of a
    uniform distribution with support of [min_val, max_val].

    :param quantile: (float) the sample taken from uniform distribution [0,1]
    :param min_val: (float) the minimum value of this uniform distribution
    :param max_val: (float) the maximum value of this uniform distribution
    :returns: (float) the rescaled value
    """
    if quantile > 1.0:
        raise ValueError("{} is not a valid [0, 1] quantile" .format(quantile))
    if quantile < 0.0:
        raise ValueError("{} is not a valid [0, 1] quantile" .format(quantile))
    if min_val >= max_val:
        raise ValueError("min value is greater than or the same as the max")
    else:
        unif = quantile * (max_val - min_val) + min_val

    return unif


def discrete(quantile, choices):
    r"""Rescale uniform random number according to a discrete unif distribution

    :param quantile: (float) the sample taken from univariate distribution [0,1]
    :param choices: (list of int) the choices of value
    :return: (int) the choice picked based on the sampled quantile
    """
    if quantile > 1.0:
        raise ValueError("{} is not a valid [0, 1] quantile" .format(quantile))
    elif quantile < 0.0:
        raise ValueError("{} is not a valid [0, 1] quantile" .format(quantile))
    elif not isinstance(choices, list):
        raise ValueError("{} is not a valid list of choices" .format(choices))
    else:
        num_choices = len(choices)
        choice_odd = []
        for i in range(1, num_choices):
            choice_odd.append(i/float(num_choices))
        for i, odd in enumerate(choice_odd):
            if quantile < odd:
                choice = choices[i]
                break
            else:
                choice = choices[i+1]
    return choice


def loguniform(quantile, min_val, max_val):
    """Rescale uniform random number into a log-uniform distribution

    Rescale the uniformly sampled value [0,1] into a value taken of a
    log-uniform distribution with support of [min_val, max_val].

    :param quantile: (float) the sample taken from uniform distribution [0,1]
    :param min_val: (float) the minimum value of this log-uniform distribution
    :param max_val: (float) the maximum value of this log-uniform distribution
    :returns: (float) the rescaled value
    """
    from math import log, e

    if quantile > 1.0:
        raise ValueError("{} is not a valid [0, 1] quantile" .format(quantile))
    if quantile < 0.0:
        raise ValueError("{} is not a valid [0, 1] quantile" .format(quantile))
    if min_val >= max_val:
        raise ValueError("min value is greater than or the same as the max")
    else:
        logunif = quantile * (log(max_val) - log(min_val)) + log(min_val)
        logunif = e**logunif

    return logunif


def normal(quantile, mean=0, variance=1, truncations_level=0):
    """Rescale uniform random number into a normal distribution

    Rescale the uniformly sampled value [0,1] into a value taken of a
    normal distribution with given mean and variance (not standard dev.)

    If mean and variance is not given then the standard normal distribution
    will be used instead

    Truncation (cut-off) values have to be given and used to rescale the
    distribution in uniform distribution.

    :param quantile: (float) the sample taken from uniform distribution [0,1]
    :param truncations: (list of float) (2 elements) the truncation bound of 
        the normal distribution, e.g. [0.005, 0.995]
    :param mean: (float, optional) the mean value of the normal distribution
    :param variance: (float, optional) the variance of normal distribution
    :returns: (float) the rescaled value
    """
    from scipy.special import erfinv
    from math import sqrt

    if variance < 0.:
        raise ValueError("Variance has to be positive")
    else:
        if truncations_level == 0:
            norm = mean + sqrt(2*variance) * erfinv(2*quantile-1)
        else:
            # Truncated at both ends, renormalized the quantile
            quantile = uniform(quantile, 
                               (truncations_level/2)/100.0, 
                               (100 - truncations_level/2)/100.0)
            norm = mean + sqrt(2*variance) * erfinv(2*quantile-1)

    return norm
