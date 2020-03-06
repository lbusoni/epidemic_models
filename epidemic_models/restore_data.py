
from openpyxl import load_workbook
from epidemic_models.utils.package_data import dataRootDir
import os
import numpy as np


def restoreCovid(region='Hubei'):
    ''' Data from https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset#covid_19_data.csv
    '''
    rootDir = dataRootDir()
    filename = os.path.join(rootDir,
                            'covid_19_data.xlsx')

    wb = load_workbook(filename=filename)
    ws = wb[region]
    deaths = np.array([c.value for c in ws['C']])
    date = np.array([c.value for c in ws['B']])
    return deaths, date
