import pandas as pd
import json
import urllib
import matplotlib.pyplot as plt
from epidemic_models.restore_data import PopolazioneFasceAnagrafiche
import numpy as np
from datetime import datetime, timedelta


class Vaccinations():

    URL_CONSEGNE = 'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/consegne-vaccini-latest.json'
    URL_SOMMINISTRAZIONI = 'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.json'
    URL_VACCINI_SUMMARY = 'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/vaccini-summary-latest.json'
    URL_ANAGRAFICA_SUMMARY = 'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/anagrafica-vaccini-summary-latest.json'

    PRIMA_DOSE = 'prima_dose'
    SECONDA_DOSE = 'seconda_dose'
    DOSI_TOTALI = 'dosi'
    FRAZIONE_PRIMA_DOSE = 'frazione_prima_dose'
    FRAZIONE_SECONDA_DOSE = 'frazione_seconda_dose'
    FRAZIONE_DOSI_TOTALI = 'frazione_dosi'

    def __init__(self):
        self._lazy_somm = None
        self._load_consegne()
        self._load_anagrafica_summary()
        self._load_vaccini_summary()
        self._load_consegne_previste()
        self._popolazione = PopolazioneFasceAnagrafiche()

    def _load_consegne(self):
        r = urllib.request.urlretrieve(self.URL_CONSEGNE)
        d = json.load(open(r[0]))
        self._consegne = pd.DataFrame(d['data'])
        self._consegne['data_consegna'] = self._consegne['data_consegna'].astype(
            'datetime64[ns]')
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
        somministrazioni['data_somministrazione'] = somministrazioni['data_somministrazione'].astype(
            'datetime64[ns]')
        somministrazioni_schema = d['schema']
        somministrazioni[self.DOSI_TOTALI] = somministrazioni.apply(
            lambda x: x['sesso_maschile'] + x['sesso_femminile'], axis=1)
        return somministrazioni, somministrazioni_schema

    def _load_consegne_previste(self):
        self._consegne_previste = ConsegnePreviste().consegne_previste

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

    def _consegnati_per_data_e_fornitore(self, area=None):
        ss = self._filtra_per_area(self._consegne, area)
        return ss.groupby(
            ['fornitore', 'data_consegna']).agg('sum')['numero_dosi']

    def _previsti_per_data_e_fornitore(self, area=None):
        ss = self._filtra_per_area(self._consegne_previste, area)
        return ss.groupby(
            ['fornitore', 'data_consegna']).agg('sum')['numero_dosi']

    def consegnati_per_fornitore(self, area=None):
        ss = self._filtra_per_area(self._consegne, area)
        return ss.groupby('fornitore').agg('sum')['numero_dosi']

    def plot_somministrati_per_categoria(self, area=None):
        ss = self._filtra_per_area(self._somministrazioni, area)
        ds = ss[[
            'data_somministrazione',
            #            'categoria_operatori_sanitari_sociosanitari',
            #            'categoria_personale_non_sanitario',
            #            'categoria_ospiti_rsa',
            #            'categoria_over80',
            #            'categoria_forze_armate',
            #            'categoria_personale_scolastico',
            #            'categoria_altro',
        ]]
        ax = ds.groupby('data_somministrazione').agg('sum').cumsum().plot()
        ax.grid(True)

    def totale_sesso_maschile(self):
        return self._somministrazioni['sesso_maschile'].sum()

    def totale_sesso_femminile(self):
        return self._somministrazioni['sesso_femminile'].sum()

    def totale_prima_dose(self):
        return self._somministrazioni[self.PRIMA_DOSE].sum()

    def totale_seconda_dose(self):
        return self._somministrazioni[self.SECONDA_DOSE].sum()

    def totale_dosi(self):
        return self._somministrazioni[self.DOSI_TOTALI].sum()

    def fornitori(self):
        return self._consegne['fornitore'].unique()

    def fasce_anagrafiche(self):
        return self._somministrazioni['fascia_anagrafica'].unique()

    def aree_territoriali(self):
        return self._somministrazioni['area'].unique()

    def _filtra_per_area(self, cosa, area=None):
        if area:
            ss = cosa.query('area == @area')
        else:
            ss = cosa
        return ss

    def _somministrati_per_data_e_fornitore(self, area=None):
        ss = self._filtra_per_area(self._somministrazioni, area)
        ds = ss[[
            'data_somministrazione',
            'fornitore',
            #            'categoria_operatori_sanitari_sociosanitari',
            #            'categoria_personale_non_sanitario',
            #            'categoria_ospiti_rsa',
            #            'categoria_over80',
            #            'categoria_forze_armate',
            #            'categoria_personale_scolastico',
            self.PRIMA_DOSE,
            self.SECONDA_DOSE,
            self.DOSI_TOTALI,
            'sesso_maschile',
            'sesso_femminile'
        ]]

        return ds.groupby(['fornitore', 'data_somministrazione']).agg('sum')

    def plot_consegnati(self, area=None):
        ax = self._consegnati_per_data(area=area).cumsum().plot()
        ax.grid(True)

    def plot_somministrati_per_fornitore(self, area=None, **kwargs):
        ax = None
        for forn in self.fornitori():
            ax = self._somministrati_per_data_e_fornitore(
                area=area)[self.DOSI_TOTALI][forn].cumsum().plot(
                ax=ax, label=forn, **kwargs)
        ax.legend()
        ax.grid(True)

    def plot_consegnati_per_fornitore(self, area=None, **kwargs):
        aa = self._consegnati_per_data_e_fornitore(area=area)
        ax = None
        for forn in self.fornitori():
            ax = aa[forn].cumsum().plot(
                ax=ax, label=forn, drawstyle='steps-post', **kwargs)
        ax.legend()
        ax.grid(True)

    def plot_previsti_per_fornitore(self, area=None, **kwargs):
        aa = self._previsti_per_data_e_fornitore(area=area)
        ax = None
        for forn in self.fornitori():
            ax = aa[forn].cumsum().plot(
                ax=ax, label=forn, **kwargs)
        ax.legend()
        ax.grid(True)

    def plot_consegnati_e_somministrati(self, area=None):
        self.plot_consegnati_per_fornitore(area=area, linestyle='-')
        self.plot_somministrati_per_fornitore(area=area, linestyle='-.')
        plt.title("%s" % (area if area else "ITA"))

    def riserve_per_fornitore(self, area=None):
        riserve = {}
        cons = self.consegnati_per_fornitore(area)
        somm = self.somministrati_per_fornitore(area)
        for forn in self.fornitori():
            riserve[forn] = cons[forn] - somm[forn]
        return riserve

    def somministrati_per_fornitore(self, area=None):
        ss = self._filtra_per_area(self._somministrazioni, area)
        return ss.groupby('fornitore').agg('sum')[self.DOSI_TOTALI]

    def somministrati(
            self, fascia_anagrafica=None, area=None):
        ss = self._filtra_per_area(self._somministrazioni, area)
        if fascia_anagrafica is None:
            ret = ss.groupby('data_somministrazione').agg('sum')
            pop = self._popolazione_in_fascia("0+", area=area)
        else:
            ret = ss[ss.fascia_anagrafica == fascia_anagrafica].groupby(
                'data_somministrazione').agg('sum')
            pop = self._popolazione_in_fascia(fascia_anagrafica, area=area)
        ret[self.FRAZIONE_DOSI_TOTALI] = ret.apply(
            lambda x: x[self.DOSI_TOTALI] / pop, axis=1)
        ret[self.FRAZIONE_PRIMA_DOSE] = ret.apply(
            lambda x: x[self.PRIMA_DOSE] / pop, axis=1)
        ret[self.FRAZIONE_SECONDA_DOSE] = ret.apply(
            lambda x: x[self.SECONDA_DOSE] / pop, axis=1)
        return ret

    def somministrati_velocita(self, area=None, rolling_mean='14d'):
        return self.somministrati(area=area).rolling(rolling_mean).mean()

    def plot_somministrati_velocita(self, area=None, dose=None, rolling_mean='14d', **kwargs):
        fraz = self._keyword_dose_to_frazione(dose)
        ax = self.somministrati_velocita(
            area=area, rolling_mean=rolling_mean)[fraz].plot(
                label='%s - %s' % (area, dose), **kwargs)
        ax.legend()
        ax.set_ylabel('Frazione popolazione / day')
        ax.set_title('Velocità')
        ax.grid(True)

    def plot_somministrati_per_fascia_anagrafica(
            self, area=None, dose=None, **kwargs):
        if dose is None:
            dose = self.DOSI_TOTALI
        ax = None
        for fas in self.fasce_anagrafiche():
            ax = self.somministrati(fascia_anagrafica=fas, area=area)[
                dose].cumsum().plot(
                ax=ax, label=fas, **kwargs)
        ax.legend()
        ax.set_ylabel('Dosi')
        ax.set_title('Dosi per fascia anagrafica - %s' %
                     (area if area else "ITA"))
        ax.grid(True)

    def _keyword_dose_to_frazione(self, key):
        if key == self.DOSI_TOTALI or key is None:
            return self.FRAZIONE_DOSI_TOTALI
        elif key == self.PRIMA_DOSE:
            return self.FRAZIONE_PRIMA_DOSE
        elif key == self.SECONDA_DOSE:
            return self.FRAZIONE_SECONDA_DOSE
        else:
            raise ValueError("unknown key %s" % key)

    def plot_somministrati_per_fascia_anagrafica_frazione(
            self, area=None, dose=None, **kwargs):
        fraz = self._keyword_dose_to_frazione(dose)
        ax = None
        for fas in self.fasce_anagrafiche():
            ax = self.somministrati(fascia_anagrafica=fas, area=area)[fraz].cumsum().plot(
                ax=ax, label=fas, **kwargs)
        ax.legend()
        ax.set_ylabel('Dosi per persona')
        ax.set_title('Dosi per persona per fascia anagrafica - %s' %
                     (area if area else "ITA"))
        ax.grid(True)

    def _popolazione_in_fascia(self, fascia_str, area=None):
        if '+' in fascia_str:
            aa = fascia_str.split('+')
            aa[1] = 300
        else:
            aa = fascia_str.split('-')
        eta_min = int(aa[0])
        eta_max = int(aa[1])
        return self._popolazione.fascia(eta_min, eta_max, area)

    def plot_somministrati_per_fascia_anagrafica_rispetto_a_italia(
            self, area=None, dose=None, **kwargs):
        fraz = self._keyword_dose_to_frazione(dose)
        for fas in self.fasce_anagrafiche():
            reg = self.somministrati(fascia_anagrafica=fas, area=area)[
                fraz].cumsum()
            ita = self.somministrati(fascia_anagrafica=fas)[fraz].cumsum()
            plt.plot((reg - ita) / ita * 100, label=fas, **kwargs)
        plt.legend()
        plt.ylabel('Scostamento rispetto a media italiana [%]')
        plt.title('Scostamento rispetto a ITA per fascia anagrafica - %s' % area)
        plt.grid(True)

    def plot_consegnati_per_area_per_popolazione(self):
        for area in self.aree_territoriali():
            dosi = self._consegnati_per_data(area=area).cumsum()
            pop = self._popolazione.fascia(0, 200, area=area)
            plt.plot(dosi / pop, label=area)
        plt.legend()
        plt.ylabel("Dosi consegnate per persona")
        plt.grid(True)

    def plot_stack_fascia_anagrafica_per_area(self):
        aa = self._somministrazioni.groupby(["area", "fascia_anagrafica"]).agg(sum)[
            self.DOSI_TOTALI].unstack()
        bb = self._somministrazioni.groupby("area").agg(sum)[self.DOSI_TOTALI]
        cc = 100 * aa.div(bb, axis='rows')
        cc.plot.bar(stacked=True)
        plt.legend(loc='upper center', bbox_to_anchor=(
            0.5, 1.2), fancybox=True, ncol=5)

#     def plot_stack_categoria_per_area(self):
#         ds = self._somministrazioni[[
#             'area',
#             'categoria_operatori_sanitari_sociosanitari',
#             'categoria_personale_non_sanitario',
#             'categoria_ospiti_rsa',
#             'categoria_over80',
#             'categoria_forze_armate',
#             'categoria_personale_scolastico',
#         ]]

        aa = ds.groupby("area").agg(sum)
        bb = self._somministrazioni.groupby("area").agg(sum)[self.DOSI_TOTALI]
        cc = 100 * aa.div(bb, axis='rows')
        cc.plot.bar(stacked=True)
        plt.legend(loc='upper center', bbox_to_anchor=(
            0.5, 1.2), fancybox=True, ncol=2)

    def plot_stack_riserve_per_area(self):
        aa = self._somministrazioni.groupby(["area", "fornitore"]).agg(sum)[
            self.DOSI_TOTALI].unstack()
        bb = self._consegne.groupby(["area", "fornitore"]).agg(sum)[
            "numero_dosi"].unstack()
        cc = bb - aa
        cc.plot.bar(stacked=True)
        plt.legend(loc='upper center', bbox_to_anchor=(
            0.5, 1.2), fancybox=True, ncol=3)

    def quando_mi_tocca(self, eta, area=None, con_richiamo=False):
        fas = []
        y = eta // 10 * 10
        while y < 90:
            fas.append("%d-%d" % (y, y + 9))
            y += 10
        fas.append('90+')

        mancano = 0
        for f in fas:
            mancano += (1 - self.somministrati(fascia_anagrafica=f, area=area)[
                self.FRAZIONE_PRIMA_DOSE].sum()
            ) * self._popolazione_in_fascia(f, area=area)
            if con_richiamo:
                mancano += (1 - self.somministrati(fascia_anagrafica=f,
                                                   area=area)[
                    self.FRAZIONE_SECONDA_DOSE].sum()
                ) * self._popolazione_in_fascia(f, area=area)

        somministrazioni_al_giorno = self.somministrati_velocita(
            area=area)[self.DOSI_TOTALI][-1]
        giorni_necessari = mancano / somministrazioni_al_giorno
        eta = datetime.today() + timedelta(giorni_necessari)
        return (mancano,
                somministrazioni_al_giorno,
                giorni_necessari,
                eta)


class ConsegnePreviste():

    def __init__(self, piano='210321'):
        if piano == '210321':
            self._piano_consegne = self._data210321()
        elif piano == '210303':
            self._piano_consegne = self._data210303()
        else:
            raise ValueError("Piano vaccinale %s sconosciuto" % piano)
        self._consegne_previste = self._linear_interpolation(
            self._piano_consegne)

    @property
    def consegne_previste(self):
        return self._consegne_previste

    def _data210303(self):
        '''
        From http://www.salute.gov.it/imgs/C_17_pagineAree_5452_4_file.pdf
        '''

        fornitori_lista = [
            'AstraZeneca', 'Pfizer/BioNTech', 'J&J', 'Sanofi', 'Curevac', 'Moderna']
        n_fornitori = len(fornitori_lista)
        dataQ0 = {
            'data_consegna': pd.to_datetime(["2021-01-01"] * n_fornitori),
            'fornitore': fornitori_lista,
            'numero_dosi': np.array([0, 0.456, 0, 0, 0, 0]) * 1e6
        }
        dataQ1 = {
            'data_consegna': pd.to_datetime(["2021-03-31"] * n_fornitori),
            'fornitore': fornitori_lista,
            'numero_dosi': dataQ0['numero_dosi'] + np.array([
                5.35225, 7.352 + 1.660748, 0, 0, 0, 1.33]) * 1e6
        }
        dataQ2 = {
            'data_consegna': pd.to_datetime(["2021-06-30"] * n_fornitori),
            'fornitore': fornitori_lista,
            'numero_dosi': dataQ1['numero_dosi'] + np.array([
                10.0425,
                8.76 + 4.982243 + 9.420515,
                7.307292,
                0,
                7.314904,
                4.65]) * 1e6
        }
        dataQ3 = {
            'data_consegna': pd.to_datetime(["2021-09-30"] * n_fornitori),
            'fornitore': fornitori_lista,
            'numero_dosi': dataQ2['numero_dosi'] + np.array([
                24.771250,
                10.792 + 0.5 * 6.642991 + 9.420515,
                15.943184,
                0,
                6.64,
                4.6487 + 3.32 + 6]) * 1e6
        }
        dataQ4 = {
            'data_consegna': pd.to_datetime(["2021-12-31"] * n_fornitori),
            'fornitore': fornitori_lista,
            'numero_dosi': dataQ3['numero_dosi'] + np.array([
                0,
                0.5 * 6.642991 + 6.280344,
                3.321497,
                0,
                7.968,
                7.3087 + 12.5]) * 1e6
        }
        dataQ5 = {
            'data_consegna': pd.to_datetime(["2022-03-31"] * n_fornitori),
            'fornitore': fornitori_lista,
            'numero_dosi': dataQ4['numero_dosi'] + np.array([
                0,
                0,
                0,
                20.19,
                7.968,
                0]) * 1e6
        }
        dataQ6 = {
            'data_consegna': pd.to_datetime(["2022-06-30"] * n_fornitori),
            'fornitore': fornitori_lista,
            'numero_dosi': dataQ5['numero_dosi'] + np.array([
                0,
                0,
                0,
                20.19,
                0,
                0]) * 1e6
        }

        columns = ['data_consegna', 'fornitore', 'numero_dosi']
        d0 = pd.DataFrame(dataQ0, columns=columns)
        d1 = pd.DataFrame(dataQ1, columns=columns)
        d2 = pd.DataFrame(dataQ2, columns=columns)
        d3 = pd.DataFrame(dataQ3, columns=columns)
        d4 = pd.DataFrame(dataQ4, columns=columns)
        d5 = pd.DataFrame(dataQ5, columns=columns)
        d6 = pd.DataFrame(dataQ6, columns=columns)
        dd = pd.concat([d0, d1, d2, d3, d4, d5, d6], ignore_index=True)
        return dd

    def _data210321(self):
        '''
        From https://www.trovanorme.salute.gov.it/norme/renderPdf.spring?seriegu=SG&datagu=24/03/2021&redaz=21A01802&artp=1&art=1&subart=1&subart1=10&vers=1&prog=001
        '''

        fornitori_lista = [
            'Vaxzevria (AstraZeneca)', 'Pfizer/BioNTech', 'Janssen', 'Sanofi', 'Curevac', 'Moderna']
        n_fornitori = len(fornitori_lista)
        dataQ0 = {
            'data_consegna': pd.to_datetime(["2021-01-01"] * n_fornitori),
            'fornitore': fornitori_lista,
            'numero_dosi': np.array([0, 0, 0, 0, 0, 0])
        }
        dataQ1 = {
            'data_consegna': pd.to_datetime(["2021-03-31"] * n_fornitori),
            'fornitore': fornitori_lista,
            'numero_dosi': dataQ0['numero_dosi'] + np.array([
                16.155, 8.749, 0, 0, 2.019, 1.346]) * 1e6
        }
        dataQ2 = {
            'data_consegna': pd.to_datetime(["2021-06-30"] * n_fornitori),
            'fornitore': fornitori_lista,
            'numero_dosi': dataQ1['numero_dosi'] + np.array([
                24.225, 8.076, 14.806, 0, 5.384, 4.711]) * 1e6
        }
        dataQ3 = {
            'data_consegna': pd.to_datetime(["2021-09-30"] * n_fornitori),
            'fornitore': fornitori_lista,
            'numero_dosi': dataQ2['numero_dosi'] + np.array([
                0, 10.095, 32.304, 0, 6.73, 4.711]) * 1e6
        }
        dataQ4 = {
            'data_consegna': pd.to_datetime(["2021-12-31"] * n_fornitori),
            'fornitore': fornitori_lista,
            'numero_dosi': dataQ3['numero_dosi'] + np.array([
                0, 0, 6.73, 0, 8.076, 0]) * 1e6
        }
        dataQ5 = {
            'data_consegna': pd.to_datetime(["2022-03-31"] * n_fornitori),
            'fornitore': fornitori_lista,
            'numero_dosi': dataQ4['numero_dosi'] + np.array([
                0, 0, 0, 20.19, 8.076, 0]) * 1e6
        }
        dataQ6 = {
            'data_consegna': pd.to_datetime(["2022-06-30"] * n_fornitori),
            'fornitore': fornitori_lista,
            'numero_dosi': dataQ5['numero_dosi'] + np.array([
                0, 0, 0, 20.19, 0, 0]) * 1e6
        }

        columns = ['data_consegna', 'fornitore', 'numero_dosi']
        d0 = pd.DataFrame(dataQ0, columns=columns)
        d1 = pd.DataFrame(dataQ1, columns=columns)
        d2 = pd.DataFrame(dataQ2, columns=columns)
        d3 = pd.DataFrame(dataQ3, columns=columns)
        d4 = pd.DataFrame(dataQ4, columns=columns)
        d5 = pd.DataFrame(dataQ5, columns=columns)
        d6 = pd.DataFrame(dataQ6, columns=columns)
        dd = pd.concat([d0, d1, d2, d3, d4, d5, d6], ignore_index=True)
        return dd

    def fornitori(self):
        return self._consegne_previste['fornitore'].unique()

    def _linear_interpolation(self, consegne):
        fornitori = consegne['fornitore'].unique()
        a = []
        for forn in fornitori:
            dd = consegne.query('fornitore == @forn')[
                ['data_consegna', 'numero_dosi']]
            dInt = dd.set_index('data_consegna').resample(
                'D').mean().interpolate('linear')
            dDiff = dInt.diff()
            dDiff['fornitore'] = forn
            a.append(dDiff)
        return pd.concat(a).reset_index()

    def consegnati_al(self, datetime):
        return self._consegne_previste.loc[datetime]


def sandbox():
    dP = dd.query('fornitore == "Pfizer/BioNTech"')[['datetime', 'dosi']]
    dP.set_index('datetime').resample('D').mean().interpolate('linear')

    # dMI = dd.groupby(['datetime', 'fornitore']).dosi.sum().to_frame()

    previstiQ0 = pd.Series({
        'AstraZeneca': 0,
        'Pfizer/BioNTech': 0.456e6,
        'Moderna': 0,
        'J&J': 0,
        'Curevac': 0,
    })

    previstiQ1 = pd.Series({
        'AstraZeneca': 5.35225e6,
        'Pfizer/BioNTech': 7.352e6 + 1.660748e6,
        'Moderna': 1.33e6,
        'J&J': 0,
        'Curevac': 0,
    })

    previstiQ2 = pd.Series({
        'AstraZeneca': 10.0425e6,
        'Pfizer/BioNTech': 8.76e6 + 4.982243e6 + 9.420515e6,
        'Moderna': 4.65e6,
        'J&J': 7.307292e6,
        'Curevac': 7.314904e6
    })

    #
    # trueFrac = vv.consegnati_per_fornitore() / previsti; trueFrac['J&J']=0.5; trueFrac['Curevac']=0.5
    trueFrac = pd.Series({
        'AstraZeneca': 0.462236,
        'Moderna': 0.621504,
        'Pfizer/BioNTech': 0.732732,
        'J&J': 0.500000,
        'Curevac': 0.500000})

    vv = Vaccinations()
    frTos = vv._popolazione_in_fascia(
        '0-200', area='TOS') / vv._popolazione_in_fascia('0-200')


def quando_tocca(vv, area=None):
    etas = [20, 30, 40, 50, 60, 70, 80]
    for eta in etas:
        a = vv.quando_mi_tocca(eta + 10, area=area, con_richiamo=False)[3]
        b = vv.quando_mi_tocca(eta, area=area, con_richiamo=True)[3]
        print(f"Eta {eta}: fra {a:%Y-%m-%d} e {b:%Y-%m-%d}")
