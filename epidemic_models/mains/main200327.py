from epidemic_models import seirah
import matplotlib.pyplot as plt
import numpy as np
from epidemic_models.restore_data import CSSECovid, DpcCovid, diff_from_zero
from epidemic_models.utils import piecewise
from datetime import datetime


def plotModelloLombardia():
    strdates = 'Days from Jan1'

    csse = CSSECovid()
    deH, coH, daH = csse.hubei()
    dL = DpcCovid(DpcCovid.LOMBARDIA)
    deL = dL.deceduti
    coL = dL.totale_casi
    daL = dL.days

    nSteps = 100
    delayModel = 0
    periods = np.array([65])

    E0 = 0
    I0 = .00025
    R0 = 0
    A0 = I0 * 10
    H0 = 0
    S0 = 10000000 - E0 - I0 - R0 - A0 - H0
    beta = piecewise(periods, (1.75, 0.65), nSteps)
    r = 1
    De = 5.2
    Di = 2.3
    Dq = piecewise(periods, (10, 10), nSteps)
    Dh = 30
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
    plt.plot(system3.timeSeries.timeVector,
             system3.timeSeries.susceptibles[0] - system3.timeSeries.susceptibles,
             color='C7', label='total cases')
    plt.plot(system3.timeSeries.timeVector,
             system3.timeSeries.recovered_with_immunity * 0.005,
             '--', color='C4', label='deaths')

    plt.plot(dL.days, dL.deceduti, '+-', color='C4', label='deceduti')
#    plt.plot(dL.days, dL.dimessi_guariti, 'x-', color='C4', label='dimessi')
#    plt.plot(dL.days, dL.dimessi_guariti + dL.deceduti, '.-', color='C4', label='dimessi o deceduti')
    plt.plot(dL.days, dL.totale_attualmente_positivi, '.-', color='C6',
             label='att. positivi')
    plt.plot(dL.days, dL.totale_casi, '.-', color='C7', label='totale casi')
    plt.plot([], [], ' ', label=dataAtToday())
    plt.ylim(10, 10e6)
    plt.xlim(40, 100)
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
    
