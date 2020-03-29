
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate


class Population(object):

    def __init__(self, S, E, I, R, A, H):
        self._S = S
        self._E = E
        self._I = I
        self._R = R
        self._A = A
        self._H = H

    @property
    def susceptibles(self):
        return self._S

    @property
    def exposed(self):
        return self._E

    @property
    def infectious(self):
        return self._I

    @property
    def recovered_with_immunity(self):
        return self._R

    @property
    def hospitalized(self):
        return self._H

    @property
    def unascertained(self):
        return self._A

    @property
    def totalPopulation(self):
        return self._S + self._I + self._R + self._E + self._H + self._A


class PopulationTimeSeries():

    def __init__(self):
        self._timeHist = np.array([])
        self._SHist = np.array([])
        self._EHist = np.array([])
        self._IHist = np.array([])
        self._RHist = np.array([])
        self._AHist = np.array([])
        self._HHist = np.array([])

    def append(self, population, time):
        self._timeHist = np.append(self._timeHist, time)
        self._SHist = np.append(self._SHist, population.susceptibles)
        self._EHist = np.append(self._EHist, population.exposed)
        self._IHist = np.append(self._IHist, population.infectious)
        self._RHist = np.append(self._RHist, population.recovered_with_immunity)
        self._AHist = np.append(self._CHist, population.unascertained)
        self._HHist = np.append(self._DHist, population.hospitalized)

    def add(self, time, susceptibles, exposed, infectious,
            recovered, unascertained, hospitalized):
        self._timeHist = time
        self._SHist = susceptibles
        self._EHist = exposed
        self._IHist = infectious
        self._RHist = recovered
        self._AHist = unascertained
        self._HHist = hospitalized

    @property
    def susceptibles(self):
        return self._SHist

    @property
    def exposed(self):
        return self._EHist

    @property
    def infectious(self):
        return self._IHist

    @property
    def recovered_with_immunity(self):
        return self._RHist

    @property
    def unascertained(self):
        return self._AHist

    @property
    def hospitalized(self):
        return self._HHist

    @property
    def totalPopulation(self):
        return self._SHist + self._IHist + self._RHist

    @property
    def timeVector(self):
        return self._timeHist


class SEIRAH(object):
    '''
    SEIR Model with the addition unAscertained infectious and Hospitalized

    From "Evolving Epidemiology and Impact of Non-pharmaceutical 
    Interventions on the Outbreak of Coronavirus Disease 2019 in Wuhan, China"
    https://www.medrxiv.org/content/10.1101/2020.03.03.20030593v1


    N = S + E + I + R + A + H
    S' = -b S (I + a A) / N + n - n S / (N-I-H)
    E' = b S (I + a A) / N - E / De - n E / (N-I-H)
    I' = r E / De - I / Dq - I / Di
    A' = (1-r) E / De - A / Di - n A / (N-I-H)
    H' = I / Dq - H / Dn
    R' = (I+A) / Di + H / Dn - n R / (N-I-H)

    b: transmission rate
    a: ratio of transmission rate of unascertained / ascertained
    r: ascertainment fraction
    De: latent period
    Di: infectious period
    Dq: illness onset -> hospitalization
    Dh: hospitalizaion period
    n: inbound = outbound travelers
    '''

    def __init__(self,
                 susceptibles=90, exposed=0, infectious=10, recovered=0,
                 unascertained=0, hospitalized=0,
                 transmission_rate=0.3,
                 unscertained_transmission_rate_ratio=1,
                 ascertainment_fraction=1.0,
                 latent_period=5.2,
                 infectious_period=2.8,
                 illness_to_hospitalization_period=10,
                 hospitalization_period=30,
                 inbound_outbound_travelers=0,
                 nSteps=100, t0=0):
        self._nSteps = int(nSteps)
        self._population = Population(
            susceptibles, exposed, infectious, recovered,
            unascertained, hospitalized)

        self._beta = self._scalarArgs2Vectors(transmission_rate)
        self._alpha = self._scalarArgs2Vectors(
            unscertained_transmission_rate_ratio)
        self._r = self._scalarArgs2Vectors(ascertainment_fraction)
        self._De = self._scalarArgs2Vectors(latent_period)
        self._Di = self._scalarArgs2Vectors(infectious_period)
        self._Dq = self._scalarArgs2Vectors(illness_to_hospitalization_period)
        self._Dh = self._scalarArgs2Vectors(hospitalization_period)
        self._n = self._scalarArgs2Vectors(inbound_outbound_travelers)

        self._dt = 1
        self._t0 = t0

        self._timeSeries = PopulationTimeSeries()

    def _scalarArgs2Vectors(self, value):
        if np.isscalar(value):
            vect = np.ones(self._nSteps) * value
        else:
            assert len(value) == self._nSteps
            vect = value
        return vect

    @property
    def timeSeries(self):
        return self._timeSeries

    @property
    def currentPopulation(self):
        return self._population

    @property
    def contactRate(self):
        return self._beta

    @property
    def averageInfectiousPeriod(self):
        return 1. / self._gamma

    @property
    def totalPopulation(self):
        return self._N

    @property
    def basicReproductionNumber(self):
        pass

    @property
    def R0(self):
        return self.basicReproductionNumber

    @property
    def forceOfInfection(self):
        pass

    @property
    def exponentialTimeConstant(self):
        pass

    @property
    def tau(self):
        pass

    def timeToIncreaseByFactor(self, factor):
        return self.exponentialTimeConstant * np.log(factor)

    @property
    def caseFatalityRate(self):
        pass

    @property
    def delayDeaths(self):
        ''' In the exponential phase, delay tauDI is such that
            deaths(t+tauDI) = infected(t)
        '''
        return self.tau * np.log(self._delta * self._gamma * self.tau)

    @property
    def delayConfirmed(self):
        ''' In the exponential phase, delay tauCI is such that
            confirmed(t+tauCI) = infected(t)
        '''
        return self.tau * np.log(self._epsilon * self._beta * self.tau)

    @property
    def delayRecovered(self):
        ''' In the exponential phase, delay tauRI is such that
            recovered(t+tauRI) = infected(t)
        '''
        return self.tau * np.log(self._gamma * self.tau)

    def evolveSystem(self):
        t_start = 0
        t_end = self._nSteps
        t_inc = self._dt
        initial_values = (self._population.susceptibles,
                          self._population.exposed,
                          self._population.infectious,
                          self._population.recovered_with_immunity,
                          self._population.unascertained,
                          self._population.hospitalized)
        t_range = np.arange(t_start, t_end + t_inc, t_inc)
        t_span = (t_start, t_end)
        res = integrate.solve_ivp(
            self._diff_eqs, t_span, initial_values, t_eval=t_range)
        assert res.success is True
        self._timeSeries.add(res.t, res.y[0], res.y[1], res.y[2],
                             res.y[3], res.y[4], res.y[5])

    def _diff_eqs(self, t, values):
        Y = np.zeros((6))  # (S,E,I,R,A,H)
        S, E, I, R, A, H = values
        tV = np.clip(int(t), 0, self._nSteps - 1)
        N = self._population.totalPopulation
        dS = -self._beta[tV] * S * (I + self._alpha[tV] * A) / N
        n = self._n[tV]
        nNIH = n / (N - I - H)
        De = self._De[tV]
        Dq = self._Dq[tV]
        Di = self._Di[tV]
        Dh = self._Dh[tV]
        r = self._r[tV]

        Y[0] = dS + n - nNIH * S
        Y[1] = -dS - E / De - nNIH * E
        Y[2] = r * E / De - I / Dq - I / Di
        Y[3] = (I + A) / Di + H / Dh - nNIH * R
        Y[4] = (1 - r) * E / De - A / Di - nNIH * A
        Y[5] = I / Dq - H / Dh
        return Y

    def plot(self, susceptibles=True, exposed=True,
             infectious=True, recovered=True,
             unascertained=True, hospitalized=True, newFigure=True):

        ts = self._timeSeries
        if newFigure:
            plt.figure()
        if susceptibles:
            plt.plot(ts.timeVector, ts.susceptibles, label='Susceptibles')
        if exposed:
            plt.plot(ts.timeVector, ts.exposed, label='Exposed')
        if infectious:
            plt.plot(ts.timeVector, ts.infectious, label='Infectious')
        if recovered:
            plt.plot(ts.timeVector,
                     ts.recovered_with_immunity,
                     label='Recovered with Immunity')
        if unascertained:
            plt.plot(ts.timeVector, ts.unascertained,
                     label='Unascertained')
        if hospitalized:
            plt.plot(ts.timeVector, ts.hospitalized,
                     label='Hospitalized')
        # plt.plot(ts.timeVector, ts.justInfected, label='Just Infected')
        # plt.plot(ts.timeVector, self.forceOfInfection(), label='Force of Infection')
        plt.legend()
        plt.grid(True)
        plt.show()
        plt.semilogy()


def main(susceptibles=99.9, exposed=0, infectious=.1, recovered=0,
         unascertained=0, hospitalized=0,
         transmission_rate=0.3,
         unscertained_transmission_rate_ratio=1,
         ascertainment_fraction=1.0,
         latent_period=5.2,
         infectious_period=2.8,
         illness_to_hospitalization_period=10,
         hospitalization_period=30,
         inbound_outbound_travelers=0,
         nSteps=100):
    system = SEIRAH(susceptibles, exposed, infectious, recovered,
                    unascertained, hospitalized,
                    transmission_rate,
                    unscertained_transmission_rate_ratio,
                    ascertainment_fraction,
                    latent_period,
                    infectious_period,
                    illness_to_hospitalization_period,
                    hospitalization_period,
                    inbound_outbound_travelers,
                    nSteps)
    system.evolveSystem()
    system.plot()
    return system
