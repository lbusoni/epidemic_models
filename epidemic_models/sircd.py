
import numpy as np
import matplotlib.pyplot as plt


class Population(object):

    def __init__(self, S, I, R, C, D):
        self._S = S
        self._I = I
        self._R = R
        self._C = C
        self._D = D
        pass

    @property
    def susceptibles(self):
        return self._S

    @property
    def infectives(self):
        return self._I

    @property
    def recoveredWithImmunity(self):
        return self._R

    @property
    def confirmed(self):
        return self._C

    @property
    def deaths(self):
        return self._D

    @property
    def totalPopulation(self):
        return self._S + self._I + self._R + self._D


class PopulationTimeSeries():

    def __init__(self):
        self._timeHist = np.array([])
        self._SHist = np.array([])
        self._IHist = np.array([])
        self._RHist = np.array([])
        self._CHist = np.array([])
        self._DHist = np.array([])

    def append(self, population, time):
        self._timeHist = np.append(self._timeHist, time)
        self._SHist = np.append(self._SHist, population.susceptibles)
        self._IHist = np.append(self._IHist, population.infectives)
        self._RHist = np.append(self._RHist, population.recoveredWithImmunity)
        self._CHist = np.append(self._CHist, population.confirmed)
        self._DHist = np.append(self._DHist, population.deaths)

    @property
    def susceptibles(self):
        return self._SHist

    @property
    def infectives(self):
        return self._IHist

    @property
    def recoveredWithImmunity(self):
        return self._RHist

    @property
    def confirmed(self):
        return self._CHist

    @property
    def deaths(self):
        return self._DHist

    @property
    def totalPopulation(self):
        return self._SHist + self._IHist + self._RHist

    @property
    def timeVector(self):
        return self._timeHist

    @property
    def justInfected(self):
        return np.append(0, np.diff(self.recoveredWithImmunity))


class SIRCD(object):
    '''
    SIR Model with the addition of two observable populations: confirmed and deaths

    N = S + I + R
    dS = -beta S I / N
    dC = epsilon dS
    dI = dS - gamma I
    dR = gamma I
    dD = delta dR

    Note: in this approach, Deaths are a subset of RecoveredWithImmunity 
    altough it sounds weird.
    It's just a way of correlating an observable (total deaths) with
    the R of SIR through a known proportional factor delta.
    '''

    def __init__(self, susceptibles=90, infectives=10, immunes=0,
                 confirmed=0, deaths=0,
                 contact_rate=0.3, average_infection_period=10,
                 nSteps=100, t0=0, epsilon=.1, delta=.001):
        self._nSteps = int(nSteps)
        self._population = Population(
            susceptibles, infectives, immunes, confirmed, deaths)

        self._beta = self._scalarArgs2Vectors(contact_rate)
        self._gamma = self._scalarArgs2Vectors(
            1 / average_infection_period)
        self._epsilon = self._scalarArgs2Vectors(epsilon)
        self._delta = self._scalarArgs2Vectors(delta)

        self._dt = 1
        self._nSubSteps = 10
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
        return self._beta / self._gamma

    @property
    def R0(self):
        return self.basicReproductionNumber

    @property
    def forceOfInfection(self):
        return self._beta * self._timeSeries.infectives / \
            self._timeSeries.totalPopulation

    @property
    def exponentialTimeConstant(self):
        return 1 / (self._beta - self._gamma)

    @property
    def tau(self):
        return 1 / (self._beta - self._gamma)

    @property
    def delayRecoveredInfected(self):
        return -np.log(self.basicReproductionNumber - 1) * \
            self.exponentialTimeConstant

    def timeToIncreaseByFactor(self, factor):
        return self.exponentialTimeConstant * np.log(factor)

    @property
    def caseFatalityRate(self):
        return self._delta

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

    def _singleStep(self, step):
        cp = self.currentPopulation
        Su = cp.susceptibles
        In = cp.infectives
        Re = cp.recoveredWithImmunity
        Co = cp.confirmed
        De = cp.deaths
        Nu = cp.totalPopulation
        dt = self._dt / self._nSubSteps
        for _ in np.arange(self._nSubSteps):
            dS = -self._beta[step] * Su * In / Nu
            dR = self._gamma[step] * In
            dI = -dS - dR
            dC = -self._epsilon[step] * dS
            dD = self._delta[step] * dR
            Su = Su + dS * dt
            In = In + dI * dt
            Re = Re + dR * dt
            Co = Co + dC * dt
            De = De + dD * dt
        self._population = Population(np.clip(Su, 0, Nu),
                                      In, Re, Co, De)

    def evolveSystem(self):
        for i in np.arange(self._nSteps):
            self._timeSeries.append(self.currentPopulation,
                                    self._dt * i + self._t0)
            self._singleStep(i)

    def plot(self, susceptibles=True, infectives=True, recovered=True,
             confirmed=True, deaths=True, newFigure=True):

        ts = self._timeSeries
        if newFigure:
            plt.figure()
        if susceptibles:
            plt.plot(ts.timeVector, ts.susceptibles, label='Susceptibles')
        if infectives:
            plt.plot(ts.timeVector, ts.infectives, label='Infectives')
        if recovered:
            plt.plot(ts.timeVector,
                     ts.recoveredWithImmunity,
                     label='Recovered with Immunity')
        if confirmed:
            plt.plot(ts.timeVector, ts.confirmed,
                     label='Confirmed eps=%g' % self._epsilon[0])
        if deaths:
            plt.plot(ts.timeVector, ts.deaths,
                     label='Deaths delta=%g' % self._delta[0])
        # plt.plot(ts.timeVector, ts.justInfected, label='Just Infected')
        # plt.plot(ts.timeVector, self.forceOfInfection(), label='Force of Infection')
        t = "Contact rate (%g, %g) - Infective period (%g, %g)\nInfective peak %g" % (
            self.contactRate.min(), self.contactRate.max(),
            self.averageInfectiousPeriod.min(),
            self.averageInfectiousPeriod.max(),
            ts.infectives.max())
        plt.title(t)
        plt.legend()
        plt.grid(True)
        plt.show()
        plt.semilogy()


def main(susceptibles=99.9, infectives=.1, immunes=0,
         confirmed=0, deaths=0,
         contact_rate=0.3, average_infection_period=10,
         nSteps=100, epsilon=0.1, delta=0.001):
    system = SIRCD(susceptibles, infectives, immunes, confirmed, deaths,
                   contact_rate, average_infection_period,
                   nSteps, epsilon, delta)
    system.evolveSystem()
    system.plot()
    return system
