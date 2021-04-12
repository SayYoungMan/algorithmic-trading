import pandas as pd
from pywt import wavedec
from numpy import log
import os

# Read the dataset
df = pd.read_csv('snp500_9-4-21.csv')

# 1. Data Preprocessing
df['YesClose'] = df['Close/Last'].shift(-1)
df = df[:-1]
df['logReturn'] = log(df['Close/Last']/df['YesClose'])

# 2. Wavelet Transform
subseries = {}
for basis_num in range (1, 5):
    for stage in range (1, 7):
        coeffs = wavedec(df['logReturn'], f'db{basis_num}', level=stage)
        cAn, cDn = coeffs[0], coeffs[1]
        subseries[f'DB{basis_num}A{stage}'] = cAn
        subseries[f'DB{basis_num}D{stage}'] = cDn

