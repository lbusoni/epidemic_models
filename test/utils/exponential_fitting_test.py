#!/usr/bin/env python
import unittest
import numpy as np
from epidemic_models.utils.exponential_fitting import daily_increment, \
    doubling_time


class MyCovid():

    def __init__(self, t, v):
        self.t = t
        self.v = v

    @property
    def days(self):
        return self.t

    def select(self, what):
        return self.v


class ExponentialFittingTest(unittest.TestCase):

    def testDailyIncrement(self):
        want_inc = 0.32
        n_samples = 15
        fit_samples = 5
        tt = np.arange(n_samples)
        v = np.ones(n_samples)
        for i in np.arange(1, n_samples):
            v[i] = v[i - 1] * (1 + want_inc)
        t, inc = daily_increment(MyCovid(tt, v), 'foo', fit_samples=fit_samples)
        self.assertEqual(n_samples - fit_samples , len(t))
        self.assertTrue(np.allclose(want_inc, inc), "%s" % inc)

    def testDoublingTime(self):
        tau = 3.14
        n_samples = 15
        fit_samples = 5
        tt = np.arange(n_samples)
        v = np.exp(tt / tau)
        t, dou = doubling_time(MyCovid(tt, v), 'foo', fit_samples=fit_samples)
        self.assertEqual(n_samples - fit_samples, len(t))
        self.assertTrue(np.allclose(dou, tau * np.log(2)), "%s" % dou)

    def testDailyIncrementIsAveragedOnPreviousNSamplesValues(self):
        inc_1 = 0.32
        t_1 = 15
        inc_2 = 0.11
        t_2 = 15
        fit_samples = 5
        tt = np.arange(t_1 + t_2)
        v = np.ones(t_1 + t_2)
        for i in np.arange(1, t_1):
            v[i] = v[i - 1] * (1 + inc_1)
        for i in np.arange(t_1, t_1 + t_2):
            v[i] = v[i - 1] * (1 + inc_2)
        t, inc = daily_increment(MyCovid(tt, v), 'foo',
                                 fit_samples=fit_samples)
        self.assertEqual(t_1 + t_2 - fit_samples,
                         len(t))
        self.assertTrue(np.allclose(inc[0:t_1 - fit_samples],
                                    inc_1),
                        "%s" % inc)
        self.assertTrue(np.allclose(inc[t_1 + fit_samples:],
                                    inc_2),
                        "%s" % inc)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
