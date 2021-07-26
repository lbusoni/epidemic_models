
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

    _DICT = {"ABR": ABRUZZO, "BAS": BASILICATA, "CAL": CALABRIA, "CAM": CAMPANIA,
             "EMR": EMILIA_ROMAGNA, "FVG": FRIULI_VENEZIA_GIULIA, "LAZ": LAZIO,
             "LIG": LIGURIA, "LOM": LOMBARDIA, "MAR": MARCHE, "MOL": MOLISE,
             "PAB": None, "PAT": None, "PIE": PIEMONTE, "PUG": PUGLIA,
             "SAR": SARDEGNA, "SIC": SICILIA, "TOS": TOSCANA, "UMB": UMBRIA,
             "VDA": VALLE_DI_AOSTA, "VEN": VENETO,
             "ITALIA": ITALIA, "NORD": NORD, "CENTRO": CENTRO, "SUD": SUD}

    def __init__(self, denominazione_regione):
        self._all = self.load_csv_regioni()
        denominazione_regione = self._translate(denominazione_regione)
        self._createLabel(denominazione_regione)
        if not isinstance(denominazione_regione, list):
            denominazione_regione = (denominazione_regione,)
        self._filter = \
            self._all[self.DENOMINAZIONE_REGIONE].isin(denominazione_regione)
        self._data = self._all[self._filter].sum()

    def _translate(self, denominazione_regione):
        if isinstance(denominazione_regione, str):
            if denominazione_regione in self._DICT:
                denominazione_regione = self._DICT[denominazione_regione]
        return denominazione_regione

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


class PopolazioneFasceAnagrafiche():
    ABRUZZO = 'ITF1'
    BASILICATA = 'ITF5'
    CALABRIA = "ITF6"
    CAMPANIA = "ITF3"
    EMILIA_ROMAGNA = "ITD5"
    FRIULI_VENEZIA_GIULIA = "ITD4"
    LAZIO = "ITE4"
    LIGURIA = "ITC3"
    LOMBARDIA = "ITC4"
    MARCHE = "ITE3"
    MOLISE = "ITF2"
    PIEMONTE = "ITC1"
    PROVINCIA_BOLZANO = "ITD1"
    PROVINCIA_TRENTO = "ITD2"
    PUGLIA = "ITF4"
    SARDEGNA = "ITG2"
    SICILIA = "ITG1"
    TOSCANA = "ITE1"
    UMBRIA = "ITE2"
    VALLE_DI_AOSTA = "ITC2"
    VENETO = "ITD3"

    ITALIA = "IT"
    NORD_EST = "ITD"
    NORD_OVEST = "ITC"
    CENTRO = "ITE"
    ISOLE = "ITG"
    SUD = "ITF"

    _DICT = {"ABR": ABRUZZO, "BAS": BASILICATA, "CAL": CALABRIA, "CAM": CAMPANIA,
             "EMR": EMILIA_ROMAGNA, "FVG": FRIULI_VENEZIA_GIULIA, "LAZ": LAZIO,
             "LIG": LIGURIA, "LOM": LOMBARDIA, "MAR": MARCHE, "MOL": MOLISE,
             "PAB": PROVINCIA_BOLZANO, "PAT": PROVINCIA_TRENTO, "PIE": PIEMONTE, "PUG": PUGLIA,
             "SAR": SARDEGNA, "SIC": SICILIA, "TOS": TOSCANA, "UMB": UMBRIA,
             "VDA": VALLE_DI_AOSTA, "VEN": VENETO,
             "ITALIA": ITALIA, "NORD_EST": NORD_EST, "NORD_OVEST": NORD_OVEST,
             "CENTRO": CENTRO, "ISOLE": ISOLE, "SUD": SUD}

    def __init__(self):
        self._p = self._load_csv_fasce_anagrafiche()
        self._p['eta'] = self._p.apply(self._convert_eta_to_integer, axis=1)

    @staticmethod
    def _convert_eta_to_integer(record):
        if "_GE100" in record['ETA1']:
            return 100
        elif "TOTAL" in record['ETA1']:
            return -1
        else:
            return int(record['ETA1'][1:])

    def _translate(self, denominazione_regione):
        if denominazione_regione is None:
            return self.ITALIA
        if isinstance(denominazione_regione, str):
            if denominazione_regione in self._DICT:
                denominazione_regione = self._DICT[denominazione_regione]
        return denominazione_regione

    def _load_csv_fasce_anagrafiche(self):
        rootDir = dataRootDir()
        filename = os.path.join(rootDir,
                                'popolazione_italiana',
                                'popolazione_eta_regioni.csv')
        return pd.read_csv(filename, sep=',')

    def _filtra(self, sesso, eta_min, eta_max, area=None):
        area = self._translate(area)
        aa = self._p
        return aa[(aa.ITTER107 == area) & (aa.Sesso == sesso) &
                  (aa.eta >= eta_min) & (aa.eta <= eta_max)]["Value"].sum()

    def fascia(self, eta_min, eta_max, area=None):
        return self._filtra("totale", eta_min, eta_max, area)

    def maschi(self, eta_min, eta_max, area=None):
        return self._filtra("maschi", eta_min, eta_max, area)

    def femmine(self, eta_min, eta_max, area=None):
        return self._filtra("femmine", eta_min, eta_max, area)


class PostiLettoItalia():

    DENOMINAZIONE_REGIONE = 'Regioni'
    AREA_NON_CRITICA = 'PL in Area Non Critica'
    TERAPIA_INTENSIVA = 'PL in Terapia Intensiva'
    TERAPIA_INTENSIVA_ATTIVABILI = 'PL Terapia Intensiva attivabili'

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
    PROVINCIA_BOLZANO = "P.A. Bolzano"
    PROVINCIA_TRENTO = "P.A. Trento"
    PIEMONTE = "Piemonte"
    PUGLIA = "Puglia"
    SARDEGNA = "Sardegna"
    SICILIA = "Sicilia"
    TOSCANA = "Toscana"
    UMBRIA = "Umbria"
    VALLE_DI_AOSTA = "Valle d'Aosta"
    VENETO = "Veneto"

    ITALIA = [ABRUZZO, BASILICATA, CALABRIA, CAMPANIA, EMILIA_ROMAGNA,
              FRIULI_VENEZIA_GIULIA, LAZIO, LIGURIA, LOMBARDIA, MARCHE,
              MOLISE, PIEMONTE, PUGLIA, SARDEGNA, SICILIA,
              TOSCANA, PROVINCIA_BOLZANO, PROVINCIA_TRENTO, UMBRIA,
              VALLE_DI_AOSTA, VENETO]

    TRENTINO_ALTO_ADIGE = [PROVINCIA_BOLZANO, PROVINCIA_TRENTO]

    NORD = [EMILIA_ROMAGNA,
            FRIULI_VENEZIA_GIULIA, LIGURIA, LOMBARDIA,
            PIEMONTE, TRENTINO_ALTO_ADIGE, VALLE_DI_AOSTA, VENETO]

    CENTRO = [LAZIO, MARCHE, TOSCANA, UMBRIA]

    SUD = [ABRUZZO, BASILICATA, CALABRIA, CAMPANIA, MOLISE, PUGLIA,
           SARDEGNA, SICILIA]

    def __init__(self, area=None):
        self._all = self._load_csv_posti_letto()
        if area is None:
            area = self.ITALIA
        self._posti_letto = self._filtra_per_area(area)

    def _filtra_per_area(self, area):
        if not isinstance(area, list):
            lista_regioni = (area,)
        else:
            lista_regioni = area
        filtro = \
            self._all[self.DENOMINAZIONE_REGIONE].isin(lista_regioni)
        return self._all[filtro].sum()

    def _load_csv_posti_letto(self):
        rootDir = dataRootDir()
        filename = os.path.join(rootDir,
                                'popolazione_italiana',
                                'posti_letto_italia.csv')
        return pd.read_csv(filename, sep=';')

    def terapia_intensiva(self):
        return self._posti_letto[self.TERAPIA_INTENSIVA]

    def area_non_critica(self):
        return self._posti_letto[self.AREA_NON_CRITICA]

    def terapia_intensiva_attivabili(self):
        return self._posti_letto[self.TERAPIA_INTENSIVA_ATTIVABILI]
