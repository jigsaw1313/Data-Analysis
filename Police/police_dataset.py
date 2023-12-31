# -*- coding: utf-8 -*-
"""Police-Dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16cT5u8-RV0Q_Xn2apsmXMzJ0j3lLwfIt

# Import Libs
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# import dataset
df = pd.read_csv('police.csv')

"""# Initial review of df"""

# check df
df.head()

df.info()
# there is a column which is all nan, and some columns has missing values

df.describe()

# check df dim
df.shape

# check columns
df.columns

"""# get unique of columns"""

# check unique values of df
df.nunique()

categorical_cols = ['driver_gender', 'driver_race', 'violation_raw', 'violation', 'search_type', 'stop_outcome']
for col in categorical_cols:
    print(f"{col} unique values:\n ", df[col].unique())
    print('-' * 50)

"""# get value_counts of columns"""

categorical_cols = ['driver_gender', 'driver_race', 'violation_raw', 'violation', 'search_type', 'stop_outcome']
for col in categorical_cols:
    print(df[col].value_counts())
    print('-' * 50)

"""# check boolean columns"""

bool_cols = ['search_conducted', 'is_arrested', 'drugs_related_stop']
for col in bool_cols:
    print(df[col].value_counts())
    print("-" * 50)

"""# Drop `county_name` which has only null values"""

df['county_name'].isnull().sum()

# drop country_name feature
df.drop(columns= ['county_name'], inplace = True)

# check df
df.info()

"""# Handling Missing Values"""

df.info()

# mean imputation for numerical columns
numerical_columns = ['driver_age_raw', 'driver_age']
for col in numerical_columns:
    df[col].fillna(df[col].mean(), inplace=True)

# Example of mode imputation for categorical columns
categorical_columns = ['driver_gender', 'driver_race', 'violation_raw', 'violation', 'stop_outcome', 'is_arrested']
for col in categorical_columns:
    df[col].fillna(df[col].mode()[0], inplace=True)

# analyzing missing values
missing_values = df.isnull().sum()
missing_values

"""# check `stop_date` columns and extract date, month, day"""

df['stop_date'] = pd.to_datetime(df['stop_date'])
# extract date, month, day
df['year'] = df['stop_date'].dt.year
df['month'] = df['stop_date'].dt.month
df['day'] = df['stop_date'].dt.day

df.head()

"""# Men or women were stopped more often for speeding :"""

df[(df['violation'] == 'Speeding')]

df[(df['violation'] == 'Speeding')]['driver_gender'].value_counts()

"""# Does gender affect who gets searched during a stop ?"""

df.groupby('driver_gender')['search_conducted'].sum()

df['search_conducted'].value_counts()

"""# Mean stop_duration"""

# check df
df.head(3)

# check stop_duration values
df['stop_duration'].value_counts()

df['stop_duration'] = df['stop_duration'].map({'0-15 Min': 7.5, '16-30 Min': 24, '30+ Min' : 45})

df.head()

df['stop_duration'].mean()

"""# Age Distribution for each violation"""

df.groupby('violation')['driver_age'].describe()

"""# Cross-tabulation for categorical variables"""

cross_tab = pd.crosstab(df['driver_gender'], df['violation'])
cross_tab

"""# Visualization"""

correlation_matrix = df.select_dtypes(include=np.number).corr()
correlation_matrix

plt.figure(figsize=(12, 4))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, cbar_kws={'shrink': 0.8, 'format': '%.2f'})
plt.title('Correlation Matrix Heatmap', fontsize=20, pad=20)
plt.xlabel('Features', fontsize=16, labelpad=10)
plt.ylabel('Features', fontsize=16, labelpad=10)
plt.xticks(fontsize=12, rotation=45)
plt.yticks(fontsize=12, rotation=0)
plt.show()

"""## Age distribution by driver age"""

plt.figure(figsize=(10, 6))
sns.histplot(df['driver_age'], kde=True)
plt.title('Driver Age Distribution', fontsize = 20)
plt.xlabel("Driver Age", fontsize = 15)
plt.ylabel('Count', fontsize = 15)
plt.show()

"""# Analysis of search-related information based on various factors"""

plt.figure(figsize = (12, 5))
sns.countplot(x = 'violation', hue = 'search_conducted', data = df)
plt.title("Search Conducted based on Violation", fontsize = 15)
plt.ylabel('Count', fontsize = 10)
plt.xlabel('Violation', fontsize = 10)
plt.legend(fontsize = 10)
plt.show()

"""# Stop duration analysis based on violation type"""

plt.figure(figsize = (12, 5))
sns.boxplot(x = 'violation', y='stop_duration', data = df)
plt.title("Stop Duration Based on Violation", fontsize = 15)
plt.xlabel('Duration', fontsize = 10)
plt.ylabel('Violation Type', fontsize = 10)
plt.show()

"""# Stop Time"""

df['stop_hour'] = pd.to_datetime(df['stop_time']).dt.hour
plt.figure(figsize=(10, 6))
sns.countplot(x='stop_hour', data=df, palette='viridis')
plt.title('Stop Distribution by Hour of the Day')
plt.xlabel('Stop Hour')
plt.ylabel('Count')
plt.show()

"""# Analysis of drugs-related stops"""

plt.figure(figsize = (10, 7))
sns.countplot(x='violation', hue='drugs_related_stop', data=df)
plt.title('Was the Stop Related to Drugs ?')
plt.xlabel ("Count")
plt.ylabel("Violation")
plt.legend()
plt.show()

"""# Bar plot for Violation Count"""

plt.figure ( figsize = (12, 6))
df['violation'].value_counts().plot(kind = 'bar', color = 'skyblue')
plt.title("Violation Count", fontsize = 16, pad = 20)
plt.xlabel("Violation Types", fontsize = 16, labelpad = 20)
plt.ylabel("Counts", fontsize = 16, labelpad = 20)
plt.xticks(rotation = 45, ha = 'right', fontsize = 10)
plt.show()

"""# Pie Chart for driver race distribution"""

plt.figure(figsize=(15, 15))
df['driver_race'].value_counts().plot(kind = 'pie', autopct = '%1.1f%%', colors = sns.color_palette('pastel'), startangle = 90)
plt.title('Driver Race Distribution')
plt.ylabel('')
plt.legend()
plt.show()

"""# Count Plot for search conducted based on gender"""

plt.figure(figsize=(10, 6))
sns.countplot(x='search_conducted', hue='driver_gender', data=df, palette='muted')
plt.title('Search Conducted by Gender', fontsize=16, pad=20)
plt.xlabel('Search Conducted', fontsize=12, labelpad=10)
plt.ylabel('Count', fontsize=12, labelpad=10)
plt.legend()
plt.show()

"""# Stacked Bar for stop outcome by gender"""

stop_outcome_gender = df.groupby(['stop_outcome', 'driver_gender']).size().unstack()
stop_outcome_gender.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.title('Stop Outcome by Gender', fontsize=16, pad=20)
plt.xlabel('Stop Outcome', fontsize=12, labelpad=10)
plt.ylabel('Count', fontsize=12, labelpad=10)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.show()

