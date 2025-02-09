# -*- coding: utf-8 -*-
"""Synapse Task2

Automatically generated by Colaboratory.

Original file is located at https://colab.research.google.com/drive/1nN7c8TH_7GZLAWRbdEAazOtADrHhcySy
"""
import pandas as pd

# Original Data
orig_df = pd.read_json('./data.json')
data = pd.DataFrame([col for col in orig_df.data])
data = pd.concat([data.drop(['location'], axis=1),
                  data['location'].apply(pd.Series)], axis=1)

# Drop unneeded data
data = data.drop(columns=['marital_status'])

# Remove aged users
data = data[(data['age'] != '45-54') & (data['age'] != '55+')]
#data = data.drop(columns='age')

# Filtering non-compatible categories
data = data[(data['category'] == 'Environment')
            | (data['category'] == 'Sports')]
#data = data.drop(columns='category')

# Only keep most valuable entries from each user
ids = []
cat = []
evt = []
dup = []

for ind in data.index:
    try:
        loc = ids.index(data['session_id'][ind])
        if evt[loc] == 'Fund Project' and data['event_name'][ind] == 'Fund Project':
            pass  # check for prices here if needed
        elif evt[loc] == 'Fund Project':
            dup.append(ind)
        elif data['event_name'][ind] == 'Fund Project':
            # Remove view item
            ids.pop(loc)
            cat.pop(loc)
            evt.pop(loc)
            # Add Fund item
            ids.append(data['session_id'][ind])
            cat.append(data['category'][ind])
            evt.append(data['event_name'][ind])
        else:
            dup.append(ind)
    except ValueError:
        ids.append(data['session_id'][ind])
        cat.append(data['category'][ind])
        evt.append(data['event_name'][ind])
    except Exception as e:
        print(e)

data = data.drop(index=dup)
data = data.reset_index(drop=True)

data_ind = data.copy()
data_ind.drop_duplicates(subset="session_id", keep='first', inplace=True)

# Stats by gender
data_ind['gender'].value_counts().plot.bar()

# Stats by mobile device
data_ind['device'].value_counts().plot.bar()

# Stats by age
data_ind['age'].value_counts().plot.bar()

# Stats by state
data_ind['state'].value_counts().plot.bar(figsize=(20, 5))

# Stats by city
data_ind['city'].value_counts().plot.bar(figsize=(500, 200))

# Stats by amount
data['amount'].plot.hist()

# Amount by Gender
m = 0
f = 0
u = 0

for ind in data.index:
    if data['event_name'][ind] == 'Fund Project':
        if data['gender'][ind] == 'M':
            m = m + data['amount'][ind]
        if data['gender'][ind] == 'F':
            f = f + data['amount'][ind]
        if data['gender'][ind] == 'U':
            u = u + data['amount'][ind]

datadct = {'M': [m], 'F': [f], 'U': [u]}
datav = pd.DataFrame(datadct, columns=['M', 'F', 'U'])
datav.plot.bar()
