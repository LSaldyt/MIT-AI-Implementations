from statistics import stdev, mean
from math       import sqrt

import scipy.stats as st

def ztest(samples, u):
    x = mean(samples)
    n = len(samples)
    return (x - u) / (stdev(samples)/ sqrt(n))

def to_p(z):
    p_values = st.norm.sf(z)
    return p_values
