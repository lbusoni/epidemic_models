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

    plt.figure()
    plt.plot(deId, deI, '.-', label='Deaths Italy')
    plt.plot(deRd, deR, '.-', label='Deaths Iran')
    plt.plot(deHd, deH, '.-', label='Deaths Hubei')
    t = "Evolution of deaths in Hubei, Italy, Iran"
    plt.title(t)
    plt.legend()
    plt.grid(True)
    plt.ylabel('Total deaths')
    plt.xlabel(strdates)
    plt.show()
    plt.semilogy()

    pop = 6e7
    nSteps = 100
    cfr = 0.03
    delayModel = -3
    beta = np.zeros(nSteps)
    tInt1 = 33
    beta[:tInt1] = 0.481
    beta[tInt1:] = 0.192
    gamma = 0.192
    system = simple_sir.SimpleSIR(pop, 1, 0, beta, 1 / gamma, nSteps,
                                  t0=delayModel)
    system.evolveSystem()
    system.plot(susceptibles=False, infectious=False, recovered=False)
    deaths = cfr * system.timeSeries.recovered_with_immunity
    plt.plot(system.timeSeries.timeVector,
             deaths,
             label='deaths if R0=1 at day=%d' % (tInt1 + delayModel))

    beta2 = np.zeros(nSteps)
    tInt2 = 40
    beta2[:tInt2] = 0.481
    beta2[tInt2:] = 0.192
    gamma2 = 0.192
    system2 = simple_sir.SimpleSIR(pop, 1, 0, beta2, 1 / gamma2,
                                   nSteps, t0=delayModel)
    system2.evolveSystem()
    deaths2 = cfr * system2.timeSeries.recovered_with_immunity
    plt.plot(system2.timeSeries.timeVector,
             deaths2,
             label='deaths if R0=1 at day=%d' % (tInt2 + delayModel))

    beta3 = 0.481
    gamma3 = 0.192
    system3 = simple_sir.SimpleSIR(pop, 1, 0, beta3, 1 / gamma3,
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

