
from epidemic_models import sircd

import matplotlib.pyplot as plt
from epidemic_models.restore_data import CSSECovid, DpcCovid
import numpy as np
from epidemic_models.utils.plotting import dataAtToday


def plotEurope():

    csse = CSSECovid()
    deH, coH, daH = csse.hubei()
    deI, coI, daI = csse.italy()
    deF, coF, daF = csse.france()
    deN, coN, daN = csse.netherlands()
    deE, coE, daE = csse.spain()
    deU, coU, daU = csse.uk()
    deG, coG, daG = csse.germany()
    deK, coK, daK = csse.south_korea()
    deS, coS, daS = csse.sweden()
    deUs, coUs, daUs = csse.usa()

    pop = 6e7
    nSteps = 100
    cfr = 0.03
    delayModel = -1
    beta0 = 0.481
    gamma0 = 0.16

    system3 = sircd.SIRCD(susceptibles=pop,
                          infectious=1,
                          contact_rate=beta0,
                          average_infection_period=1 / gamma0,
                          epsilon=0.5,
                          delta=cfr,
                          nSteps=nSteps,
                          t0=delayModel)
    system3.evolveSystem()
    system3.plot(susceptibles=False, infectious=False, recovered=False,
                 confirmed=False, deaths=False)
    plt.plot(system3.timeSeries.timeVector, system3.timeSeries.confirmed,
             color='C7', linestyle='dotted',
             label='Confirmed $\epsilon$=%g' % system3._epsilon[0])
    plt.plot(system3.timeSeries.timeVector, system3.timeSeries.deaths,
             color='C7', linestyle='dashed',
             label=r'Deaths $\tau$=%.2g days' % system3.tau[0])

    plt.plot(daH, deH, '.-', color='C8', label='deaths Hubei')
    plt.plot(daI, deI, '.-',
             linewidth=2,
             markersize=12,
             color='C4',
             label='deaths Italy')
    plt.plot(daF, deF, '.-', color='C0', label='deaths France')
    plt.plot(daE, deE, '.-', color='C3', label='deaths Spain')
    plt.plot(daN, deN, '.-', color='C1', label='deaths Netherlands')
    plt.plot(daU, deU, '.-', color='C2', label='deaths UK')
    plt.plot(daG, deG, '.-', color='C7', label='deaths Germany')
    plt.plot(daK, deK, '.-', color='C6', label='deaths South Korea')
    plt.plot(daS, deS, '.-', color='C9', label='deaths Sweden')
    plt.plot(daUs, deUs, '.-', color='C5', label='deaths USA')
    plt.plot(daH, coH, 'x-', color='C8', label='confirmed Hubei')
    plt.plot(daI, coI, 'x-', color='C4', label='confirmed Italy')
    plt.plot(daF, coF, 'x-', color='C0', label='confirmed France')
    plt.plot(daE, coE, 'x-', color='C3', label='confirmed Spain')
    plt.plot(daN, coN, 'x-', color='C1', label='confirmed Netherlands')
    plt.plot(daU, coU, 'x-', color='C2', label='confirmed UK')
    plt.plot(daG, coG, 'x-', color='C7', label='confirmed Germany')
    plt.plot(daK, coK, 'x-', color='C6', label='confirmed South Korea')
    plt.plot(daS, coS, 'x-', color='C9', label='confirmed Sweden')
    plt.plot(daUs, coUs, 'x-', color='C5', label='confirmed USA')
    plt.ylim(1, 1e6)
    plt.xlim(0, 80)
    plt.xlabel(csse.string_dates())
    plt.title('')
    plt.plot([], [], ' ', label=dataAtToday())
    plt.legend()


def plotEuropeDeath():

    csse = CSSECovid()
    deH, coH, daH = csse.hubei()
    deI, coI, daI = csse.italy()
    deF, coF, daF = csse.france()
    deN, coN, daN = csse.netherlands()
    deE, coE, daE = csse.spain()
    deU, coU, daU = csse.uk()
    deG, coG, daG = csse.germany()
    deK, coK, daK = csse.south_korea()
    deS, coS, daS = csse.sweden()
    deUs, coUs, daUs = csse.usa()

    pop = 6e7
    nSteps = 100
    cfr = 0.03
    delayModel = -1
    beta0 = 0.481
    gamma0 = 0.16

    system3 = sircd.SIRCD(susceptibles=pop,
                          infectious=1,
                          contact_rate=beta0,
                          average_infection_period=1 / gamma0,
                          epsilon=0.5,
                          delta=cfr,
                          nSteps=nSteps,
                          t0=delayModel)
    system3.evolveSystem()
    system3.plot(susceptibles=False, infectious=False, recovered=False,
                 confirmed=False, deaths=False)

    plt.plot(daH, deH, '.-', color='C8', label='deaths Hubei')
    plt.plot(daI, deI, '.-',
             linewidth=2,
             markersize=12,
             color='C4',
             label='deaths Italy')
    plt.plot(daF, deF, '.-', color='C0', label='deaths France')
    plt.plot(daE, deE, '.-', color='C3', label='deaths Spain')
    plt.plot(daN, deN, '.-', color='C1', label='deaths Netherlands')
    plt.plot(daU, deU, '.-', color='C2', label='deaths UK')
    plt.plot(daG, deG, '.-', color='C7', label='deaths Germany')
    plt.plot(daK, deK, '.-', color='C6', label='deaths South Korea')
    plt.plot(daS, deS, '.-', color='C9', label='deaths Sweden')
    plt.plot(daUs, deUs, '.-', color='C5', label='deaths USA')
    plt.ylim(10, 1e6)
    plt.xlim(10, 80)
    plt.xlabel(csse.string_dates())
    plt.title('')
    plt.plot([], [], ' ', label=dataAtToday())
    plt.legend()


def plotReport1():
    pop = 6e7
    nSteps = 100
    epsilon = 0.001
    delta = 0.0001
    delayModel = -1
    beta0 = 0.481
    gamma0 = 0.16

    system3 = sircd.SIRCD(susceptibles=pop,
                          infectious=1,
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
    deH, coH, daH = csse.hubei()

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
                          infectious=1,
                          contact_rate=beta2,
                          average_infection_period=1 / gamma0,
                          epsilon=epsilon2,
                          delta=cfr2,
                          nSteps=nSteps,
                          t0=delay_model2)
    system2.evolveSystem()
    # system2.plot(susceptibles=False, infectious=False, recovered=False)
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
                          infectious=1,
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


def plotForecast():
    csse = CSSECovid()
    deH, coH, daH = csse.hubei()
    deI, coI, daI = csse.italy()

    pop = 6e7
    nSteps = 100
    epsilon = 0.75
    cfr = 0.03
    delayModel = -1
    beta0 = 0.48
    gamma0 = 0.16

    beta2 = np.zeros(nSteps)
    tInt2 = 31 - delayModel
    beta2[:tInt2] = beta0
    beta2[tInt2:] = 0.8 * gamma0
    system3 = sircd.SIRCD(susceptibles=pop,
                          infectious=1,
                          contact_rate=beta2,
                          average_infection_period=1 / gamma0,
                          epsilon=epsilon,
                          delta=cfr,
                          nSteps=nSteps,
                          t0=delayModel)
    system3.evolveSystem()
    system3.plot(susceptibles=False, infectious=False, recovered=False,
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
    plt.plot(daH, coH, '.-', color='C8', label='confirmed Hubei')
    plt.plot(daI, coI, '.-', color='C4', label='confirmed Italy')
    plt.ylim(1, 1e5)
    plt.xlim(0, 70)
    plt.xlabel(csse.string_dates())
    plt.legend()

