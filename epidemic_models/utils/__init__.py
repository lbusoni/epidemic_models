import numpy as np


def piecewise(when, what, nSteps):
    assert len(when) > 0
    assert len(when) + 1 == len(what)

    res = np.zeros(nSteps)
    res[0:when[0]] = what[0]
    for i in np.arange(1, len(when)):
        res[when[i - 1]:when[i]] = what[i]
    res[when[-1]:] = what[-1]
    return res

