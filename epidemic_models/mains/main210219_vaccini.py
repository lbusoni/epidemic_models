import pandas as pd
import json
import urllib
from epidemic_models.restore_data import PopolazioneFasceAnagrafiche


class Vaccinations():

    URL_CONSEGNE = 'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/consegne-vaccini-latest.json'
    URL_SOMMINISTRAZIONI = 'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.json'
    URL_VACCINI_SUMMARY = 'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/vaccini-summary-latest.json'
    URL_ANAGRAFICA_SUMMARY = 'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/anagrafica-vaccini-summary-latest.json'

    def __init__(self):
        self._lazy_somm = None
        self._load_consegne()
        self._load_anagrafica_summary()
        self._load_vaccini_summary()
        self._popolazione = PopolazioneFasceAnagrafiche()

    def _load_consegne(self):
        r = urllib.request.urlretrieve(self.URL_CONSEGNE)
        d = json.load(open(r[0]))
        self._consegne = pd.DataFrame(d['data'])
        self._consegne['data_consegna'] = self._consegne['data_consegna'].astype('datetime64[ns]')
        self._consegne_schema = d['schema']

    def _load_vaccini_summary(self):
        r = urllib.request.urlretrieve(self.URL_VACCINI_SUMMARY)
        d = json.load(open(r[0]))
        self._vaccini = pd.DataFrame(d['data'])
        self._vaccini_schema = d['schema']

    def _load_anagrafica_summary(self):
        r = urllib.request.urlretrieve(self.URL_ANAGRAFICA_SUMMARY)
        d = json.load(open(r[0]))
        self._anagrafica = pd.DataFrame(d['data'])
        self._anagrafica_schema = d['schema']

    def _load_somministrazioni(self):
        r = urllib.request.urlretrieve(self.URL_SOMMINISTRAZIONI)
        d = json.load(open(r[0]))
        somministrazioni = pd.DataFrame(d['data'])
        somministrazioni['data_somministrazione'] = somministrazioni['data_somministrazione'].astype('datetime64[ns]')
        somministrazioni_schema = d['schema']
        somministrazioni['dosi'] = somministrazioni.apply(lambda x: x['sesso_maschile'] + x['sesso_femminile'], axis=1)
        return somministrazioni, somministrazioni_schema

    @property
    def _somministrazioni(self):
        if self._lazy_somm is None:
            somm, somm_sch = self._load_somministrazioni()
            self._lazy_somm = somm
            self._lazy_somm_sch = somm_sch
        return self._lazy_somm

    def _consegnati_per_data(self, area=None):
        ss = self._filtra_per_area(self._consegne, area)
        return ss.groupby('data_consegna').agg('sum')['numero_dosi']

    def _consegnati_per_data_per_fornitore(self, area=None):
        ss = self._filtra_per_area(self._consegne, area)
        return ss.groupby(
            ['fornitore', 'data_consegna']).agg('sum')['numero_dosi']

    def plot_delivered(self, area=None):
        ax = self._consegnati_per_data(area=area).cumsum().plot()
        ax.grid(True)

    def plot_somministrati_per_categoria(self, area=None):
        ss = self._filtra_per_area(self._somministrazioni, area)
        ds = ss[[
            'data_somministrazione',
            'categoria_operatori_sanitari_sociosanitari',
            'categoria_personale_non_sanitario',
            'categoria_ospiti_rsa',
            'categoria_over80',
            'categoria_forze_armate',
            'categoria_personale_scolastico',
#            'prima_dose',
#            'seconda_dose',
#            'sesso_maschile',
#            'sesso_femminile'
            ]]
        ax = ds.groupby('data_somministrazione').agg('sum').cumsum().plot()
        ax.grid(True)

    def totale_sesso_maschile(self):
        return self._somministrazioni['sesso_maschile'].sum()

    def totale_sesso_femminile(self):
        return self._somministrazioni['sesso_femminile'].sum()

    def totale_prima_dose(self):
        return self._somministrazioni['prima_dose'].sum()

    def totale_seconda_dose(self):
        return self._somministrazioni['seconda_dose'].sum()

    def totale_dosi(self):
        return self._somministrazioni['dosi'].sum()

    def fornitori(self):
        return self._consegne['fornitore'].unique()

    def fasce_anagrafiche(self):
        return self._somministrazioni['fascia_anagrafica'].unique()

    def _filtra_per_area(self, cosa, area=None):
        if area:
            ss = cosa.query('area == @area')
        else:
            ss = cosa
        return ss

    def somministrati_per_fornitore(self, fornitore, area=None):
        ss = self._filtra_per_area(self._somministrazioni, area)
        ds = ss[[
            'data_somministrazione',
            'fornitore',
            'categoria_operatori_sanitari_sociosanitari',
            'categoria_personale_non_sanitario',
            'categoria_ospiti_rsa',
            'categoria_over80',
            'categoria_forze_armate',
            'categoria_personale_scolastico',
            'prima_dose',
            'seconda_dose',
            'dosi',
            'sesso_maschile',
            'sesso_femminile'
            ]]

        return ds[ds.fornitore == fornitore].groupby('data_somministrazione').agg('sum')

    def plot_somministrati_per_fornitore(self, area=None, **kwargs):
        ax = None
        for forn in self.fornitori():
            ax = self.somministrati_per_fornitore(forn, area=area)['dosi'].cumsum().plot(
                ax=ax, label=forn, **kwargs)
        ax.legend()
        ax.grid(True)

    def plot_consegnati_per_fornitore(self, area=None, **kwargs):
        aa = self._consegnati_per_data_per_fornitore(area=area)
        ax = None
        for forn in self.fornitori():
            ax = aa[forn].cumsum().plot(
                ax=ax, label=forn, drawstyle='steps-post', **kwargs)
        ax.legend()
        ax.grid(True)

    def plot_consegne_e_somministrazioni(self, area=None):
        self.plot_consegnati_per_fornitore(area=area, linestyle='-')
        self.plot_somministrati_per_fornitore(area=area, linestyle='-.')

    def somministrati_per_fascia_anagrafica(self, fascia_anagrafica, area=None):
        ss = self._filtra_per_area(self._somministrazioni, area)
#         ds = ss[[
#             'data_somministrazione',
#             'fascia_anagrafica'
#             'prima_dose',
#             'seconda_dose',
#             'dosi',
#             'sesso_maschile',
#             'sesso_femminile'
#             ]]
        ret = ss[ss.fascia_anagrafica == fascia_anagrafica].groupby('data_somministrazione').agg('sum')
        ret['frazione'] = ret.apply(lambda x: x['dosi'] / self._popolazione_in_fascia(fascia_anagrafica), axis=1)
        return ret

    def plot_somministrati_per_fascia_anagrafica(self, area=None, **kwargs):
        ax = None
        for fas in self.fasce_anagrafiche():
            ax = self.somministrati_per_fascia_anagrafica(fas, area=area)['dosi'].cumsum().plot(
                ax=ax, label=fas, **kwargs)
        ax.legend()
        ax.grid(True)

    def plot_somministrati_per_fascia_anagrafica_frazione(self, area=None, **kwargs):
        ax = None
        for fas in self.fasce_anagrafiche():
            ax = self.somministrati_per_fascia_anagrafica(fas, area=area)['frazione'].cumsum().plot(
                ax=ax, label=fas, **kwargs)
        ax.legend()
        ax.grid(True)

    def _popolazione_in_fascia(self, fascia_str):
        if '+' in fascia_str:
            aa = fascia_str.split('+')
            aa[1] = 300
        else:
            aa = fascia_str.split('-')
        eta_min = int(aa[0])
        eta_max = int(aa[1])
        return self._popolazione.fascia(eta_min, eta_max)

