# -*- coding: utf-8 -*-
"""

    trace_simexp.tracin_util.rescale
    ********************************

    Module with functions to scale a univariate [0, 1] samples to a specified
    distribution
"""

__author__ = "Damar Wicaksono"


def uniform(quantile: float, min_val: float, max_val: float) -> float:
    """Rescale uniform random number into a uniform dist. of a given support

    Rescale the uniformly sampled value [0,1] into a value taken of a
    uniform distribution with support of [min_val, max_val].

    :param quantile: the sample taken from uniform distribution [0,1]
    :param min_val: the minimum value of the uniform distribution
    :param max_val: the maximum value of the uniform distribution
    :return: the rescaled value in the specified uniform distribution
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


def discrete(quantile: float, choices: dict):
    r"""Make a random selection between choices based on their probabilities

    :param quantile: the sample taken from uniform distribution [0,1]
    :param choices: the choices (key) and their probability (value)
    :return: the choice picked based on the sampled quantile
    """
    import numpy as np

    choice = None

    if quantile > 1.0:
        raise ValueError("{} is not a valid [0, 1] quantile" .format(quantile))
    elif quantile < 0.0:
        raise ValueError("{} is not a valid [0, 1] quantile" .format(quantile))
    elif not isinstance(choices, dict):
        raise ValueError("{} is not a valid dict of choices" .format(choices))
    else:
        # Convert everything to lists and create cumulative sum of probability
        keys_list = []
        vals_list = []
        vals_cum = 0.0
        for key, val in choices.items():
            vals_cum += val
            vals_list.append(vals_cum)
            keys_list.append(key)

        # Sort the values and the keys accordingly
        keys_array = np.array(keys_list)
        vals_array = np.array(vals_list)
        keys_array = keys_array[vals_array.argsort()]
        vals_array.sort()   # ascending order

        # Make selection of the choices based on the sampled quantile value
        for i, val in enumerate(vals_array):
            if quantile <= val:
                choice = keys_array[i]
                break

    return choice


def loguniform(quantile: float, min_val: float, max_val: float) -> float:
    """Rescale uniform random number into a value from a log-uniform dist.

    Rescale the uniformly sampled value [0,1] into a value taken of a
    log-uniform distribution with support of [min_val, max_val].

    :param quantile: the sample taken from uniform distribution [0,1]
    :param min_val: the minimum value of this log-uniform distribution
    :param max_val: the maximum value of this log-uniform distribution
    :return: the rescaled value in the specified log-uniform distribution
    """
    from math import log, e

    if quantile > 1.0:
        raise ValueError("{} is not a valid [0, 1] quantile" .format(quantile))
    elif quantile < 0.0:
        raise ValueError("{} is not a valid [0, 1] quantile" .format(quantile))
    elif min_val >= max_val:
        raise ValueError("min value is greater than or the same as the max")
    elif min_val < 0 or max_val < 0:
        raise ValueError("the support of log-unif has to be positive")
    else:
        logunif = quantile * (log(max_val) - log(min_val)) + log(min_val)
        logunif = e**logunif

    return logunif


def normal(quantile: float, mu: float=0, sigma: float=1,
           truncations_level: float=0) -> float:
    """Rescale uniform random number into a value from a normal distribution

    Rescale the uniformly sampled value [0,1] into a value taken from a
    normal distribution with given mean and standard deviation

    If the mean and the sigma are not given then the standard normal
    distribution will be used instead (i.e., mu = 0.0, sigma = 1.0)

    Truncation level (cut-off) in 2 sided-percentile can be given to truncate
    the normal distribution at both ends. For example, `
    truncations_level` = 10, truncate the 5% percent of the distribution at
    each side. This is useful for the case of which the value at the design
    matrix include exactly 0.0 and 1.0

    :param quantile: the sample taken from uniform distribution [0,1]
    :param mu: the mean of the normal distribution
    :param sigma: the standard deviation of the normal distribution
    :param truncations_level: the symmetric truncation level at both ends
    :return: the rescaled value in the specified normal distribution
    """
    import scipy.special
    from math import sqrt

    if sigma < 0.:
        raise ValueError("Sigma has to be positive")
    elif truncations_level >= 100:
        raise ValueError("Truncations level >= 100%")
    else:
        if truncations_level == 0:
            norm = mu + sigma*sqrt(2) * scipy.special.erfinv(2 * quantile - 1)
        else:
            # Truncated at both ends, renormalized the quantile
            quantile = uniform(quantile, 
                               (truncations_level/2)/100.0, 
                               (100 - truncations_level/2)/100.0)
            norm = mu + sigma*sqrt(2) * scipy.special.erfinv(2 * quantile - 1)

    return norm
