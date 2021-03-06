
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from cpyment.cmodel import CModel


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
    def infectious(self):
        return self._I

    @property
    def recovered_with_immunity(self):
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
        self._IHist = np.append(self._IHist, population.infectious)
        self._RHist = np.append(self._RHist, population.recovered_with_immunity)
        self._CHist = np.append(self._CHist, population.confirmed)
        self._DHist = np.append(self._DHist, population.deaths)

    def add(self, time, susceptibles, infectious,
            recovered, confirmed, deaths):
        self._timeHist = time
        self._SHist = susceptibles
        self._IHist = infectious
        self._RHist = recovered
        self._CHist = confirmed
        self._DHist = deaths

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
        return np.append(0, np.diff(self.recovered_with_immunity))


class SIRCD(object):
    '''
    SIR Model with the addition of two observable populations: confirmed and deaths

    N = S + I + R
    dS = -beta S I / N
    dC = -epsilon dS
    dI = dS - gamma I
    dR = gamma I
    dD = delta dR

    Note: in this approach, Deaths are a subset of RecoveredWithImmunity 
    altough it sounds weird.
    It's just a way of correlating an observable (total deaths) with
    the R of SIR through a known proportional factor delta.
    '''

    def __init__(self, susceptibles=90, infectious=10, immunes=0,
                 confirmed=0, deaths=0,
                 contact_rate=0.3, average_infection_period=10,
                 nSteps=100, t0=0, epsilon=.1, delta=.001):
        self._nSteps = int(nSteps)
        self._population = Population(
            susceptibles, infectious, immunes, confirmed, deaths)

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
        return self._beta * self._timeSeries.infectious / \
            self._timeSeries.totalPopulation

    @property
    def exponentialTimeConstant(self):
        return 1 / (self._beta - self._gamma)

    @property
    def tau(self):
        return 1 / (self._beta - self._gamma)

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

    def evolveSystem(self):
        t_start = 0
        t_end = self._nSteps
        t_inc = self._dt
        initial_values = (self._population.susceptibles,
                          self._population.infectious,
                          self._population.recovered_with_immunity,
                          self._population.confirmed,
                          self._population.deaths)
        t_range = np.arange(t_start, t_end + t_inc, t_inc)
        t_span = (t_start, t_end)
        res = integrate.solve_ivp(
            self._diff_eqs, t_span, initial_values, t_eval=t_range)
        assert res.success is True
        self._timeSeries.add(res.t, res.y[0], res.y[1], res.y[2],
                             res.y[3], res.y[4])

    def _diff_eqs(self, t, values):
        Y = np.zeros((5))  # (S,I,R,C,D)
        V = values
        tV = np.clip(int(t), 0, self._nSteps - 1)
        N = self._population.totalPopulation
        dS = -self._beta[tV] * V[0] * V[1] / N
        dR = self._gamma[tV] * V[1]

        Y[0] = dS
        Y[1] = -dS - dR
        Y[2] = dR
        Y[3] = -self._epsilon[tV] * dS
        Y[4] = self._delta[tV] * dR
        return Y

    def plot(self, susceptibles=True, infectious=True, recovered=True,
             confirmed=True, deaths=True, newFigure=True):

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
            ts.infectious.max())
        plt.title(t)
        plt.legend()
        plt.grid(True)
        plt.show()
        plt.semilogy()


class SIRCD_new(SIRCD):

    '''
    SIR Model with the addition of two observable populations: confirmed and deaths

    N = S + I + R
    dS = -beta S I / N
    dC = -epsilon dS
    dI = dS - gamma I
    dR = gamma I
    dD = delta dR

    Note: in this approach, Deaths are a subset of RecoveredWithImmunity 
    altough it sounds weird.
    It's just a way of correlating an observable (total deaths) with
    the R of SIR through a known proportional factor delta.
    '''

    def __init__(self, susceptibles=90, infectious=10, immunes=0,
                 confirmed=0, deaths=0,
                 contact_rate=0.3, average_infection_period=10,
                 nSteps=100, t0=0, epsilon=.1, delta=.001):

        self._nSteps = int(nSteps)
        self._population = Population(
            susceptibles, infectious, immunes, confirmed, deaths)

        self._beta = self._scalarArgs2Vectors(contact_rate)
        self._gamma = self._scalarArgs2Vectors(
            1 / average_infection_period)
        self._epsilon = self._scalarArgs2Vectors(epsilon)
        self._delta = self._scalarArgs2Vectors(delta)

        self._dt = 1
        self._nSubSteps = 10
        self._t0 = t0

        self._timeSeries = PopulationTimeSeries()

        # Now add the couplings
        self._model = CModel('SIRCD')
        self._model.set_coupling_rate('S*I:S=>I', self._beta[0], name='beta')  # Infection rate
        self._model.set_coupling_rate('S*I:=>C', self._beta[0] * self._epsilon[0], name='epsilon_beta')  # Confirmed rate
        self._model.set_coupling_rate('I:I=>R', self._gamma[0], name='gamma')  # Recovery rate
        self._model.set_coupling_rate('I:=>D', self._gamma[0] * self._delta[0], name='gamma')  # Recovery rate

    def evolveSystem(self):
        t_start = 0
        t_end = self._nSteps
        t_inc = self._dt
        N = self._population.totalPopulation
        initial_values = (self._population.susceptibles / N,
                          self._population.infectious / N,
                          self._population.recovered_with_immunity / N,
                          self._population.confirmed / N,
                          self._population.deaths / N)
        t_range = np.arange(t_start, t_end + t_inc, t_inc)
#        t_span = (t_start, t_end)
#        res = integrate.solve_ivp(
#           self._diff_eqs, t_span, initial_values, t_eval=t_range)
#        assert res.success is True
#        self._timeSeries.add(res.t, res.y[0], res.y[1], res.y[2],
#                             res.y[3], res.y[4])

        res = self._model.integrate(t_range, initial_values)
        self._timeSeries.add(t_range, res[:, 0] * N, res[:, 1] * N,
                             res[:, 2] * N, res[:, 3] * N, res[:, 4] * N)


def main(susceptibles=99.9, infectious=.1, immunes=0,
         confirmed=0, deaths=0,
         contact_rate=0.3, average_infection_period=10,
         nSteps=100, epsilon=0.1, delta=0.001):
    systemo = SIRCD(susceptibles, infectious, immunes, confirmed, deaths,
                    contact_rate, average_infection_period,
                    nSteps, epsilon, delta)
    systemo.evolveSystem()
    systemo.plot()

    system = SIRCD_new(susceptibles, infectious, immunes, confirmed, deaths,
                       contact_rate, average_infection_period,
                       nSteps, epsilon, delta)
    system.evolveSystem()
    system.plot()

    return system
