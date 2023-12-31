# -*- coding: utf-8 -*-
"""Ds_Job_Preprocessing-Cleaning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-en2GQDDVY0Yu9NQYj6ujecEeZrtsnX1
"""

import pandas as pd
import numpy as np

df = pd.read_csv(r"C:\Users\mrmhm\Desktop\Python\Datasets For Projects\Uncleaned_DS_jobs.csv")

"""# Handling `-1` In Columns"""

def correctMinusOne(df, cols):
    for col in cols:
        df.loc[(df[col] == '-1'), col] = np.nan

correctMinusOne(df, ['Headquarters', 'Size', 'Type of ownership', 'Industry', 'Sector', 'Revenue', 'Competitors'])
df.loc[(df['Founded'] == -1), 'Founded'] = np.nan

"""# Drop Duplicates"""

df.drop_duplicates()

df.info()

"""# Columns Evaluation

#### Working on `Salary Estimate` Column
"""

import re
def extractSalary(salary_string):
    pattern = r'\$(\d+)K-\$(\d+)K'
    match = re.search(pattern, salary_string)
    if match:
        min_salary = int(match.group(1))
        max_salary = int(match.group(2))
        return min_salary, max_salary
    else:
        return None, None

df[["Min_Salary", "Max_Salary"]] = df['Salary Estimate'].apply(extractSalary).apply(pd.Series)

df.drop(columns=['Salary Estimate'], inplace = True)

"""#### Working on `Company Name` Column"""

def companyName(co_name):
    co_name = ''.join(filter(str.isalpha, co_name))
    return co_name

df['Company Name'] = df['Company Name'].apply(companyName).apply(pd.Series)

"""#### Extract State Code In `Location` Column"""

def extractLocation(loc):
    return loc.split(',')[0].strip()

df['Location'] = df['Location'].apply(extractLocation).apply(pd.Series)

"""#### Extract Company Size:"""

def extractSize(size):
    pattern = r'(\d+) to (\d+)'
    if isinstance(size, str):
        match = re.match(pattern, size)
        if match :
            min_size = int(match.group(1))
            max_size = int(match.group(2))
            return min_size, max_size
        else:
            return None, None

df[['Min_Size', 'Max_Size']] = df['Size'].apply(extractSize).apply(pd.Series)

"""#### Categorization on `Revenue` Column"""

df['Revenue'].value_counts()

def group_categories(revenue):
    if isinstance(revenue, str):
        if revenue == 'Unknown / Non-Applicable':
            return 'Unknown / Non-Applicable'
        elif 'billion' in revenue:
            return 'High Revenue'
        elif 'million' in revenue:
            return 'Medium Revenue'
        elif 'less than' in revenue:
            return 'Low Revenue'
        else:
            return revenue

df['Revenue'] = df['Revenue'].apply(group_categories).apply(pd.Series)

df['Revenue'].value_counts()

df.head(5)

"""___________________________

#### `Rating` Column
"""

bin_edges = [-2, 0, 2, 3, 4, 5]
bin_labels = ['Very Poor', 'Poor', 'Fair', 'Good', 'Excellent']  # Define bin labels

df['Rating'] = pd.cut(df['Rating'], bins=bin_edges, labels=bin_labels)

df['Rating'].value_counts()

"""____________________________________________

#### `Type of ownership` Column
"""

df['Type of ownership'].value_counts()

df['Type of ownership'].isna().value_counts()

df['Type of ownership'].fillna('Other', inplace = True)

def ownership(ownership):
    if "Company" in ownership:
        return 'Corporate'
    elif "Nonprofit" in ownership:
        return 'Non-Profit'
    elif "Government" in ownership :
        return 'Goverment'
    else:
        return 'Other'

df['Type of ownership'] = df['Type of ownership'].apply(ownership).apply(pd.Series)

df['Type of ownership'].value_counts()

"""#### `Industry` Columns"""

df['Industry'].value_counts()

df['Industry'].isna().value_counts()

"""#### `Competitors` Column"""

df['Competitors'].value_counts()

df['Competitors'].isna().value_counts()

"""#### `Job Title` Column"""

df['Job Title'].value_counts()

df['Job Title'].nunique()

"""# Drop unuseable columns"""

df.drop(columns= ['Headquarters', 'Competitors', 'Location', 'Company Name', 'Founded', 'Job Description', 'index' ,'Size'], inplace = True)

"""# fill NaNs"""

df.fillna(value={
    'Industry' : df['Industry'].fillna(method='bfill'),
    'Sector' : df['Sector'].fillna(method= 'bfill'),
    'Revenue' : df['Revenue'].mode()[0],
    'Min_Salary' : df['Min_Salary'].median(),
    'Max_Salary' : df['Max_Salary'].median(),
    'Min_Size' : df['Min_Size'].fillna(method = 'ffill'),
    'Max_Size' : df['Max_Size'].fillna(method = 'ffill')

}, inplace = True)

"""# Rename the Columns"""

df.rename(columns= {
    'Job Title' : 'Title',
    'Type of ownership' : 'Ownership_Type',
}, inplace = True)

"""# Save to CSV"""

df

df.to_csv('preprocessed.csv', index = False)

