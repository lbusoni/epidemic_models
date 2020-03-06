
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
    def infectives(self):
        return self._I

    @property
    def recoveredWithImmunity(self):
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
        self._IHist = np.append(self._IHist, population.infectives)
        self._RHist = np.append(self._RHist, population.recoveredWithImmunity)

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
    def totalPopulation(self):
        return self._SHist + self._IHist + self._RHist

    @property
    def timeVector(self):
        return self._timeHist

    @property
    def justInfected(self):
        return np.append(0, np.diff(self.recoveredWithImmunity))


class SimpleSIR(object):

    def __init__(self, susceptibles=90, infectives=10, immunes=0,
                 contact_rate=0.3, average_infection_period=10,
                 nSteps=100.):
        self._population = Population(susceptibles, infectives, immunes)
        self._beta = contact_rate
        self._gamma = 1.0 / average_infection_period

        self._dt = 1
        self._nSteps = nSteps

        self._timeSeries = PopulationTimeSeries()

    def currentPopulation(self):
        return self._population

    def contactRate(self):
        return self._beta

    def averageInfectiousPeriod(self):
        return 1. / self._gamma

    def totalPopulation(self):
        return self._N

    def basicReproductionNumber(self):
        return self._beta / self._gamma

    def forceOfInfection(self):
        return self._beta * self._timeSeries.infectives / \
                self._timeSeries.totalPopulation

    def _singleStep(self):
        cp = self.currentPopulation()
        dt = self._dt
        dS = -self._beta * cp.susceptibles * cp.infectives / cp.totalPopulation
        dI = self._beta * cp.susceptibles * cp.infectives / cp.totalPopulation - \
            self._gamma * cp.infectives
        dR = self._gamma * cp.infectives
        S = np.clip(cp.susceptibles + dS * dt, 0, cp.totalPopulation)
        self._population = Population(S,
                                     cp.infectives + dI * dt,
                                     cp.recoveredWithImmunity + dR * dt)

    def evolveSystem(self):
        for i in np.arange(self._nSteps):
            self._timeSeries.append(self.currentPopulation(), self._dt * i)
            self._singleStep()

    def plot(self):
        ts = self._timeSeries
        plt.figure()
        plt.plot(ts.timeVector, ts.susceptibles, label='Susceptibles')
        plt.plot(ts.timeVector, ts.infectives, label='Infectives')
        plt.plot(ts.timeVector, ts.recoveredWithImmunity, label='Recovered with Immunity')
        # plt.plot(ts.timeVector, ts.justInfected, label='Just Infected')
        plt.plot(ts.timeVector, self.forceOfInfection(), label='Force of Infection')
        t = "Contact rate %g - Infective period %g\nInfective peak %g" % (
            self.contactRate(), self.averageInfectiousPeriod(),
            ts.infectives.max())
        plt.title(t)
        plt.legend()
        plt.grid(True)
        plt.show()


def main(susceptibles=90, infectives=10, immunes=0,
         contact_rate=0.3, average_infection_period=10,
         nSteps=100.):
    system = SimpleSIR(susceptibles, infectives, immunes,
                       contact_rate, average_infection_period,
                       nSteps)
    system.evolveSystem()
    system.plot()
