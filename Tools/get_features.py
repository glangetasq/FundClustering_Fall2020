""" Feature generating functions used for labelling part """

import numpy as np
import pandas as pd

rf = 0.0001 # assumption


def get_positive_length(ts):
    """
    Give the maximum number of days that a timeserie was positive.

    Input:
        ts: timeserie, array-like
    Output:
        m: max positive length of the timeserie.
    """
    ranges = []
    n = len(ts)
    length = 0
    for i in range(n):
        if ts[i] > 0:
            length += 1
        else:
            if length != 0:
                ranges.append(length)
            length = 0
    if length > 0:
        ranges.append(length)
    return 0 if len(ranges) == 0 else max(ranges)

def get_negative_length(ts):
    """
    Give the maximum number of days that a timeserie was negative.

    Input:
        ts: timeserie, array-like
    Output:
        m: max negative length of the timeserie.
    """
    ranges = []
    n = len(ts)
    length = 0
    for i in range(n):
        if ts[i] < 0:
            length += 1
        else:
            if length != 0:
                ranges.append(length)
            length = 0
    if length < 0:
        ranges.append(length)
    return 0 if len(ranges) == 0 else max(ranges)

def maxdd(ts):
    """
    Get max-drawdown of timeserie.

    Input:
        ts: timeserie, array-like
    Output:
        max draw-down, float
    """
    cum_ret = np.concatenate(([1],(ts+1).cumprod()))
    return float(-((pd.DataFrame(cum_ret)-pd.DataFrame(cum_ret).cummax())/pd.DataFrame(cum_ret).cummax()).min())

def beta(ts, market):
    """
    Give the beta of the timeserie related to the market (cf. CAPM)
    """
    cov = np.cov(ts,market)[0,1]
    var = np.var(market)
    return cov/var
