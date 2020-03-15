
# Data repositories 

The package uses data from 
1. https://github.com/CSSEGISandData/COVID-19  - worldwide by state
2. https://github.com/pcm-dpc/COVID-19  - details Italy

Data are not included here; they must be downloaded from github and
 are typically updated every day.

## CSSE repo

In folder epidemic_models/data/csse:

```
git clone https://github.com/CSSEGISandData/COVID-19
```

This package uses timeseries from folder csse_covid_19_data/csse_covid_19_time_series

## PCM DPC repo

In folder epidemic_models/data/pcm-dpc:

```
git clone https://github.com/pcm-dpc/COVID-19
```

This package uses data from dati-regioni/dpc-covid19-ita-regioni.csv
and from dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv


## Daily Update

You must manually update the repositories to pull new data. 
Go in the folders and use  `git pull`
