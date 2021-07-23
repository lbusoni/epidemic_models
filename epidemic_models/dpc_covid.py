import numpy as np
from epidemic_models.restore_data import PopolazioneRegioniItaliane,\
    diff_from_zero
import datetime
from epidemic_models.utils.package_data import dataRootDir
import os
import pandas as pd
from epidemic_models.utils.today import dataAtToday
from pickle import NONE


class DpcCovid():
    '''
    ospedalizzati = ricoverati_con_sintomi + terapia_intensiva
    totale_attualmente_positivi = ospedalizzati + isolamento_domiciliare
    nuovi_attualmente_positivi = diff(totale_attualmente_positivi)
    totale_casi = totale_attualmente_positivi + dimessi_guariti + deceduti

    Nota: nuovi_attualmente_positivi non serve a niente

    Aggiungo:
    nuovi_contagiati = diff(totale_casi) corrisponde al numero di persone
    passate da sani a positivi oggi, cioè al numero di nuove contagi. EDIT: 
    ora è nel db, sotto nuovi_positivi. Elimino nuovi_contagiati
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
    NUOVI_POSITIVI = 'nuovi_positivi'
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
    NUOVI_TAMPONI = 'nuovi_tamponi'
    INCIDENZA_SETTIMANALE = 'incidenza_settimanale_per_100k'

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

    def __init__(self, denominazione_regione=None):
        if denominazione_regione is None:
            denominazione_regione = self.ITALIA
        self._pop = PopolazioneRegioniItaliane(denominazione_regione)
        self._all = self.load_csv_regioni()
        self._createLabel(denominazione_regione)
        if not isinstance(denominazione_regione, list):
            denominazione_regione = (denominazione_regione,)
        self._filter = \
            self._all[self.DENOMINAZIONE_REGIONE].isin(denominazione_regione)
        self._all[self.DATA] = self._all[self.DATA].astype(
            'datetime64[ns]')
        self._data = self._all[self._filter].groupby(self.DATA).agg('sum')
        self._add_my_variables()

    def _add_my_variables(self):
        self._data[self.NUOVI_DECEDUTI] = diff_from_zero(self.deceduti)
        self._data[self.NUOVI_DIMESSI_GUARITI] = diff_from_zero(
            self.dimessi_guariti)
        self._data[self.NUOVI_TAMPONI] = diff_from_zero(self.tamponi)
        self._data[self.VARIAZIONE_RICOVERATI_CON_SINTOMI] = diff_from_zero(
            self.ricoverati_con_sintomi)
        self._data[self.VARIAZIONE_TERAPIA_INTENSIVA] = diff_from_zero(
            self.terapia_intensiva)
        self._data[self.VARIAZIONE_TOTALE_OSPEDALIZZATI] = diff_from_zero(
            self.totale_ospedalizzati)
        self._data[self.VARIAZIONE_ISOLAMENTO_DOMICILIARE] = diff_from_zero(
            self.isolamento_domiciliare)
        self._data[self.INCIDENZA_SETTIMANALE] = self._rolling_sum(
            self.nuovi_positivi, how_long='7d') / self._pop.residenti * 1e5

    def _rolling_sum(self, what, how_long='7d'):
        return what.rolling(how_long).sum()

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
        return self._data.index

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
    def nuovi_positivi(self):
        return self.select(self.NUOVI_POSITIVI)

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
    def nuovi_deceduti(self):
        return self.select(self.NUOVI_DECEDUTI)

    @property
    def nuovi_dimessi_guariti(self):
        return self.select(self.NUOVI_DIMESSI_GUARITI)

    @property
    def nuovi_tamponi(self):
        return self.select(self.NUOVI_TAMPONI)

    @property
    def variazione_ricoverati_con_sintomi(self):
        return self.select(self.VARIAZIONE_RICOVERATI_CON_SINTOMI)

    @property
    def variazione_terapia_intensiva(self):
        return self.select(self.VARIAZIONE_TERAPIA_INTENSIVA)

    @property
    def variazione_totale_ospedalizzati(self):
        return self.select(self.VARIAZIONE_TOTALE_OSPEDALIZZATI)

    @property
    def variazione_isolamento_domiciliare(self):
        return self.select(self.VARIAZIONE_ISOLAMENTO_DOMICILIARE)

    @property
    def incidenza_settimanale(self):
        return self.select(self.INCIDENZA_SETTIMANALE)

    def select(self, what):
        return self._data[what]

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

    def plot_summary(self):
        import matplotlib.pyplot as plt

        plt.figure()
        ax = None
        ax = self.deceduti.plot(
            ax=ax, label='deceduti', ls='-', marker='.')
        ax = self.dimessi_guariti.plot(
            ax=ax, label='dimessi_guariti', ls='-', marker='.')
        ax = self.totale_casi.plot(
            ax=ax, label='totale_casi', ls='-', marker='.')
        ax = self.tamponi.plot(
            ax=ax, label='tamponi', ls='-', marker='.')
        ax.plot([], [], ' ', label=dataAtToday())
        ax.set_title('Cumulative - %s' % self._label)
        ax.semilogy()
        ax.legend()
        ax.grid(True)

        plt.figure()
        ax = None
        ax = self.totale_positivi.plot(
            ax=ax, label='totale positivi', ls='-', marker='.')
        ax = self.isolamento_domiciliare.plot(
            ax=ax, label='isolamento domiciliare', ls='-', marker='.')
        ax = self.ricoverati_con_sintomi.plot(
            ax=ax, label='ricoverati con sintomi', ls='-', marker='.')
        ax = self.terapia_intensiva.plot(
            ax=ax, label='terapia intensiva', ls='-', marker='.')
        ax.plot([], [], ' ', label=dataAtToday())

        ax2 = ax.twinx()
        self.incidenza_settimanale.plot(
            ax=ax2, label='incidenza settimanale', ls='-', marker='.',
            color='k')
        ax2.set_ylabel('Incidenza settimanale per 100k')

        ax.set_title('Positive  - %s' % self._label)
        ax.semilogy()
        ax.grid(True)
        ax.legend()

        plt.figure()
        ax = None
        ax = self.nuovi_positivi.plot(
            ax=ax, label='nuovi positivi', ls='-', marker='.')
        ax = self.nuovi_deceduti.plot(
            ax=ax, label='nuovi deceduti', ls='-', marker='.')
        ax = self.nuovi_dimessi_guariti.plot(
            ax=ax, label='nuovi dimessi', ls='-', marker='.')
        ax.plot([], [], ' ', label=dataAtToday())
        ax.set_title('Daily variation - %s' % self._label)
        ax.semilogy()
        ax.legend()
        ax.grid(True)
