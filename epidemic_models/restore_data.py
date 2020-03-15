
from epidemic_models.utils.package_data import dataRootDir
import os
import numpy as np
import pandas as pd
import csv
import datetime


class CCSECovidTimeSeries():

    def __init__(self, key, state, country, lat, long, values, dates):
        self.state = state
        self.country = country
        self.latitude = lat
        self.longitude = long
        self.values = values
        self.dates = dates
        self.key = key

    @property
    def days(self):
        jan1 = datetime.datetime(2020, 1, 1, 0, 0)
        return np.array([(k - jan1).days for k in self.dates])

    @staticmethod
    def from_csv(row, headers):
        key = row[0] + '/' + row[1] if row[0] != '' else row[1]
        dates = np.array([datetime.datetime.strptime(h, '%m/%d/%y')
                          for h in headers[4:]])
        dd = CCSECovidTimeSeries(
            key, str(row[0]), str(row[1]),
            float(row[2]), float(row[3]),
            np.array(row[4:]).astype(float), dates)
        return dd


def _restoreGenericCSSE(filename):
    with open(filename, newline='') as csvfile:
        rd = csv.reader(csvfile, delimiter=',')
        headers = next(rd, None)
        d = {}
        for row in rd:
            ts = CCSECovidTimeSeries.from_csv(row, headers)
            d[ts.key] = ts
    return d


def restoreCSSEDeath():

    rootDir = dataRootDir()
    filename = os.path.join(rootDir,
                            'csse',
                            'COVID-19',
                            'csse_covid_19_data',
                            'csse_covid_19_time_series',
                            'time_series_19-covid-Deaths.csv')
    return _restoreGenericCSSE(filename)


def restoreCSSEConfirmed():

    rootDir = dataRootDir()
    filename = os.path.join(rootDir,
                            'csse',
                            'COVID-19',
                            'csse_covid_19_data',
                            'csse_covid_19_time_series',
                            'time_series_19-covid-Confirmed.csv')
    return _restoreGenericCSSE(filename)


def restoreCSSERecovered():

    rootDir = dataRootDir()
    filename = os.path.join(rootDir,
                            'csse',
                            'COVID-19',
                            'csse_covid_19_data',
                            'csse_covid_19_time_series',
                            'time_series_19-covid-Recovered.csv')
    return _restoreGenericCSSE(filename)


class CSSECovid():
    DELAY_ITALY = 36
    DELAY_IRAN = 34
    DELAY_HUBEI = 0
    DELAY_FRANCE = 45
    DELAY_SPAIN = 45
    DELAY_SOUTH_KOREA = 35
    DELAY_NETHERLANDS = 50

    def __init__(self):
        self._de = restoreCSSEDeath()
        self._co = restoreCSSEConfirmed()
        self._re = restoreCSSERecovered()

    def string_dates(self):
        return 'Days [hub (Jan1), it(+36), fr(+45), es(45), ne(50)]'

    def restoreCSSECountry(self, name, delay_date=0):
        assert np.array_equal(self._de[name].days, self._co[name].days)
        assert np.array_equal(self._de[name].days, self._re[name].days)
        deaths = self._de[name].values
        confirmed = self._co[name].values
        recovered = self._re[name].values
        days = self._de[name].days - delay_date
        return deaths, confirmed, recovered, days

    def restoreItaly(self):
        de, co, re, da = self.restoreCSSECountry('Italy', self.DELAY_ITALY)
        de[50] = 1016
        co[50] = 15113
        re[50] = 1258
        return de, co, re, da

    def restoreHubei(self):
        return self.restoreCSSECountry('Hubei/China', self.DELAY_HUBEI)

    def restoreFrance(self):
        return self.restoreCSSECountry('France/France', self.DELAY_FRANCE)

    def restoreSpain(self):
        return self.restoreCSSECountry('Spain', self.DELAY_SPAIN)

    def restoreNetherlands(self):
        return self.restoreCSSECountry('Netherlands',
                                       self.DELAY_NETHERLANDS)


class DpcCovid():
    DENOMINAZIONE_REGIONE = 'denominazione_regione'
    CODICE_REGIONE = 'codice_regione'
    STATO = 'stato'
    LATITUDINE = 'lat'
    LONGITUDINE = 'long'
    DATA = 'data'
    RICOVERATI_CON_SINTOMI = 'ricoverati_con_sintomi'
    TERAPIA_INTENSIVA = 'terapia_intensiva'
    TOTALE_OSPEDALIZZATI = 'totale_ospedalizzati'
    ISOLAMENTO_DOMICILIARE = 'isolamento_domiciliare'
    TOTALE_ATTUALMENTE_POSITIVI = 'totale_attualmente_positivi'
    NUOVI_ATTUALEMENTE_POSITIVI = 'nuovi_attualemente_positivi'
    DIMESSI_GUARITI = 'dimessi_guariti'
    DECEDUTI = 'deceduti'
    TOTALE_CASI = 'totale_casi'
    TAMPONI = 'tamponi'

    ABRUZZO = 'Abruzzo'
    BASILICATA = 'Basilicata'
    PROVINCIA_AUTONOMA_DI_BOLZANO = "P.A. Bolzano"
    CALABRIA = "Calabria"
    CAMPANIA = "Campania"
    EMILIA_ROMAGNA = "Emilia Romagna"
    FRIULI_VENEZIA_GIULIA = "Friuli Venezia Giulia"
    LAZIO = "Lazio"
    LIGURIA = "Liguria"
    LOMBARDIA = "Lombardia"
    MARCHE = "Marche"
    MOLISE = "Molise"
    PIEMONTE = "Piemonte"
    PUGLIA = "Puglia"
    SARDEGNA = "Sardegna"
    SICILIA = "Sicilia"
    TOSCANA = "Toscana"
    PROVINCIA_AUTONOMA_DI_TRENTO = "P.A. Trento"
    UMBRIA = "Umbria"
    VALLE_DI_AOSTA = "Valle d'Aosta"
    VENETO = "Veneto"
    ITALIA = "Italia"

    def __init__(self, denominazione_regione):
        if denominazione_regione == self.ITALIA:
            self._data = self.load_csv_italia()
        else:
            self._all = self.load_csv_regioni()
            self._filter = \
                self._all['denominazione_regione'] == denominazione_regione
            self._data = self._all[self._filter]

    def stato(self):
        return self._filteredData(self.STATO)

    @property
    def codice_regione(self):
        return self._filteredData(self.CODICE_REGIONE)

    @property
    def denominazione_regione(self):
        return self._filteredData(self.DENOMINAZIONE_REGIONE)

    @property
    def latitudine(self):
        return self._filteredData(self.LATITUDINE)

    @property
    def longitudine(self):
        return self._filteredData(self.LONGITUDINE)

    @property
    def data(self):
        dd = self._filteredData(self.DATA)
        return np.array([datetime.datetime.strptime(
            d, '%Y-%m-%d %H:%M:%S') for d in dd])

    @property
    def ricoverati_con_sintomi(self):
        return self._filteredData(self.RICOVERATI_CON_SINTOMI)

    @property
    def terapia_intensiva(self):
        return self._filteredData(self.TERAPIA_INTENSIVA)

    @property
    def totale_ospedalizzati(self):
        return self._filteredData(self.TOTALE_OSPEDALIZZATI)

    @property
    def isolamento_domiciliare(self):
        return self._filteredData(self.ISOLAMENTO_DOMICILIARE)

    @property
    def totale_attualmente_positivi(self):
        return self._filteredData(self.TOTALE_ATTUALMENTE_POSITIVI)

    @property
    def nuovi_attualmente_positivi(self):
        return self._filteredData(self.TOTALE_ATTUALMENTE_POSITIVI)

    @property
    def dimessi_guariti(self):
        return self._filteredData(self.DIMESSI_GUARITI)

    @property
    def deceduti(self):
        return self._filteredData(self.DECEDUTI)

    @property
    def totale_casi(self):
        return self._filteredData(self.TOTALE_CASI)

    @property
    def tamponi(self):
        return self._filteredData(self.TAMPONI)

    def _filteredData(self, what):
        return self._data[what].values

    @property
    def days(self):
        jan1 = datetime.datetime(2020, 1, 1, 0, 0)
        return np.array([(k - jan1).days for k in self.data])

    def load_csv_regioni(self):
        rootDir = dataRootDir()
        filename = os.path.join(rootDir,
                                'pcm-dpc',
                                'COVID-19',
                                'dati-regioni',
                                'dpc-covid19-ita-regioni.csv')
        return pd.read_csv(filename)

    def load_csv_italia(self):
        rootDir = dataRootDir()
        filename = os.path.join(rootDir,
                                'pcm-dpc',
                                'COVID-19',
                                'dati-andamento-nazionale',
                                'dpc-covid19-ita-andamento-nazionale.csv')
        return pd.read_csv(filename)
