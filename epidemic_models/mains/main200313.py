'''
Created on Mar 6, 2020

@author: lbusoni
'''
from epidemic_models import simple_sir, restore_data, sircd

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import convolve
from epidemic_models.restore_data import CSSECovid


def _restoreCountry(name, delay_date):

    de = restore_data.restoreCSSEDeath()
    co = restore_data.restoreCSSEConfirmed()
    re = restore_data.restoreCSSERecovered()
    assert np.array_equal(de[name].days, co[name].days)
    assert np.array_equal(de[name].days, re[name].days)
    deaths = de[name].values
    confirmed = co[name].values
    recovered = re[name].values
    days = de[name].days - delay_date
    return deaths, confirmed, recovered, days


def main():
    delayI = 36
    delayR = 34
    delayH = 0
    delayF = 45
    delayS = 45
    delayK = 35
    strdates = 'Days (Hubei from Jan1, Italy from Feb6, France from Feb15)'

    deH, coH, reH, daH = _restoreCountry('Hubei/Mainland China', delayH)
    deI, coI, reI, daI = _restoreCountry('Italy', delayI)
    deF, coF, reF, daF = _restoreCountry('France', delayF)
    deR, coR, reR, daR = _restoreCountry('Iran (Islamic Republic of)', delayR)
    deS, coS, reS, daS = _restoreCountry('Spain', delayS)
    deK, coK, reK, daK = _restoreCountry('Republic of Korea', delayK)

    plt.figure()
    plt.plot(daH, deH, '.-', label='Deaths Hubei')
    plt.plot(daH, coH, '.-', label='Confirmed Hubei')
    plt.plot(daI, deI, '.-', label='Deaths Italy')
    plt.plot(daI, coI, '.-', label='Confirmed Italy')
    plt.plot(daR, deR, '.-', label='Deaths Iran')
    plt.plot(daR, coR, '.-', label='Confirmed Iran')
    plt.plot(daF, deF, '.-', label='Deaths France')
    plt.plot(daF, coF, '.-', label='Confirmed France')
    plt.plot(daS, deS, '.-', label='Deaths Spain')
    plt.plot(daS, coS, '.-', label='Confirmed Spain')
    plt.plot(daK, deK, '.-', label='Deaths S.Korea')
    plt.plot(daK, coK, '.-', label='Confirmed S.Korea')
    plt.grid(True)
    plt.legend()
    plt.xlabel(strdates)
    plt.show()
    plt.semilogy()


def plotGio():
    delayI = 36
    delayR = 34
    delayH = 0
    delayF = 45
    delayS = 45
    delayK = 35
    strdates = 'Days (Hub +Jan1, I +Feb6, F +Feb15, S +Feb15)'

    deH, coH, reH, daH = _restoreCountry('Hubei/China', delayH)
    deI, coI, reI, daI = _restoreCountry('Italy', delayI)
    deF, coF, reF, daF = _restoreCountry('France/France', delayF)
    # deR, coR, reR, daR = _restoreCountry('Iran', delayR)
    deS, coS, reS, daS = _restoreCountry('Spain', delayS)
    # deK, coK, reK, daK = _restoreCountry('Korea, South', delayK)

    pop = 6e7
    nSteps = 100
    cfr = 0.03
    delayModel = -1
    beta0 = 0.481
    gamma0 = 0.16

    beta = np.zeros(nSteps)
    tInt1 = 29 - delayModel
    beta[:tInt1] = beta0
    beta[tInt1:] = gamma0
    system = simple_sir.SimpleSIR(pop, 1, 0, beta, 1 / gamma0, nSteps,
                                  t0=delayModel)
    system.evolveSystem()
    system.plot(susceptibles=False, infectious=False, recovered=False)
    deaths = cfr * system.timeSeries.recovered_with_immunity
    plt.plot(system.timeSeries.timeVector,
             deaths,
             label='deaths if R0=1 at day=%d' % (tInt1 + delayModel))

    beta2 = np.zeros(nSteps)
    tInt2 = 32 - delayModel
    beta2[:tInt2] = beta0
    beta2[tInt2:] = gamma0
    system2 = simple_sir.SimpleSIR(pop, 1, 0, beta2, 1 / gamma0,
                                   nSteps, t0=delayModel)
    system2.evolveSystem()
    deaths2 = cfr * system2.timeSeries.recovered_with_immunity
    plt.plot(system2.timeSeries.timeVector,
             deaths2,
             label='deaths if R0=1 at day=%d' % (tInt2 + delayModel))

    beta4 = np.zeros(nSteps)
    beta4[:tInt2] = beta0
    beta4[tInt2:] = 0 * gamma0
    system4 = simple_sir.SimpleSIR(pop, 1, 0, beta4, 1 / gamma0,
                                   nSteps, t0=delayModel)
    system4.evolveSystem()
    deaths4 = cfr * system4.timeSeries.recovered_with_immunity
    plt.plot(system4.timeSeries.timeVector,
             deaths4,
             label='deaths if R0=0 at day=%d' % (tInt2 + delayModel))

    system3 = simple_sir.SimpleSIR(pop, 1, 0, beta0, 1 / gamma0,
                                   nSteps, t0=delayModel)
    system3.evolveSystem()
    deaths3 = cfr * system3.timeSeries.recovered_with_immunity
    plt.plot(system3.timeSeries.timeVector,
             deaths3, label='deaths no action')

    plt.plot(daH, deH, '.-', label='deaths Hubei')
    plt.plot(daI, deI, '.-',
             linewidth=2,
             markersize=12,
             label='deaths Italy')
    plt.plot(daF, deF, '.-', label='deaths France')
    # plt.plot(daS, deS, '.-', label='deaths Spain')
    # plt.plot(coHd + delayModel, coH, '.-', label='confirmed Hubei')
    # plt.plot(coId + delayModel, coI, '.-', label='confirmed Italy')
    plt.ylim(10, 1e5)
    plt.xlim(20, 70)
    plt.xlabel(strdates)
    plt.legend()


def plotFB():
    delayI = 36
    delayR = 34
    delayH = 0
    delayF = 45
    delayS = 45
    delayK = 35
    strdates = 'Days (Hub +Jan1, I +Feb6)'

    csse = CSSECovid()
    deH, coH, reH, daH = csse.restoreHubei()
    deI, coI, reI, daI = csse.restoreItaly()
    # deF, coF, reF, daF = csse.restoreFrance()
    # deR, coR, reR, daR = _restoreCountry('Iran', delayR)
    # deS, coS, reS, daS = csse.restoreSpain()
    # deK, coK, reK, daK = _restoreCountry('Korea, South', delayK)

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
                          epsilon=1,
                          delta=cfr,
                          nSteps=nSteps,
                          t0=delayModel)
    system3.evolveSystem()
    deaths3 = cfr * system3.timeSeries.recovered_with_immunity
    system3.plot(susceptibles=False, infectious=False, recovered=False,
                 confirmed=False, deaths=False)
    plt.plot(system3.timeSeries.timeVector,
             deaths3, color='C2', label='SIR model, R0=3')

    plt.plot(daH, deH, '.-', color='C3', label='deaths Hubei')
    plt.plot(daI, deI, '.-',
             linewidth=2,
             markersize=12,
             color='C4',
             label='deaths Italy')
    # plt.plot(daF, deF, '.-', label='deaths France')
    # plt.plot(daS, deS, '.-', label='deaths Spain')
    # plt.plot(coHd + delayModel, coH, '.-', label='confirmed Hubei')
    # plt.plot(coId + delayModel, coI, '.-', label='confirmed Italy')
    # Create empty plot with blank marker containing the extra label
    plt.plot([], [], ' ', label="data at 14 Mar 2020")
    plt.ylim(10, 1e4)
    plt.xlim(20, 60)
    plt.xlabel(strdates)
    plt.title('')
    plt.legend()


def plotLapo():
    pop = 6e7
    nSteps = 200
    cfr = 0.03
    delayModel = -1
    beta0 = 0.481
    gamma0 = 0.16
    lockDownTime = 60

    beta2 = np.zeros(nSteps)
    tInt2 = 32 - delayModel
    beta2[:tInt2] = beta0
    beta2[tInt2:tInt2 + lockDownTime] = 1.0 * gamma0
    beta2[tInt2 + lockDownTime:] = beta0
    system2 = sircd.SIRCD(susceptibles=pop,
                          infectious=1,
                          contact_rate=beta2,
                          average_infection_period=1 / gamma0,
                          epsilon=1,
                          delta=cfr,
                          nSteps=nSteps,
                          t0=delayModel)
    system2.evolveSystem()
    # system2.plot(susceptibles=False, infectious=False, recovered=False)
    system2.plot()
    deaths2 = 1.1 * cfr * system2.timeSeries.recovered_with_immunity
    plt.plot(system2.timeSeries.timeVector,
             deaths2,
             label='deaths if R0=1.0 from day %d to %d ' % (
                 tInt2 + delayModel, tInt2 + lockDownTime + delayModel))

    system3 = sircd.SIRCD(susceptibles=pop,
                          infectious=1,
                          contact_rate=beta0,
                          average_infection_period=1 / gamma0,
                          epsilon=1,
                          delta=cfr,
                          nSteps=nSteps,
                          t0=delayModel)
    system3.evolveSystem()
    system3.plot(susceptibles=False, infectious=True, recovered=False, newFigure=False)
    deaths3 = 1.1 * cfr * system3.timeSeries.recovered_with_immunity
    plt.plot(system3.timeSeries.timeVector,
             deaths3, label='deaths no action')

    plt.ylim(10,)
    plt.xlim(20,)
    plt.legend()


def plotLongPeriod():
    strdates = 'Days (Hub +Jan1)'

    csse = CSSECovid()
    deH, coH, reH, daH = csse.restoreHubei()

    pop = 6e7
    nSteps = 200
    cfr = 0.03
    beta0 = 0.481
    gamma0 = 0.16
    lock_down_period = 60

    epsilon2 = 0.75
    cfr2 = 0.03
    delay_model2 = 0

    beta2 = np.zeros(nSteps)
    tInt2 = 32 - delay_model2
    beta2[:tInt2] = beta0
    beta2[tInt2:tInt2 + lock_down_period] = 0.8 * gamma0
    beta2[tInt2 + lock_down_period:] = beta0
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
    t = 'Social rarefaction R0=0.8 from day %d to %d\nSymptomatic/asymptomatic = %g\n' % (
        tInt2 + delay_model2, tInt2 + lock_down_period + delay_model2, epsilon2)
    plt.title(t)
    plt.ylim(10,)
    plt.xlim(0, 150)

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
    t = 'Constant contact_rate\nSymptomatic/asymptomatic = %g\n' % (epsilon1)
    plt.title(t)
    plt.ylim(10,)
    plt.xlim(0, 100)
    plt.plot(daH, deH, '.-', color='C4', label='deaths Hubei')
    plt.plot(daH, coH, '.-', color='C3', label='confirmed Hubei')
    plt.legend()


def speed(R0):
    strdates = 'Days (Hub +Jan1)'

    csse = CSSECovid()
    deH, coH, reH, daH = csse.restoreHubei()

    pop = 6e7
    nSteps = 500
    gamma = 0.16
    beta = gamma * R0

    epsilon2 = 1
    cfr2 = 0.03
    delay_model2 = 0

    system2 = sircd.SIRCD(susceptibles=pop,
                          infectious=1,
                          contact_rate=beta,
                          average_infection_period=1 / gamma,
                          epsilon=epsilon2,
                          delta=cfr2,
                          nSteps=nSteps,
                          t0=delay_model2)
    system2.evolveSystem()
    system2.plot()
    t = 'R0=%g\nSymptomatic/asymptomatic = %g\n' % (
        system2.R0[0], epsilon2)
    plt.title(t)
    plt.ylim(10,)
    plt.xlim(0,)

#    plt.plot(daH, deH, '.-', color='C4', label='deaths Hubei')
#    plt.plot(daH, coH, '.-', color='C3', label='confirmed Hubei')
    plt.legend()

    return system2
