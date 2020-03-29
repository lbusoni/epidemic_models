from epidemic_models import sircd, seirah

import matplotlib.pyplot as plt
import numpy as np
from epidemic_models.restore_data import CSSECovid, DpcCovid, diff_from_zero
from epidemic_models.utils import piecewise
from datetime import datetime


def plotModelloLombardia():
    strdates = 'Days from Jan1'

    csse = CSSECovid()
    deH, coH, daH = csse.restoreHubei()
    dpc = DpcCovid(DpcCovid.LOMBARDIA)
    deL = dpc.deceduti
    coL = dpc.totale_casi
    daL = dpc.days

    nSteps = 100
    delayModel = 0
    periods = np.array([65])

    E0 = 0
    I0 = .01
    R0 = 0
    A0 = I0 * 10
    H0 = 0
    S0 = 10000000 - E0 - I0 - R0 - A0 - H0
    beta = piecewise(periods, (1.75, 0.15), nSteps)
    r = piecewise(periods, (0.19, 0.17), nSteps)
    De = 5.2
    Di = 2.3
    Dh = 30
    Dq = piecewise(periods, (10, 10), nSteps)
    travellers = 0

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

    plt.plot(daL, deL, '.-',
             linewidth=2,
             markersize=12,
             color='C4',
             label='deaths Italy')
    plt.plot(daL, coL, 'x-', color='C4', label='confirmed Italy')
    plt.plot([], [], ' ', label="data at 27 Mar 2020")
    plt.ylim(10, 1e6)
    plt.xlim(0, 100)
    plt.xlabel(strdates)
    plt.title('')
    plt.legend()


def dataAtToday():
    now = datetime.now()
    return now.strftime("data at %m/%d/%Y")


def plotDatiDpc(who=DpcCovid.ALL):
    dI = DpcCovid(who)

    plt.figure()
    plt.plot(dI.data, dI.deceduti, '.-', label='deceduti')
    plt.plot(dI.data, dI.dimessi_guariti, '.-', label='dimessi_guariti')
    plt.plot(dI.data, dI.totale_casi, '.-', label='totale_casi')
    plt.plot(dI.data, dI.tamponi, '.-', label='tamponi')
    plt.plot([], [], ' ', label=dataAtToday())
    plt.semilogy()
    plt.legend()
    plt.grid()

    plt.figure()
    plt.plot(dI.data, dI.isolamento_domiciliare, '.-', label='isolamento domiciliare')
    plt.plot(dI.data, dI.ricoverati_con_sintomi, '.-', label='ricoverati con sintomi')
    plt.plot(dI.data, dI.terapia_intensiva, '.-', label='terapia intensiva')
    plt.plot([], [], ' ', label=dataAtToday())
    plt.semilogy()
    plt.legend()
    plt.grid()

    plt.figure()
    plt.plot(dI.data, dI.nuovi_contagiati, '.-', label='nuovi contagiati')
    plt.plot(dI.data, dI.nuovi_deceduti, '.-', label='nuovi deceduti')
    plt.plot(dI.data, dI.nuovi_dimessi_guariti, '.-', label='nuovi dimessi')
    plt.plot([], [], ' ', label=dataAtToday())
    plt.semilogy()
    plt.legend()
    plt.grid()


def plotTerapieIntensive():
    dI = DpcCovid(DpcCovid.ALL)
    dL = DpcCovid(DpcCovid.LOMBARDIA)
    dT = DpcCovid(DpcCovid.TOSCANA)
    dV = DpcCovid(DpcCovid.VENETO)

    plt.figure()
    plt.plot(dL.data, dL.terapia_intensiva / dL.totale_attualmente_positivi, 'x-', color='C2', label='ICU/positivi Lombardia')
    plt.plot(dV.data, dV.terapia_intensiva / dV.totale_attualmente_positivi, 'x-', color='C3', label='ICU/positivi Veneto')
    plt.plot(dT.data, dT.terapia_intensiva / dT.totale_attualmente_positivi, 'x-', color='C4', label='ICU/positivi Toscana')

    plt.plot(dL.data, dL.nuovi_deceduti / dL.terapia_intensiva, '.-', color='C2', label='morti/ICU Lombardia')
    plt.plot(dV.data, dV.nuovi_deceduti / dV.terapia_intensiva, '.-', color='C3', label='morti/ICU Veneto')
    plt.plot(dT.data, dT.nuovi_deceduti / dT.terapia_intensiva, '.-', color='C4', label='morti/ICU Toscana')

    plt.plot([], [], ' ', label="data at 27 Mar 2020")
    plt.legend()
    plt.grid()


def doublingTimeVsR():
    R = np.linspace(0, 4, 101)
    gamma = 0.13
    t2 = np.log(2) / (gamma * (R - 1))
    plt.figure()
    plt.plot(R, t2, '-')
    plt.plot([], [], ' ', label=r'$\tau=\frac{\log(2)}{\gamma (R-1)}$' + '\n' + r'$\gamma=%g$' % gamma)
    plt.xlabel(r'Effective Reproduction Number R')
    plt.ylabel(r'Infectious doubling time (halving, if negative) $ \tau $ [days]')
    plt.legend()
    plt.grid()
    plt.ylim(-20, 20)
    
