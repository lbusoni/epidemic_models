from epidemic_models import sircd, seirah

import matplotlib.pyplot as plt
import numpy as np
from epidemic_models.restore_data import CSSECovid, DpcCovid
from epidemic_models.utils.exponential_fitting import tau_evolution, \
    doubling_time, daily_increment
from epidemic_models.utils import piecewise


def plotFB():
    strdates = 'Days (Hub +Jan1, I +Feb6)'

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


def doublingTime(what):
    dpcS = DpcCovid(DpcCovid.SUD)
    dpcC = DpcCovid(DpcCovid.CENTRO)
    dpcN = DpcCovid(DpcCovid.NORD)
    dpcI = DpcCovid(DpcCovid.ITALIA)

    ttS = tau_evolution(dpcS, what)
    ttC = tau_evolution(dpcC, what)
    ttN = tau_evolution(dpcN, what)
    ttI = tau_evolution(dpcI, what)

    plt.figure()
    plt.plot(ttS[0], doubling_time(ttS[1]), label='Sud')
    plt.plot(ttC[0], doubling_time(ttC[1]), label='Centro')
    plt.plot(ttN[0], doubling_time(ttN[1]), label='Nord')
    plt.plot(ttI[0], doubling_time(ttI[1]), label='Italia')
    plt.legend()
    plt.grid()


def plotTalkXiongLin():
    '''
    https://harvard.zoom.us/rec/play/v8Ytceqqqzs3GNzB4gSDB_59W9TsK6Ks13RI_6cLxB62BSUAOlumZeRAZLC7e1vif7xIyy6HL_uXyNHw?startTime=1584118874000
    '''

    strdates = 'Days (Hub +Jan1, I +Feb6)'

    csse = CSSECovid()
    deH, coH, daH = csse.hubei()
    deI, coI, daI = csse.italy()

    nSteps = 100
    delayModel = 0
    periods = np.array([10, 22, 32])

    S0 = 9999467
    E0 = 346
    I0 = 80
    R0 = 0
    A0 = 80
    H0 = 27
    beta = piecewise(periods, (1.75, 1.75, 0.58, 0.15), nSteps)
    r = piecewise(periods, (0.19, 0.19, 0.22, 0.17), nSteps)
    De = 5.2
    Di = 2.3
    Dh = 30
    Dq = piecewise(periods, (10, 7, 5, 2), nSteps)
    travellers = piecewise(periods, (500e3, 800e3, 0, 0), nSteps)

    system3 = seirah.SEIRAH(susceptibles=S0,
                            exposed=E0,
                            infectious=I0,
                            recovered=R0,
                            unascertained=A0,
                            hospitalized=H0,
                            transmission_rate=beta,
                            unscertained_transmission_rate_ratio=1,
                            ascertainment_fraction=r,
                            latent_period=De,
                            infectious_period=Di,
                            illness_to_hospitalization_period=Dq,
                            hospitalization_period=Dh,
                            inbound_outbound_travelers=travellers,
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


def howIsGoing(who):
    plotRegione(who, DpcCovid.NUOVI_TAMPONI)
    plotRegione(who, DpcCovid.NUOVI_DECEDUTI)
    plotRegione(who, DpcCovid.VARIAZIONE_TOTALE_POSITIVI)
    plotRegione(who, DpcCovid.NUOVI_DIMESSI_GUARITI)
    plotRegione(who, DpcCovid.NUOVI_CONTAGIATI)
    plt.semilogy()

