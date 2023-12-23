# -*- coding: utf-8 -*-
"""Ds_Job_Data Scaling & Encoding.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-bLTH1f1TahaMcRuGqw46aKPXpOUpKCr
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv('preprocessed.csv')
df

df.info()

"""# Encoding
Using sklearn LabelEncoder
"""

def encoder(df, columns):
    le = LabelEncoder()
    for col in columns:
        df[col] = le.fit_transform(df[col])
    return df

encoder(df, ['Title', 'Rating', 'Ownership_Type', 'Industry', 'Sector', 'Revenue'])

"""# Data Scaling"""

def scaler(df, columns):
    scaler = MinMaxScaler()
    df = scaler.fit_transform(df)
    df = pd.DataFrame(df)
    df.columns = columns
    return df

scaler(df, [['Title', 'Rating', 'Ownership_Type', 'Industry', 'Sector', 'Revenue', 'Min_Salary', 'Max_Salary', 'Min_Size', 'Max_Size']])

df.to_csv('preocessed_2.csv', index = False)
