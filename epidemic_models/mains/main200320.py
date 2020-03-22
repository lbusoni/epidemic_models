from epidemic_models import simple_sir, restore_data, sircd

import matplotlib.pyplot as plt
import numpy as np
from epidemic_models.restore_data import CSSECovid, DpcCovid
from epidemic_models.utils.exponential_fitting import tau_evolution, \
    doubling_time


def plotFB():
    strdates = 'Days (Hub +Jan1, I +Feb6)'

    csse = CSSECovid()
    deH, coH, reH, daH = csse.restoreHubei()
    deI, coI, reI, daI = csse.restoreItaly()

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
                          infectives=1,
                          contact_rate=beta,
                          average_infection_period=1 / gamma0,
                          epsilon=epsilon,
                          delta=cfr,
                          nSteps=nSteps,
                          t0=delayModel)
    system3.evolveSystem()
    system3.plot(susceptibles=False, infectives=False, recovered=False,
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


def doublingTime(what):
    dpcS = DpcCovid(DpcCovid.SUD)
    dpcC = DpcCovid(DpcCovid.CENTRO)
    dpcN = DpcCovid(DpcCovid.NORD)
    dpcIs = DpcCovid(DpcCovid.ISOLE)
    dpcI = DpcCovid(DpcCovid.ALL)

    ttS = tau_evolution(dpcS, what)
    ttC = tau_evolution(dpcC, what)
    ttN = tau_evolution(dpcN, what)
    ttIs = tau_evolution(dpcIs, what)
    ttI = tau_evolution(dpcI, what)

    plt.figure()
    plt.plot(ttS[0], doubling_time(ttS[1]), label='Sud')
    plt.plot(ttC[0], doubling_time(ttC[1]), label='Centro')
    plt.plot(ttN[0], doubling_time(ttN[1]), label='Nord')
    plt.plot(ttIs[0], doubling_time(ttIs[1]), label='Isole')
    plt.plot(ttI[0], doubling_time(ttI[1]), label='Italia')
    plt.legend()
    plt.grid()


def plotTalkXiongLin():
    '''
    https://harvard.zoom.us/rec/play/v8Ytceqqqzs3GNzB4gSDB_59W9TsK6Ks13RI_6cLxB62BSUAOlumZeRAZLC7e1vif7xIyy6HL_uXyNHw?startTime=1584118874000
    '''

    strdates = 'Days (Hub +Jan1, I +Feb6)'

    csse = CSSECovid()
    deH, coH, reH, daH = csse.restoreHubei()
    deI, coI, reI, daI = csse.restoreItaly()

    pop = 11e6
    nSteps = 100
    epsilon = 0.4
    cfr = 0.03
    delayModel = -1

    Rt = np.array([3.88, 1.26, 0.32])
    gamma = 0.16
    betat = Rt * gamma
    tInt1 = 23 - delayModel
    tInt2 = 33 - delayModel

    beta = np.zeros(nSteps)
    beta[:tInt1] = betat[0]
    beta[tInt1:tInt2] = betat[1]
    beta[tInt2:] = betat[2]
    system3 = sircd.SIRCD(susceptibles=pop,
                          infectives=.5,
                          contact_rate=beta,
                          average_infection_period=1 / gamma,
                          epsilon=epsilon,
                          delta=cfr,
                          nSteps=nSteps,
                          t0=delayModel)
    system3.evolveSystem()
    system3.plot()
#    plt.plot(system3.timeSeries.timeVector,
#             system3.timeSeries.deaths, color='C2', label='SIRCD model')

    plt.plot(daH, deH, '.-', color='C3', label='deaths Hubei')
    plt.plot(daH, coH, '+-', color='C3', label='confirmed Hubei')
#     plt.plot(daI, deI, '.-',
#              linewidth=2,
#              markersize=12,
#              color='C4',
#              label='deaths Italy')
    plt.plot([], [], ' ', label="data at 20 Mar 2020")
    # plt.ylim(10, 1e4)
    # plt.xlim(20, 60)
    plt.xlabel(strdates)
    plt.title('')
    plt.legend()
    return system3
