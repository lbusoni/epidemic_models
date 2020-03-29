from epidemic_models import simple_sir, restore_data, sircd

import matplotlib.pyplot as plt
import numpy as np
from epidemic_models.restore_data import CSSECovid, DpcCovid


def plotFB():
    strdates = 'Days (Hub +Jan1, I +Feb6)'

    csse = CSSECovid()
    deH, coH, daH = csse.restoreHubei()
    deI, coI, daI = csse.restoreItaly()

    pop = 6e7
    nSteps = 100
    epsilon = 0.75
    cfr = 0.03
    delayModel = -1
    beta0 = 0.48
    gamma0 = 0.16

    beta = np.zeros(nSteps)
    tInt2 = 31 - delayModel
    beta[:tInt2] = beta0
    beta[tInt2:] = 0.8 * gamma0
    system3 = sircd.SIRCD(susceptibles=pop,
                          infectious=1,
                          contact_rate=beta,
                          average_infection_period=1 / gamma0,
                          epsilon=epsilon,
                          delta=cfr,
                          nSteps=nSteps,
                          t0=delayModel)
    system3.evolveSystem()
    system3.plot(susceptibles=False, infectious=False, recovered=False,
                 confirmed=False, deaths=False)
    plt.plot(system3.timeSeries.timeVector,
             system3.timeSeries.deaths, color='C2', label='SIR model, R0=3')

    plt.plot(daH, deH, '.-', color='C3', label='deaths Hubei')
    plt.plot(daI, deI, '.-',
             linewidth=2,
             markersize=12,
             color='C4',
             label='deaths Italy')
    plt.plot([], [], ' ', label="data at 17 Mar 2020")
    plt.ylim(10, 1e4)
    plt.xlim(20, 60)
    plt.xlabel(strdates)
    plt.title('')
    plt.legend()

