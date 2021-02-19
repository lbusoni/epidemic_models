import pandas as pd
import json
import urllib

fname = '/Users/lbusoni/Downloads/somministrazioni-vaccini-summary-latest.json'
url = 'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/consegne-vaccini-latest.json'


class Vaccinations():

    def __init__(self, url_json):
        r = urllib.request.urlretrieve(url_json)
        d = json.load(open(r[0]))
        self._v = pd.DataFrame(d['data'])
        self._v['data_consegna'] = self._v['data_consegna'].astype('datetime64[ns]')
        self._s = d['schema']

    def _consegnati_per_data(self):
        return self._v.groupby('data_consegna').agg('sum')['numero_dosi']

