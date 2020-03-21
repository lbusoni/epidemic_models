
import numpy as np


class ExponentialFitResult():

    def __init__(self, tau, I0, t, y):
        self.tau = tau
        self.I0 = I0
        self.t = t
        self.y = y


def fit_exponential(t, y):
    '''
    y = A exp( t / tau)

    return ExponentialFitResult(tau, A, and best fit values (t,y)
    '''
    aa = np.polyfit(t, np.log(y), 1, w=np.sqrt(y))
    tau = 1 / aa[0]
    A = np.exp(aa[1])
    return ExponentialFitResult(tau, A, t, A * np.exp(t / tau))


def __tau_evolution(t, y, fit_samples=5):
    pass


def tau_evolution(dpcCovid, what, fit_samples=5):
    t = dpcCovid.days
    y = dpcCovid.select(what)
    valid = np.where(y > 10)[0]
    valid = valid[fit_samples:]
    dt = fit_samples
    ll = len(valid)
    tVect = np.zeros(ll)
    tauVect = np.zeros(ll)
    i = 0
    for idx0 in valid:
        aa = fit_exponential(t[idx0 - dt: idx0], y[idx0 - dt: idx0])
        tVect[i] = t[idx0]
        tauVect[i] = aa.tau
        i = i + 1
    return tVect, tauVect


def doubling_time(tau):
    return tau * np.log(2.)
