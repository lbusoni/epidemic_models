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
    strdates = 'Days (H from Jan1, I from Feb6, Ir from Feb4)'
    plt.xlabel(strdates)
    plt.show()
    plt.semilogy()

    co2de = 0.04
    delay_co2de = 2
    ff = np.ones(int(delay_co2de)) / delay_co2de
    expDeH = co2de * convolve(coH, ff, mode='full')[:len(coH)]
    expDeI = co2de * convolve(coI, ff, mode='full')[:len(coI)]
    expDeR = co2de * convolve(coR, ff, mode='full')[:len(coR)]
    plt.figure()
    plt.plot(deId, deI, '.-', label='Deaths Italy')
    plt.plot(deRd, deR, '.-', label='Deaths Iran')
    plt.plot(deHd, deH, '.-', label='Deaths Hubei')
    plt.plot(coId, coI, '.-', label='Confirmed Italy')
    plt.plot(coRd, coR, '.-', label='Confirmed Iran')
    plt.plot(coHd, coH, '.-', label='Confirmed Hubei')
    plt.plot(coId, expDeI, label='Expected Deaths Italy')
    plt.plot(coRd, expDeR, label='Expected Deaths Iran')
    plt.plot(coHd, expDeH, label='Expected Deaths Hubei')
    t = "Confirmed 2 Dead\n co2de=%g, delay=%g d" % (co2de, delay_co2de)
    plt.title(t)
    plt.legend()
    plt.grid(True)
    plt.ylabel('Total deaths')
    plt.xlabel(strdates)
    plt.ylim(1,)
    plt.show()
    plt.semilogy()

    pop = 6e7
    nSteps = 100
    beta = np.zeros(nSteps)
    beta[:36] = 0.4
    beta[36:] = 0.1
    system = simple_sir.SimpleSIR(pop, 1, 0, beta, 15, nSteps)
    system.evolveSystem()
    system.plot()

    cfr = 0.03
    deaths = cfr * system.timeSeries.recoveredWithImmunity
    plt.plot(deaths, label='deaths (CFR=%g)' % (cfr))

    plt.plot(deHd + 6, deH, '.-', label='deaths Hubei')
    plt.plot(deId + 6, deI, '.-', label='deaths Italy')
    plt.plot(deRd + 6, deR, '.-', label='deaths Iran')
    plt.plot(coHd + 6, coH, '.-', label='confirmed Hubei')
    plt.plot(coId + 6, coI, '.-', label='confirmed Italy')
    plt.plot(coRd + 6, coR, '.-', label='confirmed Iran')
    plt.ylim(1,)
    plt.legend()

