import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

df_raw = pd.read_csv('https://raw.githubusercontent.com/4GeeksAcademy/data-preprocessing-project-tutorial/main/AB_NYC_2019.csv')
 

# We proceed to drop the columns last_review and host_name and eliminate the rows 
# that have no name and no host_name, as well as eliminate any outliers 
# in the price column, stratified by borough

df_raw['name'] = pd.Categorical(df_raw['name'])
df_raw['neighbourhood_group'] = pd.Categorical(df_raw['neighbourhood_group'])
df_raw['neighbourhood'] = pd.Categorical(df_raw['neighbourhood'])
df_raw['room_type'] = pd.Categorical(df_raw['room_type'])

df_raw = df_raw.drop(columns = ['host_name','last_review'])

boroughs = np.array(df_raw['neighbourhood_group'].unique())
for borough in boroughs:
    stat = df_raw[df_raw['neighbourhood_group'] == borough]['price'].describe()
    IQR = stat['75%'] - stat['25%']
    superior = stat['75%'] + IQR*1.5
    inferior = stat['25%'] - IQR*1.5
    count_upper = df_raw[df_raw['neighbourhood_group'] == borough][df_raw['price']>superior]['price'].shape[0]
    mean = stat['mean']
    df_raw.loc[(df_raw['neighbourhood_group'] == borough) & (df_raw['price']>superior),'price'] = mean

df_raw = df_raw[df_raw['price'] != 0]

df_raw['reviews_per_month'] = df_raw['reviews_per_month'].fillna(0)

df_raw = df_raw.dropna()

df_raw['room_type'] = df_raw['room_type'].map({'Entire home/apt' : 0, 'Private room': 1, 'Shared room': 2})
df_raw['neighbourhood_group'] = df_raw['neighbourhood_group'].map({'Bronx' : 0, 'Brooklyn': 1, 'Manhattan': 2, 'Queens': 3, 'Staten Island': 4})

df_raw.to_csv('/workspace/Data-Preprocessing-Project/data/processed/df_processed.csv')