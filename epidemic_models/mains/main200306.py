'''
Created on Mar 6, 2020

@author: lbusoni
'''
from epidemic_models.restore_data import restoreCovid
from epidemic_models import simple_sir

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import convolve


def main():
    syncI2H = 27
    deH, coH, reH, daH = restoreCovid('Hubei')
    deI, coI, reI, daI = restoreCovid('Italy', fromItem=syncI2H)

    plt.figure()
    plt.plot(np.arange(len(deI)), deI, '.-', label='Deaths Italy')
    plt.plot(np.arange(len(deH)), deH, '.-', label='Deaths Hubei')
    t = "Evolution of deaths in Hubei and Italy (both 60M people)"
    plt.title(t)
    plt.legend()
    plt.grid(True)
    plt.ylabel('Total deaths')
    plt.xlabel('Time [days]. Arbitrary origin')
    plt.show()
    plt.semilogy()

    co2de = 0.04
    delay_co2de = 2
    ff = np.ones(int(delay_co2de)) / delay_co2de
    expDeH = co2de * convolve(coH, ff, mode='full')[:len(coH)]
    expDeI = co2de * convolve(coI, ff, mode='full')[:len(coI)]
    plt.figure()
    plt.plot(np.arange(len(deI)), deI, '.-', label='Deaths Italy')
    plt.plot(np.arange(len(deH)), deH, '.-', label='Deaths Hubei')
    plt.plot(np.arange(len(coI)), coI, '.-', label='Confirmed Italy')
    plt.plot(np.arange(len(coH)), coH, '.-', label='Confirmed Hubei')
    plt.plot(np.arange(len(expDeI)), expDeI, label='Expected Deaths Italy') 
    plt.plot(np.arange(len(expDeH)), expDeH, label='Expected Deaths Hubei')
    t = "Confirmed 2 Dead\n co2de=%g, delay=%g d" % (co2de, delay_co2de)
    plt.title(t)
    plt.legend()
    plt.grid(True)
    plt.ylabel('Total deaths')
    plt.xlabel('Time [days]. Arbitrary origin')
    plt.show()
    plt.semilogy()

    pop = 6e7
    system = simple_sir.SimpleSIR(pop, 1, 0, 0.4, 15, 100)
    system.evolveSystem()
    system.plot()

    cfr = 0.03
    deaths = cfr * system.timeSeries.recoveredWithImmunity
    plt.plot(deaths, label='deaths (CFR=%g)' % (cfr))

    plt.plot(np.arange(len(deH)) + 27, deH, '.-', label='deaths Hubei')
    plt.plot(np.arange(len(deI)) + 27, deI, '.-', label='deaths Italy')
    plt.plot(np.arange(len(coH)) + 27, coH, '.-', label='confirmed Hubei')
    plt.plot(np.arange(len(coI)) + 27, coI, '.-', label='confirmed Italy')
    plt.ylim(1,)
    plt.legend()

