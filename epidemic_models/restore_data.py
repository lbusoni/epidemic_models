
from openpyxl import load_workbook
from epidemic_models.utils.package_data import dataRootDir
import os
import numpy as np


def restoreCovid(region='Hubei'):
    rootDir = dataRootDir()
    filename = os.path.join(rootDir,
                            'covid_19_data.xlsx')

    wb = load_workbook(filename=filename)
    ws = wb['Hubei']
    deaths = np.array([c.value for c in ws['E']])
    date = np.array([c.value for c in ws['B']])
    return deaths, date
