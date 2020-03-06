'''
Created on Mar 6, 2020

@author: lbusoni
'''
from epidemic_models.restore_data import restoreCovid
from epidemic_models import simple_sir

import matplotlib.pyplot as plt
import numpy as np


def main():
    deH, daH = restoreCovid('Hubei')
    deI, daI = restoreCovid('Italy')

    plt.figure()
    plt.plot(np.arange(len(deI)), deI, label='Deaths Italy')
    plt.plot(np.arange(len(deH)) + 27, deH, label='Deaths Hubei')
    t = "Evolution of deaths in Hubei and Italy (both 60M people)"
    plt.title(t)
    plt.legend()
    plt.grid(True)
    plt.xlim(20,)
    plt.ylabel('Total deaths')
    plt.xlabel('Time [days]. Arbitrary origin')
    plt.show()
    plt.semilogy()

    pop = 6e7
    system = simple_sir.SimpleSIR(pop, 1, 0, 0.4, 15, 100)
    system.evolveSystem()
    system.plot()
    plt.plot(np.arange(len(deH)) + 10, deH, label='Hubei')
    plt.plot(np.arange(len(deI[17:])), deI[17:], label='Italy')
    plt.legend()

    pop = 6e7
    system = simple_sir.SimpleSIR(pop, 1, 0, 0.2, 15, 100)
    system.evolveSystem()
    system.plot()
    plt.plot(np.arange(len(deH)) + 10, deH, label='Hubei')
    plt.plot(np.arange(len(deI[17:])), deI[17:], label='Italy')
    plt.legend()

