'''
Created on Mar 6, 2020

@author: lbusoni
'''
from epidemic_models import simple_sir, restore_data

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import convolve


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


def plotFB():
    delayI = 36
    delayR = 34
    delayH = 0
    delayF = 45
    delayS = 45
    delayK = 35
    strdates = 'Days (Hub +Jan1, I +Feb6, F +Feb15)'

    deH, coH, reH, daH = _restoreCountry('Hubei/China', delayH)
    deI, coI, reI, daI = _restoreCountry('Italy', delayI)
    deF, coF, reF, daF = _restoreCountry('France/France', delayF)
    deR, coR, reR, daR = _restoreCountry('Iran', delayR)
    deS, coS, reS, daS = _restoreCountry('Spain', delayS)
    deK, coK, reK, daK = _restoreCountry('Korea, South', delayK)

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
    system.plot(susceptibles=False, infectives=False, recovered=False)
    deaths = cfr * system.timeSeries.recoveredWithImmunity
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
    deaths2 = cfr * system2.timeSeries.recoveredWithImmunity
    plt.plot(system2.timeSeries.timeVector,
             deaths2,
             label='deaths if R0=1 at day=%d' % (tInt2 + delayModel))

    beta4 = np.zeros(nSteps)
    beta4[:tInt2] = beta0
    beta4[tInt2:] = 0 * gamma0
    system4 = simple_sir.SimpleSIR(pop, 1, 0, beta4, 1 / gamma0,
                                   nSteps, t0=delayModel)
    system4.evolveSystem()
    deaths4 = cfr * system4.timeSeries.recoveredWithImmunity
    plt.plot(system4.timeSeries.timeVector,
             deaths4,
             label='deaths if R0=0 at day=%d' % (tInt2 + delayModel))

    system3 = simple_sir.SimpleSIR(pop, 1, 0, beta0, 1 / gamma0,
                                   nSteps, t0=delayModel)
    system3.evolveSystem()
    deaths3 = cfr * system3.timeSeries.recoveredWithImmunity
    plt.plot(system3.timeSeries.timeVector,
             deaths3, label='deaths no action')

    plt.plot(daH, deH, '.-', label='deaths Hubei')
    plt.plot(daI, deI, '.-',
             linewidth=2,
             markersize=12,
             label='deaths Italy')
    plt.plot(daF, deF, '.-', label='deaths France')
    # plt.plot(coHd + delayModel, coH, '.-', label='confirmed Hubei')
    # plt.plot(coId + delayModel, coI, '.-', label='confirmed Italy')
    plt.ylim(10, 1e5)
    plt.xlim(20, 70)
    plt.xlabel(strdates)
    plt.legend()
