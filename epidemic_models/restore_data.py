
from epidemic_models.utils.package_data import dataRootDir
import os
import numpy as np
import pandas as pd
import csv
import datetime


def diff_from_zero(v):
    return np.diff(np.hstack(([0.], v)))


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
                            'time_series_covid19_deaths_global.csv')
    return _restoreGenericCSSE(filename)


def restoreCSSEConfirmed():

    rootDir = dataRootDir()
    filename = os.path.join(rootDir,
                            'csse',
                            'COVID-19',
                            'csse_covid_19_data',
                            'csse_covid_19_time_series',
                            'time_series_covid19_confirmed_global.csv')
    return _restoreGenericCSSE(filename)


class CSSECovid():
    DELAY_ITALY = 36
    DELAY_IRAN = 34
    DELAY_HUBEI = 0
    DELAY_FRANCE = 47
    DELAY_SPAIN = 44
    DELAY_SOUTH_KOREA = 35
    DELAY_NETHERLANDS = 52
    DELAY_UK = 51
    DELAY_GERMANY = 54
    DELAY_SWEDEN = 59
    DELAY_US = 49

    def __init__(self):
        self._de = restoreCSSEDeath()
        self._co = restoreCSSEConfirmed()

    def string_dates(self):
        return 'Days [hub (Jan1), it(+36), fr(+47), es(+43), ne(+52), uk(+51), de(+54)]'

    def restoreCSSECountry(self, name, delay_date=0):
        assert np.array_equal(self._de[name].days, self._co[name].days)
        deaths = self._de[name].values
        confirmed = self._co[name].values
        days = self._de[name].days - delay_date
        return deaths, confirmed, days

    def italy(self):
        de, co, da = self.restoreCSSECountry('Italy', self.DELAY_ITALY)
        de[50] = 1016
        co[50] = 15113
        return de, co, da

    def hubei(self):
        return self.restoreCSSECountry('Hubei/China', self.DELAY_HUBEI)

    def france(self):
        return self.restoreCSSECountry('France', self.DELAY_FRANCE)

    def spain(self):
        return self.restoreCSSECountry('Spain', self.DELAY_SPAIN)

    def netherlands(self):
        return self.restoreCSSECountry('Netherlands',
                                       self.DELAY_NETHERLANDS)

    def uk(self):
        return self.restoreCSSECountry('United Kingdom',
                                       self.DELAY_UK)

    def germany(self):
        return self.restoreCSSECountry('Germany',
                                       self.DELAY_GERMANY)

    def south_korea(self):
        return self.restoreCSSECountry('Korea, South',
                                       self.DELAY_SOUTH_KOREA)

    def sweden(self):
        return self.restoreCSSECountry('Sweden',
                                       self.DELAY_SWEDEN)

    def usa(self):
        return self.restoreCSSECountry('US',
                                       self.DELAY_US)


class DpcCovid():
    '''
    ospedalizzati = ricoverati_con_sintomi + terapia_intensiva
    totale_attualmente_positivi = ospedalizzati + isolamento_domiciliare
    nuovi_attualmente_positivi = diff(totale_attualmente_positivi)
    totale_casi = totale_attualmente_positivi + dimessi_guariti + deceduti

    Nota: nuovi_attualmente_positivi non serve a niente

    Aggiungo:
    nuovi_contagiati = diff(totale_casi) corrisponde al numero di persone
    passate da sani a positivi oggi, cioè al numero di nuove contagi
    '''

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
    TOTALE_POSITIVI = 'totale_positivi'
    DIMESSI_GUARITI = 'dimessi_guariti'
    DECEDUTI = 'deceduti'
    TOTALE_CASI = 'totale_casi'
    TAMPONI = 'tamponi'

    VARIAZIONE_RICOVERATI_CON_SINTOMI = 'variazione_ricoverati_con_sintomi'
    VARIAZIONE_TERAPIA_INTENSIVA = 'variazione_terapia_intensiva'
    VARIAZIONE_TOTALE_OSPEDALIZZATI = 'variazione_totale_ospedalizzati'
    VARIAZIONE_ISOLAMENTO_DOMICILIARE = 'variazione_isolamento_domiciliare'
    VARIAZIONE_TOTALE_POSITIVI = 'variazione_totale_positivi'
    NUOVI_DIMESSI_GUARITI = 'nuovi_dimessi_guariti'
    NUOVI_DECEDUTI = 'nuovi_deceduti'
    NUOVI_CONTAGIATI = 'nuovi_contagiati'
    NUOVI_TAMPONI = 'nuovi_tamponi'

    ABRUZZO = 'Abruzzo'
    BASILICATA = 'Basilicata'
    PROVINCIA_AUTONOMA_DI_BOLZANO = "P.A. Bolzano"
    CALABRIA = "Calabria"
    CAMPANIA = "Campania"
    EMILIA_ROMAGNA = "Emilia-Romagna"
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

    TRENTINO_ALTO_ADIGE = [PROVINCIA_AUTONOMA_DI_BOLZANO,
                           PROVINCIA_AUTONOMA_DI_TRENTO]

    ITALIA = [ABRUZZO, BASILICATA, CALABRIA, CAMPANIA, EMILIA_ROMAGNA,
              FRIULI_VENEZIA_GIULIA, LAZIO, LIGURIA, LOMBARDIA, MARCHE,
              MOLISE, PIEMONTE, PROVINCIA_AUTONOMA_DI_BOLZANO,
              PROVINCIA_AUTONOMA_DI_TRENTO, PUGLIA, SARDEGNA, SICILIA,
              TOSCANA, UMBRIA, VALLE_DI_AOSTA, VENETO]

    NORD = [EMILIA_ROMAGNA,
            FRIULI_VENEZIA_GIULIA, LIGURIA, LOMBARDIA,
            PIEMONTE, PROVINCIA_AUTONOMA_DI_BOLZANO,
            PROVINCIA_AUTONOMA_DI_TRENTO, VALLE_DI_AOSTA, VENETO]

    CENTRO = [LAZIO, MARCHE, TOSCANA, UMBRIA]

    SUD = [ABRUZZO, BASILICATA, CALABRIA, CAMPANIA, MOLISE, PUGLIA,
           SARDEGNA, SICILIA]

    def __init__(self, denominazione_regione):
        self._pop = PopolazioneRegioniItaliane(denominazione_regione)
        self._all = self.load_csv_regioni()
        self._createLabel(denominazione_regione)
        if not isinstance(denominazione_regione, list):
            denominazione_regione = (denominazione_regione,)
        self._filter = \
            self._all[self.DENOMINAZIONE_REGIONE].isin(denominazione_regione)
        self._data = self._all[self._filter].groupby(self.DATA).sum()

    def _createLabel(self, denominazione_regione):
        if denominazione_regione == self.ITALIA:
            self._label = "Italia"
        elif denominazione_regione == self.CENTRO:
            self._label = "Centro"
        elif denominazione_regione == self.NORD:
            self._label = "Nord"
        elif denominazione_regione == self.SUD:
            self._label = "Sud e Isole"
        else:
            self._label = denominazione_regione

    @property
    def data_frame(self):
        return self._data

    @property
    def popolazione(self):
        return self._pop

    @property
    def stato(self):
        return self.select(self.STATO)

    @property
    def codice_regione(self):
        return self.select(self.CODICE_REGIONE)

    @property
    def denominazione_regione(self):
        return self._label

    @property
    def latitudine(self):
        return self.select(self.LATITUDINE)

    @property
    def longitudine(self):
        return self.select(self.LONGITUDINE)

    @property
    def data(self):
        return np.array([datetime.datetime.strptime(
            d, '%Y-%m-%dT%H:%M:%S') for d in self._data.index])

    @property
    def ricoverati_con_sintomi(self):
        return self.select(self.RICOVERATI_CON_SINTOMI)

    @property
    def terapia_intensiva(self):
        return self.select(self.TERAPIA_INTENSIVA)

    @property
    def totale_ospedalizzati(self):
        return self.select(self.TOTALE_OSPEDALIZZATI)

    @property
    def isolamento_domiciliare(self):
        return self.select(self.ISOLAMENTO_DOMICILIARE)

    @property
    def totale_positivi(self):
        return self.select(self.TOTALE_POSITIVI)

    @property
    def variazione_totali_positivi(self):
        return self.select(self.VARIAZIONE_TOTALE_POSITIVI)

    @property
    def dimessi_guariti(self):
        return self.select(self.DIMESSI_GUARITI)

    @property
    def deceduti(self):
        return self.select(self.DECEDUTI)

    @property
    def totale_casi(self):
        return self.select(self.TOTALE_CASI)

    @property
    def tamponi(self):
        return self.select(self.TAMPONI)

    @property
    def nuovi_contagiati(self):
        return diff_from_zero(self.totale_casi)

    @property
    def nuovi_deceduti(self):
        return diff_from_zero(self.deceduti)

    @property
    def nuovi_dimessi_guariti(self):
        return diff_from_zero(self.dimessi_guariti)

    @property
    def nuovi_tamponi(self):
        return diff_from_zero(self.tamponi)

    @property
    def variazione_ricoverati_con_sintomi(self):
        return diff_from_zero(self.ricoverati_con_sintomi)

    @property
    def variazione_terapia_intensiva(self):
        return diff_from_zero(self.terapia_intensiva)

    @property
    def variazione_totale_ospedalizzati(self):
        return diff_from_zero(self.totale_ospedalizzati)

    @property
    def variazione_isolamento_domiciliare(self):
        return diff_from_zero(self.isolamento_domiciliare)

    def select(self, what):
        if what == self.NUOVI_CONTAGIATI:
            return self.nuovi_contagiati
        elif what == self.NUOVI_DECEDUTI:
            return self.nuovi_deceduti
        elif what == self.NUOVI_DIMESSI_GUARITI:
            return self.nuovi_dimessi_guariti
        elif what == self.NUOVI_TAMPONI:
            return self.nuovi_tamponi
        elif what == self.VARIAZIONE_RICOVERATI_CON_SINTOMI:
            return self.variazione_ricoverati_con_sintomi
        elif what == self.VARIAZIONE_TERAPIA_INTENSIVA:
            return self.variazione_terapia_intensiva
        elif what == self.VARIAZIONE_TOTALE_OSPEDALIZZATI:
            return self.variazione_totale_ospedalizzati
        elif what == self.VARIAZIONE_ISOLAMENTO_DOMICILIARE:
            return self.variazione_isolamento_domiciliare
        else:
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


class PopolazioneRegioniItaliane():

    DENOMINAZIONE_REGIONE = 'regione'
    RESIDENTI = 'residenti'
    SUPERFICIE = 'superficie'
    NUMERO_COMUNI = 'n_comuni'
    NUMERO_PROVINCE = 'n_province'
    DENSITA = 'densita'

    ABRUZZO = 'Abruzzo'
    BASILICATA = 'Basilicata'
    CALABRIA = "Calabria"
    CAMPANIA = "Campania"
    EMILIA_ROMAGNA = "Emilia-Romagna"
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
    UMBRIA = "Umbria"
    VALLE_DI_AOSTA = "Valle d'Aosta"
    VENETO = "Veneto"
    TRENTINO_ALTO_ADIGE = "Trentino-Alto Adige"

    ITALIA = [ABRUZZO, BASILICATA, CALABRIA, CAMPANIA, EMILIA_ROMAGNA,
              FRIULI_VENEZIA_GIULIA, LAZIO, LIGURIA, LOMBARDIA, MARCHE,
              MOLISE, PIEMONTE, PUGLIA, SARDEGNA, SICILIA,
              TOSCANA, TRENTINO_ALTO_ADIGE, UMBRIA, VALLE_DI_AOSTA, VENETO]

    NORD = [EMILIA_ROMAGNA,
            FRIULI_VENEZIA_GIULIA, LIGURIA, LOMBARDIA,
            PIEMONTE, TRENTINO_ALTO_ADIGE, VALLE_DI_AOSTA, VENETO]

    CENTRO = [LAZIO, MARCHE, TOSCANA, UMBRIA]

    SUD = [ABRUZZO, BASILICATA, CALABRIA, CAMPANIA, MOLISE, PUGLIA,
           SARDEGNA, SICILIA]

    def __init__(self, denominazione_regione):
        self._all = self.load_csv_regioni()
        self._createLabel(denominazione_regione)
        if not isinstance(denominazione_regione, list):
            denominazione_regione = (denominazione_regione,)
        self._filter = \
            self._all[self.DENOMINAZIONE_REGIONE].isin(denominazione_regione)
        self._data = self._all[self._filter].sum()

    def _createLabel(self, denominazione_regione):
        if denominazione_regione == self.ITALIA:
            self._label = "Italia"
        elif denominazione_regione == self.CENTRO:
            self._label = "Centro"
        elif denominazione_regione == self.NORD:
            self._label = "Nord"
        elif denominazione_regione == self.SUD:
            self._label = "Sud e Isole"
        else:
            self._label = denominazione_regione

    @property
    def data_frame(self):
        return self._data

    def select(self, what):
        if what == self.DENSITA:
            return self.densita
        else:
            return self._data[what]

    @property
    def residenti(self):
        return self.select(self.RESIDENTI)

    @property
    def superficie(self):
        return self.select(self.SUPERFICIE)

    @property
    def densita(self):
        return self.residenti / self.superficie

    @property
    def numero_comuni(self):
        return self.select(self.NUMERO_COMUNI)

    @property
    def numero_province(self):
        return self.select(self.NUMERO_PROVINCE)

    def load_csv_regioni(self):
        rootDir = dataRootDir()
        filename = os.path.join(rootDir,
                                'popolazione_italiana',
                                'popolazione_regioni.csv')
        return pd.read_csv(filename, sep=';')
