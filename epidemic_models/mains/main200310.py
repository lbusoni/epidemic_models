'''
Created on Mar 6, 2020

@author: lbusoni
'''
from epidemic_models import simple_sir, restore_data

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import convolve


def main():
    delayI = 36
    delayR = 34
    delayH = 0
    strdates = 'Days (Hubei from Jan1, Italy from Feb6)'

    de = restore_data.restoreCSSEDeath()
    deH = de['Hubei/Mainland China'].values
    deHd = de['Hubei/Mainland China'].days - delayH
    deI = de['Italy'].values
    deId = de['Italy'].days - delayI
    deR = de['Iran'].values
    deRd = de['Iran'].days - delayR

    co = restore_data.restoreCSSEConfirmed()
    coH = co['Hubei/Mainland China'].values
    coHd = co['Hubei/Mainland China'].days - delayH
    coI = co['Italy'].values
    coId = co['Italy'].days - delayI
    coR = co['Iran'].values
    coRd = co['Iran'].days - delayR

    re = restore_data.restoreCSSERecovered()
    reH = re['Hubei/Mainland China'].values
    reHd = re['Hubei/Mainland China'].days - delayH
    reI = re['Italy'].values
    reId = re['Italy'].days - delayI
    reR = re['Iran'].values
    reRd = re['Iran'].days - delayR

    plt.figure()
    plt.plot(deHd, deH, '.-', label='Deaths Hubei')
    plt.plot(coHd, coH, '.-', label='Confirmed Hubei')
    plt.plot(reHd, reH, '.-', label='Recovered Hubei')
    plt.grid(True)
    plt.legend()
    plt.xlabel(strdates)
    plt.show()
    plt.semilogy()


def plotFB():
    delayI = 36
    delayH = 0
    strdates = 'Days (Hubei from Jan1, Italy from Feb6)'

    de = restore_data.restoreCSSEDeath()
    deH = de['Hubei/Mainland China'].values
    deHd = de['Hubei/Mainland China'].days - delayH
    deI = de['Italy'].values
    deId = de['Italy'].days - delayI

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
    tInt2 = 30 - delayModel
    beta2[:tInt2] = beta0
    beta2[tInt2:] = gamma0
    system2 = simple_sir.SimpleSIR(pop, 1, 0, beta2, 1 / gamma0,
                                   nSteps, t0=delayModel)
    system2.evolveSystem()
    deaths2 = cfr * system2.timeSeries.recovered_with_immunity
    plt.plot(system2.timeSeries.timeVector,
             deaths2,
             label='deaths if R0=1 at day=%d' % (tInt2 + delayModel))

    system3 = simple_sir.SimpleSIR(pop, 1, 0, beta0, 1 / gamma0,
                                   nSteps, t0=delayModel)
    system3.evolveSystem()
    deaths3 = cfr * system3.timeSeries.recovered_with_immunity
    plt.plot(system3.timeSeries.timeVector,
             deaths3, label='deaths no action')

    plt.plot(deHd, deH, '.-', label='deaths Hubei')
    plt.plot(deId, deI, '.-',
             linewidth=2,
             markersize=12,
             label='deaths Italy')
    # plt.plot(coHd + delayModel, coH, '.-', label='confirmed Hubei')
    # plt.plot(coId + delayModel, coI, '.-', label='confirmed Italy')
    plt.ylim(10,)
    plt.xlim(20, 75)
    plt.xlabel(strdates)
    plt.legend()


def plotGuido():
    delayH = 0
    strdates = 'Days (Hubei from Jan1, Italy from Feb6)'

    de = restore_data.restoreCSSEDeath()
    deH = de['Hubei/Mainland China'].values
    deHd = de['Hubei/Mainland China'].days - delayH

    pop = 6e7
    nSteps = 100
    cfr = 0.00006
    delayModel = -21
    beta0 = 0.481
    gamma0 = 0.16

    system3 = simple_sir.SimpleSIR(pop, 1, 0, beta0, 1 / gamma0,
                                   nSteps, t0=delayModel)
    system3.evolveSystem()
    system3.plot()
    deaths3 = cfr * system3.timeSeries.recovered_with_immunity
    plt.plot(system3.timeSeries.timeVector,
             deaths3, label='deaths no action cfr=%g' % cfr)

    plt.plot(deHd, deH, '.-', label='deaths Hubei')
    plt.ylim(1,)
    plt.xlim(10, 75)
    plt.xlabel(strdates)
    plt.legend()
 
