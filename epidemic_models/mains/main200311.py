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
    strdates = 'Days (Hubei from Jan1, Italy from Feb6)'

    deH, coH, reH, daH = _restoreCountry('Hubei/China', delayH)
    deI, coI, reI, daI = _restoreCountry('Italy', delayI)
    deF, coF, reF, daF = _restoreCountry('France/France', delayF)
    deR, coR, reR, daR = _restoreCountry('Iran', delayR)
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


def plotTuttoAZero():
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
    system.plot(susceptibles=False, infectives=False, recovered=False)
    deaths = cfr * system.timeSeries.recoveredWithImmunity
    plt.plot(system.timeSeries.timeVector,
             deaths,
             label='deaths if R0=1 at day=%d' % (tInt1 + delayModel))

    beta2 = np.zeros(nSteps)
    tInt2 = 32 - delayModel
    beta2[:tInt2] = beta0
    beta2[tInt2:] = gamma0 * 0.
    system2 = simple_sir.SimpleSIR(pop, 1, 0, beta2, 1 / gamma0,
                                   nSteps, t0=delayModel)
    system2.evolveSystem()
    deaths2 = cfr * system2.timeSeries.recoveredWithImmunity
    plt.plot(system2.timeSeries.timeVector,
             deaths2,
             label='deaths if R0=1 at day=%d' % (tInt2 + delayModel))

    system3 = simple_sir.SimpleSIR(pop, 1, 0, beta0, 1 / gamma0,
                                   nSteps, t0=delayModel)
    system3.evolveSystem()
    deaths3 = cfr * system3.timeSeries.recoveredWithImmunity
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
    deH = de['Hubei/China'].values
    deHd = de['Hubei/China'].days - delayH

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
    deaths3 = cfr * system3.timeSeries.recoveredWithImmunity
    plt.plot(system3.timeSeries.timeVector,
             deaths3, label='deaths no action cfr=%g' % cfr)

    plt.plot(deHd, deH, '.-', label='deaths Hubei')
    plt.ylim(1,)
    plt.xlim(10, 75)
    plt.xlabel(strdates)
    plt.legend()


def delays():
    delayI = 36
    delayR = 34
    delayH = 0
    delayF = 45
    delayS = 45
    delayK = 35
    strdates = 'Days (Hubei from Jan1, Italy from Feb6)'

    deH, coH, reH, daH = _restoreCountry('Hubei/China', delayH)
    deI, coI, reI, daI = _restoreCountry('Italy', delayI)
#    deF, coF, reF, daF = _restoreCountry('France', delayF)
#    deR, coR, reR, daR = _restoreCountry('Iran (Islamic Republic of)', delayR)
#    deS, coS, reS, daS = _restoreCountry('Spain', delayS)
#    deK, coK, reK, daK = _restoreCountry('Republic of Korea', delayK)

    pop = 6e7
    nSteps = 100
    beta0 = 0.48
    gamma0 = 0.16
    epsilon = 0.005
    cfr = 0.0005
    delayModel = -14

    system = simple_sir.SimpleSIR(pop, 1, 0, beta0, 1 / gamma0,
                                  nSteps, t0=delayModel)
    system.evolveSystem()
    system.plot()
    dS = np.append(np.diff(system.timeSeries.susceptibles), 0)
    dC = -epsilon * dS
    C = np.cumsum(dC)
    system.timeSeries.confirmed = C
    plt.plot(system.timeSeries.timeVector,
             system.timeSeries.confirmed,
             label='confirmed eps=%g' % epsilon)

    deaths = cfr * system.timeSeries.recoveredWithImmunity
    plt.plot(system.timeSeries.timeVector,
             deaths, label='deaths cfr=%g' % cfr)

    plt.plot(daH, coH, '.-', label='confirmed Hubei')
    plt.plot(daH, deH, '.-', label='deaths Hubei')
    plt.plot(daI, coI, '.-', label='confirmed Italy')
    plt.plot(daI, deI, '.-', label='deaths Italy')
#    plt.plot(daK, coK, '.-', label='confirmed Korea')
#    plt.plot(daK, deK, '.-', label='deaths Korea')
    plt.ylim(1,)
    plt.xlim(10, 75)
    plt.xlabel(strdates)
    plt.legend()

    alpha = cfr * system._gamma
    ncdpi = (system._beta - system._gamma)
    tauRI = -np.log(system.basicReproductionNumber - 1) / ncdpi
    tauMI = np.log(alpha / (system._beta - system._gamma)) / ncdpi
    tauMR = np.log(alpha / system._gamma) / ncdpi
    tauCI = np.log(system._beta * epsilon / ncdpi) / ncdpi
    tauCM = tauCI - tauMI
    
