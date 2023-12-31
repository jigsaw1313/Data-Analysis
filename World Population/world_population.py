# -*- coding: utf-8 -*-
"""world_population.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1p6k8JXojY2sWfaqdQQZ6vSvxSTVGUkw5

# EDA in Pandas
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# load dataset
df = pd.read_csv("") # insert path of dataset in your machine
df

"""#### Set decimal format"""

pd.set_option('display.float_format', lambda x: '%.2f' % x)

df

"""#### Check pd.info()"""

df.info()

"""#### Check pd.describe()"""

df.describe()

"""#### check dtypes of df"""

df.dtypes

# check numeric columns
df.select_dtypes(include='number')

# check str columns
df.select_dtypes(include='object')

"""#### check missing values"""

df.isnull().sum()

"""#### check unique values there are in each column"""

df.nunique()

"""### Top 5 countries based on population on `2020 Population`"""

df

df.sort_values(by = '2020 Population', ascending=False).head(10)

"""#### check correlation"""

df.corr(numeric_only = True)

"""#### Visualizing correlation using seaborn heatmatp"""

plt.figure(figsize = (20, 7))
sns.heatmap(df.corr(numeric_only = True), annot = True)
plt.show()

"""#### Check population's growth per continent"""

df

df.groupby('Continent').mean(numeric_only=True).sort_values(by = '2022 Population', ascending = False)

"""##### __Check `Oceania` Continent's countries__"""

df[df['Continent'].str.contains('Oceania')]

"""#### Visualization of population growth per continent from 1970 to 2022"""

df.columns

# make new datafram from below code
df2 = df.groupby('Continent')[['1970 Population',
       '1980 Population', '1990 Population', '2000 Population',
       '2010 Population', '2015 Population', '2020 Population',
       '2022 Population']].mean(numeric_only=True).sort_values(by = '2022 Population', ascending = False)

df2

# plotting
df2.plot(figsize = (20, 10))

"""#### Transpose `df2` and plot it"""

df3 = df2.transpose()
df3

df3.plot(figsize = (20, 10))

"""#### Boxplot for outliers"""

df.boxplot(figsize = (20, 10))

# check quartiles of each column
def filter_outliers(col):
    Q1 = df['2022 Population'].quantile(0.25)
    Q3 = df['2022 Population'].quantile(0.75)
    IQR = Q3 - Q1
    filtered_data = df[(df['2022 Population'] < (Q1 - 1.5 * IQR)) | (df['2022 Population'] > (Q3 + 1.5 * IQR))]
    return filtered_data

filter_outliers(['2022 Population'])

filter_outliers(['1970 Population'])

