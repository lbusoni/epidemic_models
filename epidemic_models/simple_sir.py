
import numpy as np
import matplotlib.pyplot as plt


class Population(object):

    def __init__(self, S, I, R):
        self._S = S
        self._I = I
        self._R = R
        pass

    @property
    def susceptibles(self):
        return self._S

    @property
    def infectious(self):
        return self._I

    @property
    def recovered_with_immunity(self):
        return self._R

    @property
    def totalPopulation(self):
        return self._S + self._I + self._R


class PopulationTimeSeries():

    def __init__(self):
        self._timeHist = np.array([])
        self._SHist = np.array([])
        self._IHist = np.array([])
        self._RHist = np.array([])

    def append(self, population, time):
        self._timeHist = np.append(self._timeHist, time)
        self._SHist = np.append(self._SHist, population.susceptibles)
        self._IHist = np.append(self._IHist, population.infectious)
        self._RHist = np.append(self._RHist, population.recovered_with_immunity)

    @property
    def susceptibles(self):
        return self._SHist

    @property
    def infectious(self):
        return self._IHist

    @property
    def recovered_with_immunity(self):
        return self._RHist

    @property
    def totalPopulation(self):
        return self._SHist + self._IHist + self._RHist

    @property
    def timeVector(self):
        return self._timeHist

    @property
    def justInfected(self):
        return np.append(0, np.diff(self.recovered_with_immunity))


class SimpleSIR(object):

    def __init__(self, susceptibles=90, infectious=10, immunes=0,
                 contact_rate=0.3, average_infection_period=10,
                 nSteps=100., t0=0):
        self._nSteps = nSteps
        self._population = Population(susceptibles, infectious, immunes)
        if np.isscalar(contact_rate):
            self._beta = np.ones(self._nSteps) * contact_rate
        else:
            assert len(contact_rate) == nSteps
            self._beta = contact_rate
        if np.isscalar(average_infection_period):
            self._gamma = np.ones(self._nSteps) / average_infection_period
        else:
            assert len(average_infection_period) == nSteps
            self._gamma = 1. / average_infection_period

        self._dt = 1
        self._nSubSteps = 10
        self._t0 = t0

        self._timeSeries = PopulationTimeSeries()

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
        return self._beta * self._timeSeries.infectious / \
            self._timeSeries.totalPopulation

    @property
    def exponentialTimeConstant(self):
        return 1 / (self._beta - self._gamma)

    @property
    def delayRecoveredInfected(self):
        return -np.log(self.basicReproductionNumber - 1) * \
            self.exponentialTimeConstant

    def timeToIncreaseByFactor(self, factor):
        return self.exponentialTimeConstant * np.log(factor)

    def _singleStep(self, step):
        cp = self.currentPopulation
        Su = cp.susceptibles
        In = cp.infectious
        Re = cp.recovered_with_immunity
        Nu = cp.totalPopulation
        dt = self._dt / self._nSubSteps
        for _ in np.arange(self._nSubSteps):
            dS = -self._beta[step] * Su * In / Nu
            dI = -dS - self._gamma[step] * In
            dR = self._gamma[step] * In
            Su = Su + dS * dt
            In = In + dI * dt
            Re = Re + dR * dt
        self._population = Population(np.clip(Su, 0, Nu),
                                      In, Re)

    def evolveSystem(self):
        for i in np.arange(self._nSteps):
            self._timeSeries.append(self.currentPopulation,
                                    self._dt * i + self._t0)
            self._singleStep(i)

    def plot(self, susceptibles=True, infectious=True, recovered=True,
             newFigure=True):

        ts = self._timeSeries
        if newFigure:
            plt.figure()
        if susceptibles:
            plt.plot(ts.timeVector, ts.susceptibles, label='Susceptibles')
        if infectious:
            plt.plot(ts.timeVector, ts.infectious, label='Infectives')
        if recovered:
            plt.plot(ts.timeVector,
                     ts.recovered_with_immunity,
                     label='Recovered with Immunity')
        # plt.plot(ts.timeVector, ts.justInfected, label='Just Infected')
        # plt.plot(ts.timeVector, self.forceOfInfection(), label='Force of Infection')
        t = "Contact rate (%g, %g) - Infective period (%g, %g)\nInfective peak %g" % (
            self.contactRate.min(), self.contactRate.max(),
            self.averageInfectiousPeriod.min(),
            self.averageInfectiousPeriod.max(),
            ts.infectious.max())
        plt.title(t)
        plt.legend()
        plt.grid(True)
        plt.show()
        plt.semilogy()


def main(susceptibles=90, infectious=10, immunes=0,
         contact_rate=0.3, average_infection_period=10,
         nSteps=100.):
    system = SimpleSIR(susceptibles, infectious, immunes,
                       contact_rate, average_infection_period,
                       nSteps)
    system.evolveSystem()
    system.plot()
