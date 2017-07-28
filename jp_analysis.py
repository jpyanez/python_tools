import numpy as np
import pickle

gaus = lambda x, normalization, mean, sigma: normalization * np.exp(-0.5 * (x - mean)**2 / sigma**2)
two_gaus = lambda x, n1, m1, s1, n2, m2, s2: gaus(x, n1, m1, s1) + gaus(x, n2, m2, s2)
line_fcn = lambda x, m, b : m*x + b
from scipy import optimize

def getNorm(v):
    return v/np.linalg.norm(v)

def renormN(n, axis=0):
    n+= 1E-9

    integral = np.sum(n,axis=axis)
    if axis==0:
        return n/integral
    else:
        return (n.T/integral).T
    
def edgesToMiddle(x):
    return (x[1:]+x[:-1])/2.


def alignHistogram( reference = None,
                    test = None,
                    padding = 8): # Padding is in bin size
    padtest = np.concatenate((np.zeros(padding), test, np.zeros(padding)))
    prodmax = 0.
    shifted_histo = None
    for thispad in range(-padding, padding):
        new_hist = padtest[padding+thispad:-(padding-thispad)]
        new_prod = np.sum(reference*new_hist)
        if new_prod > prodmax:
            prodmax = new_prod
            shifted_histo = new_hist
    if prodmax == 0:
        return test
    else:
        return shifted_histo
