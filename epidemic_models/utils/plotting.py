
import matplotlib.pyplot as plt
from epidemic_models.utils.exponential_fitting import doubling_time, \
    daily_increment
from epidemic_models.dpc_covid import DpcCovid


def _parse(who, what, split=False, per_inhabitant=False,
           use_doubling_time=False, use_daily_increment=False,
           ):
    if not isinstance(who, list):
        who = [who, ]
    if split:
        region_data = [DpcCovid(w) for w in who]
        labelRegion = who
    else:
        region_data = [DpcCovid(who), ]
        labelRegion = [region_data[0].denominazione_regione, ]

    if use_doubling_time:
        vv = [doubling_time(d, what) for d in region_data]
        days = [v[0] for v in vv]
        data = [v[1] for v in vv]
    elif use_daily_increment:
        vv = [daily_increment(d, what) for d in region_data]
        days = [v[0] for v in vv]
        data = [v[1] for v in vv]
    else:
        data = [d.select(what) for d in region_data]
        days = [d.days for d in region_data]

    if per_inhabitant:
        data = [d / r.popolazione.residenti for d, r in zip(data, region_data)]

    return days, data, labelRegion, what


def plotRegione(who, what, split=False,
                per_inhabitant=False,
                use_doubling_time=False,
                use_daily_increment=False):

    days, data, labelRegion, what = _parse(
        who, what, split, per_inhabitant,
        use_doubling_time, use_daily_increment)

    for t, d, w in zip(days, data, labelRegion):
        plt.plot(t, d, label='%s %s' % (what, w))
    plt.legend()
    plt.xlabel("Days since 1-1-20")
    plt.grid(True)


def plotRegioniVs(who, whatX, whatY, split=False,
                  use_doubling_time=False,
                  use_daily_increment=False):
    days, dataX, labelRegion, whatX = _parse(
        who, whatX, split, use_doubling_time, use_daily_increment)
    days, dataY, labelRegion, whatY = _parse(
        who, whatY, split, use_doubling_time, use_daily_increment)

    for dX, dY, w in zip(dataX, dataY, labelRegion):
        plt.plot(dX, dY, label='%s' % (w))
    plt.legend()
    plt.xlabel(whatX)
    plt.ylabel(whatY)
    plt.grid(True)
