
from epidemic_models import sircd

import matplotlib.pyplot as plt
from epidemic_models.restore_data import CSSECovid, DpcCovid
import numpy as np


def plotEurope():

    csse = CSSECovid()
    deH, coH, reH, daH = csse.restoreHubei()
    deI, coI, reI, daI = csse.restoreItaly()
    deF, coF, reF, daF = csse.restoreFrance()
    deN, coN, reN, daN = csse.restoreNetherlands()
    deS, coS, reS, daS = csse.restoreSpain()

    pop = 6e7
    nSteps = 100
    cfr = 0.03
    delayModel = -1
    beta0 = 0.481
    gamma0 = 0.16

    system3 = sircd.SIRCD(susceptibles=pop,
                          infectives=1,
                          contact_rate=beta0,
                          average_infection_period=1 / gamma0,
                          epsilon=0.5,
                          delta=cfr,
                          nSteps=nSteps,
                          t0=delayModel)
    system3.evolveSystem()
    system3.plot(susceptibles=False, infectives=False, recovered=False,
                 confirmed=False, deaths=False)
    plt.plot(system3.timeSeries.timeVector, system3.timeSeries.confirmed,
             color='C7', linestyle='dotted',
             label='Confirmed eps=%g' % system3._epsilon[0])
    plt.plot(system3.timeSeries.timeVector, system3.timeSeries.deaths,
             color='C7', linestyle='dashed',
             label='Deaths delta=%g' % system3._delta[0])

    plt.plot(daH, deH, '.-', color='C8', label='deaths Hubei')
    plt.plot(daI, deI, '.-',
             linewidth=2,
             markersize=12,
             color='C4',
             label='deaths Italy')
    plt.plot(daF, deF, '.-', color='C0', label='deaths France')
    plt.plot(daS, deS, '.-', color='C3', label='deaths Spain')
    plt.plot(daN, deN, '.-', color='C1', label='deaths Netherlands')
    plt.plot(daH, coH, '.-', color='C8', label='confirmed Hubei')
    plt.plot(daI, coI, '.-', color='C4', label='confirmed Italy')
    plt.plot(daF, coF, '.-', color='C0', label='confirmed France')
    plt.plot(daS, coS, '.-', color='C3', label='confirmed Spain')
    plt.plot(daN, coN, '.-', color='C1', label='confirmed Netherlands')
    plt.ylim(1, 1e5)
    plt.xlim(0, 70)
    plt.xlabel(csse.string_dates())
    plt.legend()


def plotRegioni():
    dLomb = DpcCovid(DpcCovid.LOMBARDIA)
    dTosc = DpcCovid(DpcCovid.TOSCANA)


def plotReport1():
    pop = 6e7
    nSteps = 100
    epsilon = 0.001
    delta = 0.0001
    delayModel = -1
    beta0 = 0.481
    gamma0 = 0.16

    system3 = sircd.SIRCD(susceptibles=pop,
                          infectives=1,
                          contact_rate=beta0,
                          average_infection_period=1 / gamma0,
                          epsilon=epsilon,
                          delta=delta,
                          nSteps=nSteps,
                          t0=delayModel)
    system3.evolveSystem()
    system3.plot()
    plt.ylim(1,)
    return system3


def plotReport2():
    strdates = 'Days (Hubei from Jan1, Italy from Feb6)'

    csse = CSSECovid()
    deH, coH, reH, daH = csse.restoreHubei()

    pop = 6e7
    nSteps = 200
    beta0 = 0.48
    gamma0 = 0.16
    epsilon2 = 0.75
    cfr2 = 0.03
    delay_model2 = 0

    beta2 = np.zeros(nSteps)
    tInt2 = 32 - delay_model2
    beta2[:tInt2] = beta0
    beta2[tInt2:] = 0.8 * gamma0
    system2 = sircd.SIRCD(susceptibles=pop,
                          infectives=1,
                          contact_rate=beta2,
                          average_infection_period=1 / gamma0,
                          epsilon=epsilon2,
                          delta=cfr2,
                          nSteps=nSteps,
                          t0=delay_model2)
    system2.evolveSystem()
    # system2.plot(susceptibles=False, infectives=False, recovered=False)
    system2.plot()
    t = 'Social rarefaction R0=0.8 from day %d\n $\epsilon$ = %g\n' % (
        tInt2 + delay_model2, epsilon2)
    plt.title(t)
    plt.xlabel(strdates)
    plt.ylim(10,)
    plt.xlim(0, 100)

    plt.plot(daH, deH, '.-', color='C4', label='deaths Hubei')
    plt.plot(daH, coH, '.-', color='C3', label='confirmed Hubei')
    plt.legend()

    epsilon1 = 0.001
    cfr1 = 0.00005
    delay_model1 = -20
    system1 = sircd.SIRCD(susceptibles=pop,
                          infectives=1,
                          contact_rate=beta0,
                          average_infection_period=1 / gamma0,
                          epsilon=epsilon1,
                          delta=cfr1,
                          nSteps=nSteps,
                          t0=delay_model1)
    system1.evolveSystem()
    system1.plot()
    t = 'Constant contact_rate\n $\epsilon$ = %g\n' % (epsilon1)
    plt.title(t)
    plt.xlabel(strdates)
    plt.ylim(10,)
    plt.xlim(0, 100)
    plt.plot(daH, deH, '.-', color='C4', label='deaths Hubei')
    plt.plot(daH, coH, '.-', color='C3', label='confirmed Hubei')
    plt.legend()
