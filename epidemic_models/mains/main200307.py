'''
Created on Mar 6, 2020

@author: lbusoni
'''
from epidemic_models import simple_sir, restore_data

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import convolve


def main():
    delayI2H = 36
    # deH, coH, reH, daH = restoreCovid('Hubei')
    # deI, coI, reI, daI = restoreCovid('Italy', fromItem=syncI2H)

    de = restore_data.restoreCSSEDeath()
    deH = de['Hubei/Mainland China'].values
    deHd = de['Hubei/Mainland China'].days
    deI = de['Italy'].values
    deId = de['Italy'].days
    co = restore_data.restoreCSSEConfirmed()
    coH = co['Hubei/Mainland China'].values
    coHd = co['Hubei/Mainland China'].days
    coI = co['Italy'].values
    coId = co['Italy'].days

    plt.figure()
    plt.plot(deId - delayI2H, deI, '.-', label='Deaths Italy')
    plt.plot(deHd, deH, '.-', label='Deaths Hubei')
    t = "Evolution of deaths in Hubei and Italy (both 60M people)"
    plt.title(t)
    plt.legend()
    plt.grid(True)
    plt.ylabel('Total deaths')
    plt.xlabel('Days (H from Jan1, I from Feb27)')
    plt.show()
    plt.semilogy()

    co2de = 0.04
    delay_co2de = 2
    ff = np.ones(int(delay_co2de)) / delay_co2de
    expDeH = co2de * convolve(coH, ff, mode='full')[:len(coH)]
    expDeI = co2de * convolve(coI, ff, mode='full')[:len(coI)]
    plt.figure()
    plt.plot(deId - delayI2H, deI, '.-', label='Deaths Italy')
    plt.plot(deHd, deH, '.-', label='Deaths Hubei')
    plt.plot(coId - delayI2H, coI, '.-', label='Confirmed Italy')
    plt.plot(coHd, coH, '.-', label='Confirmed Hubei')
    plt.plot(coId - delayI2H, expDeI, label='Expected Deaths Italy')
    plt.plot(coHd, expDeH, label='Expected Deaths Hubei')
    t = "Confirmed 2 Dead\n co2de=%g, delay=%g d" % (co2de, delay_co2de)
    plt.title(t)
    plt.legend()
    plt.grid(True)
    plt.ylabel('Total deaths')
    plt.xlabel('Days (Hubei from Jan 1, I from Feb 27)')
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
    plt.plot(deId - delayI2H + 6, deI, '.-', label='deaths Italy')
    plt.plot(coHd + 6, coH, '.-', label='confirmed Hubei')
    plt.plot(coId - delayI2H + 6, coI, '.-', label='confirmed Italy')
    plt.ylim(1,)
    plt.legend()

